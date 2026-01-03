import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DashboardPage from './pages/DashboardPage';
import CompanySector from './pages/CompanySector';
// import Financials from './pages/companyInfo';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          {/* <Route path="/company_info" element={<CompanyInfo />} /> */}
          <Route path="/company_sector" element={<CompanySector />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;