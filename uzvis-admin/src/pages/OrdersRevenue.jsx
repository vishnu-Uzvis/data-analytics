// src/pages/OrdersRevenue.jsx
import { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import FilterComponent from '../components/FilterComponent.jsx';
import KpiTile from '../components/KpiTile.jsx';
import ChartComponent from '../components/ChartComponent.jsx';
import TableComponent from '../components/TableComponent.jsx';
import { FilterContext } from '../context/FilterContext';

function OrdersRevenue() {
  const { filters } = useContext(FilterContext);
  const [kpiData, setKpiData] = useState({});
  const [orderCountData, setOrderCountData] = useState([]);
  const [revenueData, setRevenueData] = useState([]);
  const [paymentMethodData, setPaymentMethodData] = useState([]);
  const [statusBreakdownData, setStatusBreakdownData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async (filters) => {
    setLoading(true);
    setError(null);
    try {
      const baseUrl = 'http://localhost:8000/api/analytics';
      const params = {
        module: 'orders',
        period: filters.period,
        date_range: filters.dateRange,
        status: filters.status,
        payment_method: filters.paymentMethod,
        location: filters.location,
      };

      // Fetch KPIs
      const kpiResponse = await axios.get(`${baseUrl}?type=kpis`, { params });
      setKpiData(kpiResponse.data.data);

      // Fetch Order Count
      const countResponse = await axios.get(`${baseUrl}?type=count`, { params });
      setOrderCountData(countResponse.data.data);

      // Fetch Revenue
      const revenueResponse = await axios.get(`${baseUrl}?type=revenue`, { params });
      setRevenueData(revenueResponse.data.data);

      // Fetch Payment Methods
      const paymentResponse = await axios.get(`${baseUrl}?type=payment_method`, { params });
      setPaymentMethodData(paymentResponse.data.data);

      // Fetch Status Breakdown
      const statusResponse = await axios.get(`${baseUrl}?type=status_breakdown`, { params });
      setStatusBreakdownData(statusResponse.data.data);
    } catch (err) {
      // Use 'err' to enhance error handling
      console.error('Error fetching data:', err.message);
      setError(err.response?.data?.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(filters);
  }, [filters]);

  const orderCountChartData = {
    labels: orderCountData.map((item) => item.period),
    datasets: [
      {
        label: 'Order Count',
        data: orderCountData.map((item) => item.count),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const revenueChartData = {
    labels: revenueData.map((item) => item.period),
    datasets: [
      {
        label: 'Revenue',
        data: revenueData.map((item) => item.revenue),
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  const paymentMethodChartData = {
    labels: paymentMethodData.map((item) => item.method),
    datasets: [
      {
        data: paymentMethodData.map((item) => item.count),
        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const tableColumns = [
    { key: 'order_id', label: 'Order ID' },
    { key: 'date', label: 'Order Date' },
    { key: 'delivery_date', label: 'Delivery Date' },
    { key: 'payment_method', label: 'Payment Method' },
    { key: 'status', label: 'Status' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Order and Revenue</h1>
      <FilterComponent onFilterChange={fetchData} />
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <KpiTile title="Total Orders" value={kpiData.total_orders || 0} />
        <KpiTile title="Net Revenue" value={`$${kpiData.net_revenue || 0}`} />
        <KpiTile title="Avg Order Value" value={`$${kpiData.avg_order_value || 0}`} />
        <KpiTile title="Cancellation Rate" value={`${kpiData.cancellation_rate || 0}%`} />
        <KpiTile title="Avg Orders/Period" value={kpiData.avg_orders_per_period || 0} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <h2 className="text-lg font-semibold mb-2">Order Count</h2>
          <ChartComponent type="bar" data={orderCountChartData} options={chartOptions} />
        </div>
        <div>
          <h2 className="text-lg font-semibold mb-2">Revenue</h2>
          <ChartComponent type="line" data={revenueChartData} options={chartOptions} />
        </div>
      </div>
      <div className="mb-4">
        <h2 className="text-lg font-semibold mb-2">Orders by Payment Method</h2>
        <ChartComponent type="pie" data={paymentMethodChartData} options={{}} />
      </div>
      <div>
        <h2 className="text-lg font-semibold mb-2">Order Status Breakdown</h2>
        <TableComponent data={statusBreakdownData} columns={tableColumns} />
      </div>
    </div>
  );
}

export default OrdersRevenue;