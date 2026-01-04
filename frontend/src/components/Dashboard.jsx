// Master component
import { useState, useEffect } from 'react';
import LineChart from './LineChart';
import '../index.css';

export default function Dashboard() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Global (shared) date range for all charts
  const [dateRange, setDateRange] = useState({ start: '', end: '' });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          'http://localhost:5000/api/v1/dashboardData/FRED/WALCL,WTREGEN,RRPONTSYD/True'
        );
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
      <div className="dataGroup" style={{textAlign: "center"}}>

        <h1>Dashboard</h1>

        {/* Global date panel */}
        <div className="dataGroup">
          <label>
            From:{' '}
            <input
              type="date"
              value={dateRange.start}
              onChange={(e) => setDateRange((p) => ({ ...p, start: e.target.value }))}
            />
          </label>
          <label>
          To:{' '}
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => setDateRange((p) => ({ ...p, end: e.target.value }))}
          />
        </label>
        </div>
      </div>
      <div className="dataGroup"><h2>Liquidity</h2></div>

      {loading && <p>Loading...</p>}

      <div className="gridBox">
        <div className="chart-cell">
          <LineChart chartId="WALCLChart" data={chartData?.WALCL} title="Fed Balance Sheet" unit="Millions"
            startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%"/>
        </div>

        <div className="chart-cell">
          <LineChart chartId="WTREGENChart" data={chartData?.WTREGEN} title="Treasury General Account" unit="Millions"
            startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%"/>
        </div>

        <div className="chart-cell">
          <LineChart chartId="RRPONTSYDChart" data={chartData?.RRPONTSYD} title="Overnight RRA" unit="Billions"
            startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%"/>
        </div>
      </div>
    </div>
  );
}