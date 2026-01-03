import React from 'react';
import HomePageChart from './HomePageChart';

function MainContent() {
  return (
    <div className="main">
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ marginTop: '2%' }}>investorHelper</h1>
        <p>Help you find the right picks.</p>
        <HomePageChart />
      </div>
    </div>
  );
}

export default MainContent;