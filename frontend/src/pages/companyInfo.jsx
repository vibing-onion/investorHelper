import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import CompanyList from '../components/CompanyList';
import FinReportTable from '../components/FinReportTable';

function CompanyInfo() {
  const [selectedCompany, setSelectedCompany] = useState(null);

  // Handler to go back to search
  const handleReset = () => {
    setSelectedCompany(null);
  };

  return (
    <div>
      <Navbar />
      
      {/* Conditional Rendering */}
      {!selectedCompany ? (
        // SHOW LIST: Pass a handler to catch the click
        <CompanyList onSelectCompany={(company) => setSelectedCompany(company)} />
      ) : (
        // SHOW DETAILS: Pass the company data and the reset handler
        <FinReportTable 
          company={selectedCompany} 
          onBack={handleReset} 
        />
      )}
      
    </div>
  );
}

export default CompanyInfo;
