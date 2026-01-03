// Master component
import { useState, useEffect } from 'react';
import LineChart from './LineChart';

export default function Dashboard() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/v1/dashboardData/FRED/T10YIE,WTREGEN,RRPONTSYD/True');
        const data = await response.json();
        setChartData(data);
      } catch (error) {
        console.error('Failed to fetch:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Pass data to chart - it handles null gracefully */}
      {/* <LineChart data={chartData?.WALCL} title="Fed Balance Sheet" /> */}
      <LineChart chartId={"T10YIEChart"} data={chartData?.T10YIE} title="10 Year Treasury Yield" unit="%" id = "T10YIEChart"/>
      <LineChart chartId={"WTREGENChart"} data={chartData?.WTREGEN} title="Treasury General Account: Week Average Closing Balance" unit="Millions of USD" id = "WTREGENChart"/>
      <LineChart chartId={"RRPONTSYDChart"} data={chartData?.RRPONTSYD} title="Overnight Reverse Repurchase Agreements" unit="Billions of USD" id = "RRPONTSYDChart"/>
    </div>
  );
}