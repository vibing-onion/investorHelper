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
          'http://localhost:5000/api/v1/dashboardData/FRED/WALCL,WTREGEN,RRPONTSYD,TB3MS,T10YIE,PERMIT,UMCSENT,VIXCLS,FEDFUNDS,DGORDER,ICSA,A191RL1Q225SBEA,CPIAUCSL,INDPRO,TTLCON,UNRATE,TWEXBPA,PPIACO,PAYEMS/True'
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
          <LineChart 
            chartId="WALCLChart" 
            data={chartData?.WALCL} 
            title="Fed Balance Sheet (WALCL)" 
            unit="Millions"
            startDate={dateRange.start} 
            endDate={dateRange.end} 
            width="100%" 
            height="100%"
          />
        </div>
        <div className="chart-cell">
          <LineChart 
            chartId="WTREGENChart" 
            data={chartData?.WTREGEN} 
            title="Treasury General Account (WTREGEN)" 
            unit="Millions"
            startDate={dateRange.start} 
            endDate={dateRange.end} 
            width="100%" 
            height="100%"
          />
        </div>
        <div className="chart-cell">
          <LineChart 
            chartId="RRPONTSYDChart" 
            data={chartData?.RRPONTSYD} 
            title="Overnight RRP (RRPONTSYD)" 
            unit="Billions"
            startDate={dateRange.start} 
            endDate={dateRange.end} 
            width="100%" 
            height="100%"
          />
        </div>
      </div>

      {/* --- FORWARD INDICATORS --- */}
      <div className="dataGroup"><h2>Forward Indicators (Leading)</h2></div>
      <div className="gridBox">
        <div className="chart-cell">
          <LineChart chartId="TB3MSChart" data={chartData?.TB3MS} title="3-Month Treasury Rate (TB3MS)" unit="%" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="T10YIEChart" data={chartData?.T10YIE} title="10-Year Breakeven Inflation (T10YIE)" unit="%" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="PERMITChart" data={chartData?.PERMIT} title="Building Permits (PERMIT)" unit="Units" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="UMCSENTChart" data={chartData?.UMCSENT} title="Consumer Sentiment (UMCSENT)" unit="Index" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="VIXCLSChart" data={chartData?.VIXCLS} title="CBOE Volatility Index (VIX)" unit="Index" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="FEDFUNDSChart" data={chartData?.FEDFUNDS} title="Federal Funds Rate (FEDFUNDS)" unit="%" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="DGORDERChart" data={chartData?.DGORDER} title="Durable Goods Orders (DGORDER)" unit="Millions" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="ICSAChart" data={chartData?.ICSA} title="Initial Jobless Claims (ICSA)" unit="Units" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
      </div>

      {/* --- BACKWARD INDICATORS --- */}
      <div className="dataGroup"><h2>Backward Indicators (Lagging)</h2></div>
      <div className="gridBox">
        <div className="chart-cell">
          <LineChart chartId="GDPChart" data={chartData?.A191RL1Q225SBEA} title="Real GDP Growth (Quarterly)" unit="%" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="CPIChart" data={chartData?.CPIAUCSL} title="CPI - All Urban Consumers" unit="Index" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="INDPROChart" data={chartData?.INDPRO} title="Industrial Production Index" unit="Index" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="TTLCONChart" data={chartData?.TTLCON} title="Total Construction Spending" unit="Millions" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="UNRATEChart" data={chartData?.UNRATE} title="Unemployment Rate" unit="%" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="TWEXBPAChart" data={chartData?.TWEXBPA} title="Dollar Index (Trade Weighted)" unit="Index" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="PPIChart" data={chartData?.PPIACO} title="PPI - All Commodities" unit="Index" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
        <div className="chart-cell">
          <LineChart chartId="PAYEMSChart" data={chartData?.PAYEMS} title="Non-Farm Payrolls" unit="Thousands" startDate={dateRange.start} endDate={dateRange.end} width="100%" height="100%" />
        </div>
      </div>

    </div>
  );
}