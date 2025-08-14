import React, { useEffect, Component } from 'react';
import CanvasJSReact from '@canvasjs/charts';
// import CanvasJSChart from './indexChart'; 

function Chart() {
  useEffect(() => {
    // Initialize CanvasJS chart
    const chart = new CanvasJSReact.Chart('indexChart', {
      title: { text: 'Sample Investor Chart' },
      data: [
        {
          type: 'line',
          dataPoints: [
            { x: new Date(2025, 0, 1), y: 450 },
            { x: new Date(2025, 1, 1), y: 414 },
            { x: new Date(2025, 2, 1), y: 520 },
            { x: new Date(2025, 3, 1), y: 460 },
            { x: new Date(2025, 4, 1), y: 450 },
          ],
        },
      ],
    });
    chart.render();

    // Optional: Fetch chart data from Flask
    fetch('http://backend:5000/api/chart-data')
      .then((response) => response.json())
      .then((data) => {
        chart.options.data[0].dataPoints = data.dataPoints;
        chart.render();
      })
      .catch((error) => console.error('Error fetching chart data:', error));
  }, []);

  return <div id="indexChart" style={{ width: '60%', height: '50%', margin: 'auto' }} />;
}

export default Chart;