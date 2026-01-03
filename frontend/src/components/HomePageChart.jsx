import React, { useEffect, Component } from 'react';
import CanvasJSReact from '@canvasjs/charts';

function HomePageChart() {
  useEffect(() => {
    // Initialize CanvasJS chart
    const chart = new CanvasJSReact.Chart('indexChart', {
      animationEnabled: true,
      title: { text: '' },
      axisY:{
        valueFormatString: "##.##%",
      },
      data: [
        {
          indexLabelFontColor: "darkSlateGray",
          type: "area",
          yValueFormatString: "####.##%",
          dataPoints: [
            { x: new Date(2025, 0, 1), y: 450 },
            { x: new Date(2025, 1, 1), y: 414 },
            { x: new Date(2025, 2, 1), y: 520 },
            { x: new Date(2025, 3, 1), y: 460 },
            { x: new Date(2025, 4, 1), y: 450 },
          ],
        },
        {
          indexLabelFontColor: "darkSlateGray",
          type: "area",
          yValueFormatString: "####.##%",
          dataPoints: [
            { x: new Date(2025, 0, 1), y: 453 },
            { x: new Date(2025, 1, 1), y: 410 },
            { x: new Date(2025, 2, 1), y: 524 },
            { x: new Date(2025, 3, 1), y: 468 },
            { x: new Date(2025, 4, 1), y: 452 },
          ],
        },
      ],
    });
    chart.render();

    // Optional: Fetch chart data from Flask
    fetch('http://localhost:5000/api/v1/sampleData')
      .then((response) => response.json())
      .then(d => {
        // console.log(d)
        let costco = [], spx = []
        d.forEach(e => {
          costco.push({
                x: new Date(e[e.length-1]),
                y: e[1]
            })
            spx.push({
                x: new Date(e[e.length-1]),
                y: e[0]
            })
        })
        chart.options.data[0].dataPoints = costco
        chart.options.data[1].dataPoints = spx
        chart.render()
      })
      .catch((error) => console.error('Error fetching chart data:', error));
  }, []);

  return <div id="indexChart" style={{ width: '60%', height: '50%', margin: 'auto' }} />;
}

export default HomePageChart;