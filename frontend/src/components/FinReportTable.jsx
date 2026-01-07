import React, { useState, useEffect } from 'react';

const FinReportTable = ({ company, onBack }) => {
  const [activeTab, setActiveTab] = useState('financials'); // 'financials', 'balanceSheet', 'cashflow'
  const [periodType, setPeriodType] = useState('annual'); // 'annual' or 'quarterly'
  const [detailsData, setDetailsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!company) return;

    // Helper: Shortest Ticker
    const getShortestTicker = (tickerString) => {
      if (!tickerString) return '';
      const tickers = tickerString.toString().split(',').map(t => t.trim());
      tickers.sort((a, b) => a.length - b.length || a.localeCompare(b));
      return tickers[0];
    };

    const targetTicker = getShortestTicker(company.tickers);
    if (!targetTicker) {
      setError("No valid ticker found.");
      setLoading(false);
      return;
    }

    const fetchDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        // Calls your new timed API
        const response = await fetch(`http://localhost:5000/api/v1/companyInfo/${targetTicker}`);
        if (!response.ok) throw new Error('Fetch failed');
        
        const data = await response.json();
        setDetailsData(data); // Stores { annual: {...}, quarterly: {...} }
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [company]);

  // Helper to render a dynamic table from the JSON records
  const renderTable = (rows) => {
    if (!rows || rows.length === 0) {
      return <div className="text-center p-3 text-muted">No data available for this view.</div>;
    }

    // Get all unique keys from the first row to use as headers, excluding 'concept' if desired
    // Assuming keys are like: "label", "concept", "2023-12-31", "2022-12-31"...
    const allKeys = Object.keys(rows[0]);
    // Move 'label' to front, 'concept' to end or hide
    const dateKeys = allKeys.filter(k => k !== 'label' && k !== 'concept').sort().reverse(); // Sort dates descending
    const headers = ['Line Item', ...dateKeys];

    return (
      <div className="table-responsive">
        <table className="table table-sm table-hover table-striped">
          <thead className="table-light">
            <tr>
              {headers.map(h => <th key={h}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx}>
                <td className="fw-bold">{row.label}</td>
                {dateKeys.map(date => (
                  <td key={date}>
                    {/* Format numbers with commas */}
                    {typeof row[date] === 'number' 
                      ? row[date].toLocaleString() 
                      : row[date]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  // Get current dataset based on selection
  const currentData = detailsData ? detailsData[periodType] : null;

  if (!company) return null;

  return (
    <div className="container mt-4 animate-fade-in">
      
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
        <div>
          <h2 className="mb-0">{company.name}</h2>
          <span className="text-muted">{company.tickers} | {company.sicDescription}</span>
        </div>
        <button className="btn btn-outline-primary" onClick={onBack}>
          ← Search Again
        </button>
      </div>

      {loading && <div className="text-center py-5"><div className="spinner-border text-primary"></div></div>}
      
      {error && <div className="alert alert-danger">{error}</div>}

      {!loading && !error && currentData && (
        <>
          {/* Controls: Period Toggle */}
          <div className="d-flex justify-content-end mb-3">
            <div className="btn-group" role="group">
              <button 
                type="button" 
                className={`btn btn-sm ${periodType === 'annual' ? 'btn-primary' : 'btn-outline-primary'}`}
                onClick={() => setPeriodType('annual')}
              >
                Annual (10-K)
              </button>
              <button 
                type="button" 
                className={`btn btn-sm ${periodType === 'quarterly' ? 'btn-primary' : 'btn-outline-primary'}`}
                onClick={() => setPeriodType('quarterly')}
              >
                Quarterly (10-Q)
              </button>
            </div>
          </div>

          {/* Tabs */}
          <ul className="nav nav-tabs mb-3">
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'financials' ? 'active' : ''}`}
                onClick={() => setActiveTab('financials')}
              >
                Income Statement
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'balanceSheet' ? 'active' : ''}`}
                onClick={() => setActiveTab('balanceSheet')}
              >
                Balance Sheet
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'cashflow' ? 'active' : ''}`}
                onClick={() => setActiveTab('cashflow')}
              >
                Cash Flow
              </button>
            </li>
          </ul>

          {/* Content Area */}
          <div className="tab-content border p-3 bg-white shadow-sm rounded" style={{minHeight: '400px'}}>
            {activeTab === 'financials' && (
              <>
                <h5 className="mb-3 text-secondary">Consolidated Income Statement ({periodType})</h5>
                {renderTable(currentData.financials)}
              </>
            )}

            {activeTab === 'balanceSheet' && (
              <>
                <h5 className="mb-3 text-secondary">Consolidated Balance Sheet ({periodType})</h5>
                {renderTable(currentData.balanceSheet)}
              </>
            )}

            {activeTab === 'cashflow' && (
              <>
                <h5 className="mb-3 text-secondary">Consolidated Cash Flow ({periodType})</h5>
                {renderTable(currentData.cashflow)}
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default FinReportTable;