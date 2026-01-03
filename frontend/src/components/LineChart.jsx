import React, { useEffect, useRef } from 'react';
import CanvasJSReact from '@canvasjs/charts';

function LineChart({ chartId, data, title, unit, width = '60%', height = '50%' }) {
  const chartRef = useRef(null);

  useEffect(() => {
    // If no data, don't initialize chart
    if (!data || data.length === 0) {
      return;
    }

    try {
      // Initialize CanvasJS chart with passed data
      let d = JSON.parse(data);
      const transformedData = d.index.map((timestamp, i) => ({
        x: new Date(timestamp),
        y: d.data[i],
      })).filter(point => point.y !== null);
      console.log(transformedData);

      const chart = new CanvasJSReact.Chart(chartId, {
        animationEnabled: true,
        title: { text: `${title} (${unit})` || '' },
        axisY: {
          valueFormatString: '##.##',
        },
        data: [
          {
            indexLabelFontColor: "darkSlateGray",
            type: "area",
            yValueFormatString: "####.##",
            dataPoints: transformedData.slice(-1250, -1),
          },
        ]
      });

      chart.render();
      chartRef.current = chart;
    } catch (error) {
      console.error('Error initializing chart:', error);
    }

    // Cleanup if needed
    return () => {
      if (chartRef.current) {
        chartRef.current = null;
      }
    };
  }, [data, chartId, title]);

  // Render "no data available" message if data is not provided
  if (!data || data.length === 0) {
    return (
      <div
        id={chartId}
        style={{
          width,
          height,
          margin: 'auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#f5f5f5',
          borderRadius: '8px',
          color: '#999',
          fontSize: '16px',
        }}
      >
        No data available
      </div>
    );
  }

  return (
    <div
      id={chartId}
      style={{
        width,
        height,
        margin: 'auto',
      }}
    />
  );
}

export default LineChart;