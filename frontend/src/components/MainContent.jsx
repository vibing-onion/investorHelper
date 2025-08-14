import React from 'react';
import Chart from './Chart';

function MainContent() {
  return (
    <div className="main">
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ marginTop: '2%' }}>investorHelper</h1>
        <p>Help you find the right picks.</p>
        <Chart />
      </div>
    </div>
  );
}

export default MainContent;