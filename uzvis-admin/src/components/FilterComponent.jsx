import { useContext, useState } from 'react';
import { FilterContext } from '../context/FilterContext';

function FilterComponent({ onFilterChange }) {
  const { filters, setFilters } = useContext(FilterContext);
  const [tempFilters, setTempFilters] = useState(filters);

  const handleApply = () => {
    setFilters(tempFilters);
    onFilterChange(tempFilters);
  };

  return (
    <div className="bg-white p-4 rounded shadow mb-4">
      <h2 className="text-lg font-semibold mb-2">Filters</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <select
          value={tempFilters.period}
          onChange={(e) => setTempFilters({ ...tempFilters, period: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        <input
          type="text"
          placeholder="Date Range (YYYY-MM-DD,YYYY-MM-DD)"
          value={tempFilters.dateRange || ''}
          onChange={(e) => setTempFilters({ ...tempFilters, dateRange: e.target.value })}
          className="p-2 border rounded"
        />
        <select
          value={tempFilters.status}
          onChange={(e) => setTempFilters({ ...tempFilters, status: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
        </select>
        <select
          value={tempFilters.paymentMethod}
          onChange={(e) => setTempFilters({ ...tempFilters, paymentMethod: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="">All Payment Methods</option>
          <option value="upi">UPI</option>
          <option value="cod">Cash on Delivery</option>
        </select>
      </div>
      <button onClick={handleApply} className="mt-4 bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
        Apply Filters
      </button>
    </div>
  );
}

export default FilterComponent;