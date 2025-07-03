// src/pages/OverallRevenue.jsx
import { useState, useEffect, useContext } from 'react';
import {
  fetchKpis,              // you can drop this if you don’t need any generic KPIs
  fetchRevenueDetails,
} from '../api/analytics';
import FilterComponent from '../components/FilterComponent.jsx';
import KpiTile from '../components/KpiTile.jsx';
import TableComponent from '../components/TableComponent.jsx';
import { FilterContext } from '../context/FilterContext';
import { transformRevenueDetailData } from '../utils/transformAnalytics';

import {
  ResponsiveContainer,
  BarChart, Bar,
  LineChart, Line,
  XAxis, YAxis, CartesianGrid,
  Tooltip, Legend,
} from 'recharts';

export default function OverallRevenue() {
  const { filters } = useContext(FilterContext);

  const [details, setDetails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Summary KPI calculations
  const numberOfProducts = details.length;
  const totalQuantity     = details.reduce((sum, d) => sum + d.totalQuantity, 0);
  const totalRevenue      = details.reduce((sum, d) => sum + d.totalPrice, 0);
  const avgPricePerUnit   = totalQuantity > 0
    ? (totalRevenue / totalQuantity).toFixed(2)
    : 0;

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const raw = await fetchRevenueDetails(filters);
        const transformed = transformRevenueDetailData(raw);
        setDetails(transformed);
      } catch (e) {
        console.error("Failed to load revenue details:", e);
        setError(e.message || 'Error fetching data');
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [filters]);

  // pick a couple of chart colors
  const COLORS = ['#8884d8', '#82ca9d', '#ffc658'];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Overall Revenue Analytics</h1>
      <FilterComponent onFilterChange={() => {}} />

      {loading && <p>Loading…</p>}
      {error   && <p className="text-red-500">{error}</p>}

      {/* KPI Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <KpiTile title="Products Tracked"   value={numberOfProducts} />
        <KpiTile title="Total Quantity Sold" value={totalQuantity} />
        <KpiTile title="Avg. Price / Unit"   value={`₹${avgPricePerUnit}`} />
        <KpiTile title="Total Revenue"       value={`₹${totalRevenue.toFixed(2)}`} />
      </div>

      {/* Bar chart of total revenue per variant */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Revenue by Variant (Bar)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={details}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="variant" />
            <YAxis />
            <Tooltip formatter={value => `₹${value}`} />
            <Legend />
            <Bar dataKey="totalPrice" name="Total Revenue" fill={COLORS[0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Line chart of total revenue per variant */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Revenue by Variant (Line)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={details}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="variant" />
            <YAxis />
            <Tooltip formatter={value => `₹${value}`} />
            <Legend />
            <Line
              type="monotone"
              dataKey="totalPrice"
              name="Total Revenue"
              stroke={COLORS[1]}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Details table */}
      <div>
        <h2 className="text-lg font-semibold mb-2">Revenue Detail Table</h2>
        <TableComponent
          data={details}
          columns={[
            { key: 'group',         label: 'Group' },
            { key: 'variant',       label: 'Variant' },
            { key: 'totalQuantity', label: 'Quantity Sold' },
            { key: 'pricePerUnit',  label: 'Price / Unit' },
            { key: 'totalPrice',    label: 'Total Price' },
          ]}
        />
      </div>
    </div>
  );
}
