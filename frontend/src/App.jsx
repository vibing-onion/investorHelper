import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import CompanySector from './pages/companySector';
// import Financials from './pages/companyInfo';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          {/* <Route path="/company_info" element={<CompanyInfo />} /> */}
          <Route path="/company_sector" element={<CompanySector />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;