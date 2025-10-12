import React, { useEffect, useState } from 'react';

const CompanyList = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) return <div className="text-center">Loading...</div>;
  if (error) return <div className="text-danger text-center">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Companies</h2>
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
          {companies.map((company) => (
            <tr key={company.cik}>
              <td><a href={`/company/${company.cik}`}>{company.name}</a></td>
              <td>{company.tickers}</td>
              <td>{company.cik}</td>
              <td>{company.sic}</td>
              <td>{company.sicDescription}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CompanyList;