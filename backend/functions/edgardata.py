import pandas as pd
import numpy as np
import logging
from typing import Optional, List, Dict, Any
from edgar import Company, XBRL, set_identity
import os
import json
from datetime import datetime
import concurrent.futures
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set identity for edgar-python
set_identity("abc@gmail.com")


class XBRLDataExtractor:
    """
    Enhanced XBRL data extraction with better error handling for amended filings
    and missing financial statements.
    """
    
    def __init__(self, min_periods: int = 5):
        """
        Initialize the extractor.
        
        Args:
            min_periods: Minimum number of valid periods required for output
        """
        self.min_periods = min_periods
        
    def get_statements(
        self, 
        ticker: str, 
        form: str = "10-Q", 
        statement: str = "income_statement",
        skip_amended: bool = True,
        limit: int = 20
    ) -> Optional[pd.DataFrame]:
        """
        Extract financial statements from XBRL filings with improved error handling.
        
        Args:
            ticker: Stock ticker symbol
            form: Filing form type (10-K, 10-Q)
            statement: Statement type (income_statement, balance_sheet, cashflow_statement)
            skip_amended: Skip amended filings (10-K/A, 10-Q/A) which may lack complete XBRL
            limit: Maximum number of filings to process
            
        Returns:
            Merged DataFrame with multiple periods, or None if insufficient data
        """
        
        try:
            company = Company(ticker)
        except Exception as e:
            logger.error(f"Failed to create Company object for {ticker}: {e}")
            return None
        
        df_list = []
        temp_date_list = []
        failed_filings = []
        
        try:
            filings = list(company.get_filings(form=form, amendments=not skip_amended))
        except Exception as e:
            logger.error(f"Failed to get filings for {ticker} with form {form}: {e}")
            return None
        
        if not filings:
            logger.warning(f"No filings found for {ticker} with form {form}")
            return None
        
        # Process filings (limit to most recent 'limit' filings)
        for idx, report in enumerate(filings[:limit]):
            try:
                # Log filing info
                filing_info = f"{report.company} | {report.form} | {report.filing_date}"
                
                # Skip amended filings if requested
                if skip_amended and report.form.endswith('/A'):
                    logger.debug(f"Skipping amended filing: {filing_info}")
                    continue
                
                # Attempt to load XBRL
                try:
                    xbrl = XBRL.from_filing(report)
                except Exception as e:
                    logger.warning(f"XBRL load failed for {filing_info}: {type(e).__name__}")
                    failed_filings.append((filing_info, str(e)))
                    continue
                
                if xbrl is None:
                    logger.debug(f"XBRL is None for {filing_info}")
                    failed_filings.append((filing_info, "XBRL is None"))
                    continue
                
                # Extract the appropriate statement
                try:
                    if statement == "income_statement":
                        content = xbrl.statements.income_statement()
                    elif statement == "balance_sheet":
                        content = xbrl.statements.balance_sheet()
                    elif statement == "cashflow_statement":
                        content = xbrl.statements.cashflow_statement()
                    else:
                        logger.error(f"Unknown statement type: {statement}")
                        continue
                    
                    if content is None:
                        logger.debug(f"Statement is None for {filing_info} ({statement})")
                        failed_filings.append((filing_info, f"No {statement}"))
                        continue
                    
                    # Render to dataframe
                    data = content.render().to_dataframe()
                    
                    # Keep only concept, label, and value columns
                    if len(data.columns) >= 3:
                        data = data[data.columns[0:3]]
                    else:
                        logger.warning(f"Insufficient columns for {filing_info}")
                        continue
                    
                    # Filter out rows with too many zeros (> 70% zeros)
                    if data.shape[0] > 0 and data.shape[1] > 2:
                        threshold = (data.shape[1] - 2) * 0.3  # Exclude concept/label columns
                        non_zero_counts = (data.iloc[:, 2:] != 0).sum(axis=1)
                        data = data[non_zero_counts > threshold]
                    
                    # Avoid duplicate date periods
                    period_date = data.columns[-1]
                    if period_date not in temp_date_list:
                        df_list.append(data)
                        temp_date_list.append(period_date)
                        logger.info(f"Successfully extracted {statement} from {filing_info} (Period: {period_date})")
                    else:
                        logger.debug(f"Duplicate period {period_date}, skipping {filing_info}")
                
                except Exception as e:
                    logger.warning(f"Statement extraction failed for {filing_info}: {type(e).__name__} - {str(e)[:100]}")
                    failed_filings.append((filing_info, f"Extraction error: {type(e).__name__}"))
                    continue
            
            except Exception as e:
                logger.error(f"Unexpected error processing filing {idx}: {e}")
                continue
        
        # Log summary of failures
        if failed_filings:
            logger.info(f"Failed to extract from {len(failed_filings)} filings:")
            for info, reason in failed_filings[:5]:  # Log first 5 failures
                logger.debug(f"  - {info}: {reason}")
            if len(failed_filings) > 5:
                logger.debug(f"  ... and {len(failed_filings) - 5} more")
        
        # Return None if insufficient data
        if len(df_list) < self.min_periods:
            logger.warning(
                f"Insufficient valid periods for {ticker} {statement}: "
                f"Found {len(df_list)}, required {self.min_periods}"
            )
            return None
        
        logger.info(f"Found {len(df_list)} valid periods for {ticker} {statement}")
        
        # Step 2: Merge the dataframes
        return self._merge_dataframes(df_list)
    
    def _merge_dataframes(self, df_list: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Merge multiple period dataframes into a single consolidated dataframe.
        
        Args:
            df_list: List of dataframes from different periods
            
        Returns:
            Merged dataframe with consolidated labels
        """
        
        # Establish reference order from first dataframe
        reference_order = df_list[0][['concept', 'label']].copy()
        reference_order['order'] = range(len(reference_order))
        
        # Group by label to create consistent ordering
        label_groups = reference_order.groupby('label').agg({
            'order': 'min',
            'concept': 'first'
        }).reset_index()
        label_groups = label_groups.rename(columns={
            'order': 'group_order',
            'concept': 'representative_concept'
        })
        
        # Get date columns
        date_columns = [df.columns[-1] for df in df_list]
        
        # Start merging
        merged_df = df_list[0].copy()
        for df in df_list[1:]:
            merged_df = pd.merge(
                merged_df,
                df,
                on=['concept', 'label'],
                how='outer'
            )
        
        # Convert date columns to numeric
        for col in date_columns:
            if col in merged_df.columns:
                merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
        
        # Aggregate by label (in case of duplicate concepts)
        agg_dict = {col: 'sum' for col in date_columns if col in merged_df.columns}
        agg_dict['concept'] = 'first'
        
        grouped_df = merged_df.groupby('label').agg(agg_dict).reset_index()
        
        # Merge with label groups to maintain order
        grouped_df = pd.merge(
            grouped_df,
            label_groups[['label', 'group_order', 'representative_concept']],
            on='label',
            how='left'
        )
        
        # Handle missing group orders (new labels not in reference)
        max_group_order = grouped_df['group_order'].max()
        max_group_order = 0 if pd.isna(max_group_order) else int(max_group_order)
        
        for idx, row in grouped_df[grouped_df['group_order'].isna()].iterrows():
            grouped_df.loc[idx, 'group_order'] = max_group_order + 1
            max_group_order += 1
        
        # Fill concept column
        grouped_df['concept'] = grouped_df.apply(
            lambda row: (
                row['representative_concept'] 
                if pd.notna(row['representative_concept']) 
                else row['concept']
            ),
            axis=1
        )
        
        # Sort by group order and clean up
        grouped_df = grouped_df.sort_values('group_order').reset_index(drop=True)
        
        # Drop helper columns but keep concept for now
        final_df = grouped_df.drop(
            columns=['group_order', 'representative_concept'],
            errors='ignore'
        )
        
        return final_df


class StatementProcessor:
    """
    Processor for extracting financial statements and returning as JSON/Dict.
    """
    
    def __init__(self, extractor: Optional[XBRLDataExtractor] = None):
        """
        Initialize the processor.
        
        Args:
            extractor: XBRLDataExtractor instance (creates default if None)
        """
        self.extractor = extractor or XBRLDataExtractor(min_periods=3)
    
    def get_financial_summary(
        self,
        ticker: str,
        form: str = "10-K"
    ) -> Dict[str, Any]:
        """
        Extract financial statements and return as JSON-compatible dictionary.
        
        Args:
            ticker: Stock ticker symbol
            form: Filing form type (10-K for annual, 10-Q for quarterly)
            
        Returns:
            Dictionary with 'financials', 'balanceSheet', and 'cashflow' keys
        """
        
        statements_config = [
            ("income_statement", "financials"),
            ("balance_sheet", "balanceSheet"),
            ("cashflow_statement", "cashflow")
        ]
        
        response_data = {}
        
        logger.info(f"Fetching financial summary for {ticker} using {form} filings...")
        
        for stmt_type, output_key in statements_config:
            try:
                
                # Extract DataFrame
                df = self.extractor.get_statements(
                    ticker,
                    form=form,
                    statement=stmt_type,
                    skip_amended=True,
                    limit= 10 if form == "10-K" else 20
                )
                
                if df is not None:
                    # Convert numeric columns, handle NaN/Inf
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    for col in numeric_cols:
                        df[col] = df[col].replace([np.inf, -np.inf], 0).fillna(0)
                    
                    # Convert to JSON-friendly format (list of dicts)
                    # Format: [{"label": "Revenue", "2023-12-31": 1000000, ...}, ...]
                    records = df.to_dict(orient='records')
                    
                    response_data[output_key] = records
                    logger.info(f"✓ Extracted {len(records)} rows for {output_key}")
                else:
                    response_data[output_key] = []
                    logger.warning(f"✗ No data for {stmt_type}")
                    
            except Exception as e:
                logger.error(f"✗ Error extracting {stmt_type}: {e}")
                response_data[output_key] = []
        
        return response_data

def test():
    """
    Test function to demonstrate usage.
    """
    
    # Test with a single ticker
    ticker = "NVDA"
    
    logger.info(f"\n{'#'*60}")
    logger.info(f"# Testing: {ticker}")
    logger.info(f"{'#'*60}\n")
    
    try:
        processor = StatementProcessor()
    
        # Get the 3 financial statements
        annual_data = processor.get_financial_summary(ticker, form="10-K")
        quarter_data = processor.get_financial_summary(ticker, form="10-Q")
        
        # Print JSON output
        print("\n" + "="*60)
        print("JSON OUTPUT:")
        print("="*60)
        print(json.dumps(annual_data, indent=2))
        print(json.dumps(quarter_data, indent=2))
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY:")
        print("="*60)
        print(f"Financials rows: {len(result.get('income_statement', []))}")
        print(f"Balance Sheet rows: {len(result.get('balance_sheet', []))}")
        print(f"Cash Flow rows: {len(result.get('cashflow', []))}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()

def get_financial_statement(ticker: str):
    processor = StatementProcessor()
    return {
        'annual': processor.get_financial_summary(ticker, form="10-K"), 
        'quarterly':processor.get_financial_summary(ticker, form="10-Q")
    }

def timed_financial_statement_api(ticker: str):
    
    TIMEOUT_SECONDS = 270
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_financial_statement, ticker)
        
        try:
            # Wait for the result with a timeout
            result = future.result(timeout=TIMEOUT_SECONDS)
            
            elapsed = time.time() - start_time
            logger.info(f"✓ Success! Completed in {elapsed:.2f} seconds")
            
            # Print simplified summary
            print("\nJSON Keys:", list(result.keys()))
            print(f"Financials Rows: {len(result.get('financials', []))}")
            
            return result
            
        except concurrent.futures.TimeoutError:
            elapsed = time.time() - start_time
            logger.error(f"✗ TIMEOUT EXCEEDED! Operation stopped after {elapsed:.2f} seconds.")
            
            return {
                'annual': [], 
                'quarterly':[]
            }

        except Exception as e:
            logger.error(f"✗ Error: {e}")
            
            return {
                'annual': [], 
                'quarterly':[]
            }