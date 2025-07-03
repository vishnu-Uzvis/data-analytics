import { useState, useEffect, useContext } from 'react';
import {
  fetchKpis,
  fetchOrderCount,
  fetchRevenue,
  fetchPaymentMethods,
  fetchStatusBreakdown
} from '../api/analytics';
import FilterComponent from '../components/FilterComponent.jsx';
import KpiTile from '../components/KpiTile.jsx';
import TableComponent from '../components/TableComponent.jsx';
import { FilterContext } from '../context/FilterContext';
// Import the new transform functions
import {
  transformPeriodData,
  transformPieData,
  transformStatusData
} from '../utils/transformAnalytics';


// Recharts imports
import {
  ResponsiveContainer,
  BarChart, Bar,
  LineChart, Line,
  PieChart, Pie,
  XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, Cell
} from 'recharts';

export default function OrdersRevenue() {
  const { filters } = useContext(FilterContext);

  const [kpis, setKpis] = useState({});
  const [orderCount, setOrderCount] = useState([]);
  const [revenue, setRevenue] = useState([]);
  const [payments, setPayments] = useState([]);
  const [statusBreakdown, setStatusBreakdown] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Turn ISO dates into human-friendly labels
  const normalizeTimeSeries = (arr, key) =>
    arr.map(item => ({
      periodLabel: new Date(item.period).toLocaleDateString(undefined, {
        month: 'short', day: 'numeric'
      }),
      value: item[key],
    }));

  // Map objects for pie charts
  const normalizePie = (arr, nameKey, valueKey) =>
    arr.map(item => ({ name: item[nameKey], value: item[valueKey] }));

  useEffect(() => {
    async function loadAll() {
      setLoading(true);
      setError(null);
      try {
        const [
          kpiData,
          countData,
          revData,
          payData,
          rawStatusBreakdownData // This is the data from fetchStatusBreakdown
        ] = await Promise.all([
          fetchKpis(filters),
          fetchOrderCount(filters),
          fetchRevenue(filters),
          fetchPaymentMethods(filters),
          fetchStatusBreakdown(filters),
        ]);

        // This log will now show what's directly returned by fetchStatusBreakdown
        // and passed to transformStatusData. This is your primary debugging point for the raw data.
        console.log("DEBUG: rawStatusBreakdownData from API (passed to transformStatusData):", rawStatusBreakdownData);

        setKpis(kpiData);
        setOrderCount(normalizeTimeSeries(countData, 'count'));
        setRevenue(normalizeTimeSeries(revData, 'revenue'));
        setPayments(normalizePie(payData, 'payment_method', 'count'));

        // Use the transformStatusData function to process the raw data
        const transformedStatusData = transformStatusData(rawStatusBreakdownData);
        setStatusBreakdown(transformedStatusData);
        console.log("DEBUG: Final Transformed Status Breakdown for Table:", transformedStatusData); // Log the result

      } catch (e) {
        console.error("CRITICAL ERROR in loadAll function:", e.response?.data?.error || e.message || 'Failed to fetch analytics', e);
        setError(e.response?.data?.error || e.message || 'Failed to fetch analytics');
      } finally {
        setLoading(false);
      }
    }

    loadAll();
  }, [filters]);

  const pieColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042'];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Order & Revenue Analytics</h1>
      <FilterComponent onFilterChange={() => {}} />

      {loading && <p>Loading…</p>}
      {error && <p className="text-red-500">{error}</p>}

      {/* KPI Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <KpiTile title="Total Orders" value={kpis.total_orders || 0} />
        {/* Changed $ to ₹ for Net Revenue */}
        <KpiTile title="Net Revenue" value={`₹${(kpis.net_revenue || 0).toFixed(2)}`} />
        {/* Changed $ to ₹ for Avg Order Value */}
        <KpiTile title="Avg Order Value" value={`₹${(kpis.avg_order_value || 0).toFixed(2)}`} />
        <KpiTile title="Cancelled %" value={`${(kpis.cancellation_rate || 0).toFixed(2)}%`} />
        <KpiTile title="Avg Orders / Day" value={kpis.avg_orders_per_period || 0} />
      </div>

      {/* Order Count */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Order Count</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={orderCount}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="periodLabel" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" name="Orders" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Revenue */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Revenue</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={revenue}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="periodLabel" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" name="Revenue" stroke="#82ca9d" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Payment Methods */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Orders by Payment Method</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={payments}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              outerRadius={100}
              label
            >
              {payments.map((_, i) => (
                <Cell key={i} fill={pieColors[i % pieColors.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Status Breakdown */}
      <div>
        <h2 className="text-lg font-semibold mb-2">Order Status Breakdown</h2>
        <TableComponent
          data={statusBreakdown}
          columns={[
            { key: 'name', label: 'Status' },
            { key: 'value', label: 'Count' },
          ]}
        />
      </div>
    </div>
  );
}