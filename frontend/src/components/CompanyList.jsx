import React, { useEffect, useState } from 'react';

// 1. ACCEPT THE PROP HERE
const CompanyList = ({ onSelectCompany }) => { 
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/v1/companySectorList`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setCompanies(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredCompanies = companies.filter((company) => {
    const term = searchTerm.toLowerCase().trim();
    if (!term) return true;
    const name = (company.name || '').toLowerCase();
    const ticker = (company.tickers || '').toLowerCase();
    const cik = (company.cik || '').toString();
    const sicCode = (company.sic || '').toString();
    const sicDesc = (company.sicDescription || '').toLowerCase();
    return (
      name.includes(term) ||
      ticker.includes(term) ||
      cik.includes(term) ||
      sicCode.includes(term) ||
      sicDesc.includes(term)
    );
  });

  if (loading) return <div className="text-center mt-5">Loading...</div>;
  if (error) return <div className="text-danger text-center mt-5">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Companies</h2>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Search strictly by Name, Ticker, CIK, or Sector..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <small className="text-muted">
          Showing {filteredCompanies.length} result{filteredCompanies.length !== 1 && 's'}
        </small>
      </div>

      <table className="table table-striped table-hover">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Ticker</th>
            <th>CIK</th>
            <th>Sector Code</th>
            <th>Sector Description</th>
          </tr>
        </thead>
        <tbody>
          {filteredCompanies.length > 0 ? (
            filteredCompanies.map((company, index) => (
              <tr key={`${company.cik}-${index}`}>
                <td>
                  {/* 2. CHANGE LINK TO BUTTON/CLICK HANDLER */}
                  <button 
                    className="btn btn-link p-0 text-start text-decoration-none fw-bold"
                    onClick={() => {
                      // Call the prop if it exists
                      if (onSelectCompany) {
                        onSelectCompany(company);
                      }
                    }}
                  >
                    {company.name}
                  </button>
                </td>
                <td>{company.tickers}</td>
                <td>{company.cik}</td>
                <td>{company.sic}</td>
                <td>{company.sicDescription}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" className="text-center text-muted">
                No companies found matching "{searchTerm}"
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default CompanyList;
