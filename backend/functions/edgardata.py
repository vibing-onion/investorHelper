import pandas as pd
import numpy as np
import duckdb
from edgar import *
from edgar.xbrl import *

set_identity("abc@gmail.com")

def getStatements(ticker, form = "10-K", statement = "income_statement"):
    
    # Step 1: Get all the dataframes for the corresponding statement
    # Create a list to store the dataframes
    company = Company(ticker)
    df_list = []
    for report in list(company.get_filings(form = form))[:]:
        xbrl = XBRL.from_filing(report)
        if statement == "income_statement":
            content = xbrl.statements.income_statement()
        elif statement == "balance_sheet":
            content = xbrl.statements.balance_sheet()
        else:
            content = xbrl.statements.cashflow_statement()
        data = content.render().to_dataframe()
        data = data[data.columns[0:3]]
        df_list.append(data)
    
    # Step 2: Merge the dataframes
    reference_order = df_list[0][['concept', 'label']].copy()
    reference_order['order'] = range(len(reference_order))
    
    label_groups = reference_order.groupby('label').agg({'order': 'min', 'concept': 'first'}).reset_index()
    label_groups = label_groups.rename(columns={'order': 'group_order', 'concept': 'representative_concept'})
    
    date_columns = [d.columns[-1] for d in df_list]
    merged_df = df_list[0].copy()
    for i, df in enumerate(df_list[1:], 1):
        merged_df = pd.merge(
            merged_df,
            df,
            on=['concept', 'label'],
            how='outer'
        )
    for col in date_columns:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
    agg_dict = {col: 'sum' for col in date_columns}
    agg_dict['concept'] = 'first'
    grouped_df = merged_df.groupby('label').agg(agg_dict).reset_index()
    grouped_df = pd.merge(
        grouped_df,
        label_groups[['label', 'group_order', 'representative_concept']],
        on='label',
        how='left'
    )
    max_group_order = grouped_df['group_order'].max() if pd.notna(grouped_df['group_order']).any() else 0
    for idx, row in grouped_df[grouped_df['group_order'].isna()].iterrows():
        grouped_df.loc[idx, 'group_order'] = max_group_order + 1
        max_group_order += 1

    grouped_df['concept'] = grouped_df.apply(
        lambda row: row['representative_concept'] if pd.notna(row['representative_concept']) else row['concept'],
        axis=1
    )
    grouped_df = grouped_df.sort_values('group_order')
    grouped_df = grouped_df.reset_index(drop=True)

    for col in date_columns:
        grouped_df[col] = grouped_df[col].apply(lambda x: '' if pd.isna(x) else x)
    
    grouped_df = grouped_df.drop(columns=['group_order', 'representative_concept','concept']).fillna(0)
    # grouped_df.to_csv(f'./{ticker}_{statement}.csv', index=False)
    return grouped_df

def getSampleStatements(ticker, form = "10-K", statement = "income_statement"):
    df = pd.read_csv(f'./{ticker}_{statement}.csv')
    return df