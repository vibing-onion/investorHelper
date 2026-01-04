import React, { useEffect, useRef } from 'react';
import CanvasJSReact from '@canvasjs/charts';

function LineChart({ 
  chartId, 
  data, 
  title, 
  unit, 
  startDate, 
  endDate,  
  width = '100%', 
  height = '100%' 
}) {
  const chartRef = useRef(null);

  useEffect(() => {
    // 1. Basic validation
    if (!data || data.length === 0) return;

    // 2. Parse data if it's a JSON string, or use directly if array
    let allData = [];
    if (typeof data === 'string') {
      const d = JSON.parse(data);
      allData = d.index.map((timestamp, i) => ({
        x: new Date(timestamp),
        y: d.data[i],
      })).filter(pt => pt.y !== null);
    } else {
      allData = data;
    }

    // 3. Filter based on Parent's Date Props
    // If no date is selected yet (initial load), show everything or default range
    let filteredData = allData;
    if (startDate && endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      end.setHours(23, 59, 59); // Include full end day

      filteredData = allData.filter(pt => pt.x >= start && pt.x <= end);
    }

    // 4. Render Chart
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const chart = new CanvasJSReact.Chart(chartId, {
      animationEnabled: true,
      theme: "light2",
      title: { text: title ? `${title} (${unit})` : '' , fontSize: 24},
      axisX: { valueFormatString: "DD MMM YY" },
      data: [{
        type: "area",
        xValueFormatString: "DD MMM YYYY",
        dataPoints: filteredData
      }]
    });

    chart.render();
    chartRef.current = chart;

    return () => {
      if (chartRef.current) chartRef.current.destroy();
    };
  }, [data, chartId, startDate, endDate]); // Re-render when dates change

  return <div id={chartId} style={{ width, height }} />;
}

export default LineChart;
