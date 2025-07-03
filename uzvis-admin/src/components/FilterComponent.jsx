import { useContext, useState, useEffect } from 'react';
import { FilterContext } from '../context/FilterContext';
import 'react-date-range/dist/styles.css'; // still imported if needed for bounds
import 'react-date-range/dist/theme/default.css';
import {
  addDays,
  format
} from 'date-fns';
import { fetchOrderDateBounds } from '../api/analytics';

function FilterComponent({ onFilterChange }) {
  const { filters, setFilters } = useContext(FilterContext);
  const [tempFilters, setTempFilters] = useState(filters);

  // Default date selection for clearing
  const defaultDateSelection = {
    startDate: new Date(),
    endDate: new Date(),
  };

  // Manual date inputs state
  const [dateSelection, setDateSelection] = useState(
    filters.dateRange
      ? {
          startDate: new Date(filters.dateRange.split(',')[0]),
          endDate:   new Date(filters.dateRange.split(',')[1]),
        }
      : defaultDateSelection
  );

  // Display string
  const initialDisplayRange = filters.dateRange
    ? `RANGE - ${format(new Date(filters.dateRange.split(',')[0]), 'dd-MMM-yyyy').toUpperCase()} TO ${format(new Date(filters.dateRange.split(',')[1]), 'dd-MMM-yyyy').toUpperCase()}`
    : 'No date range selected';
  const [displayedDateRange, setDisplayedDateRange] = useState(initialDisplayRange);

  // Min/max from API
  const [minMaxOrderDates, setMinMaxOrderDates] = useState({ min: null, max: null });
  const [loadingDateBounds, setLoadingDateBounds] = useState(true);

  useEffect(() => {
    async function loadDateBounds() {
      try {
        setLoadingDateBounds(true);
        const bounds = await fetchOrderDateBounds();
        setMinMaxOrderDates({
          min: bounds.min_order_date ? new Date(bounds.min_order_date) : null,
          max: bounds.max_order_date ? new Date(bounds.max_order_date) : null,
        });
      } catch (e) {
        console.error('Failed to fetch order date bounds:', e);
        setMinMaxOrderDates({ min: null, max: null });
      } finally {
        setLoadingDateBounds(false);
      }
    }
    loadDateBounds();
  }, []);

  // Sync tempFilters.dateRange on manual input change
  useEffect(() => {
    const { startDate, endDate } = dateSelection;
    if (startDate && endDate) {
      const s = format(startDate, 'yyyy-MM-dd');
      const e = format(endDate, 'yyyy-MM-dd');
      setTempFilters(f => ({ ...f, dateRange: `${s},${e}` }));
    } else {
      setTempFilters(f => ({ ...f, dateRange: '' }));
    }
  }, [dateSelection]);

  const updateDisplayedDateRange = (startDate, endDate) => {
    if (startDate && endDate) {
      const a = format(startDate, 'dd-MMM-yyyy').toUpperCase();
      const b = format(endDate, 'dd-MMM-yyyy').toUpperCase();
      setDisplayedDateRange(`RANGE - ${a} TO ${b}`);
    } else {
      setDisplayedDateRange('No date range selected');
    }
  };

  const handleMainApply = () => {
    setFilters(tempFilters);
    onFilterChange(tempFilters);
    updateDisplayedDateRange(dateSelection.startDate, dateSelection.endDate);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    const dateObj = value ? new Date(value) : null;
    setDateSelection(sel => ({
      ...sel,
      [name]: dateObj
    }));
  };

  return (
    <div className="bg-white p-4 rounded shadow mb-4">
      <h2 className="text-lg font-semibold mb-2">Filters</h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Period */}
        <select
          value={tempFilters.period}
          onChange={e => setTempFilters({ ...tempFilters, period: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>

        {/* Manual Date Inputs (no calendar button) */}
        <div className="flex space-x-2">
          <input
            type="date"
            name="startDate"
            value={format(dateSelection.startDate, 'yyyy-MM-dd')}
            onChange={handleInputChange}
            className="p-2 border rounded"
            min={minMaxOrderDates.min ? format(minMaxOrderDates.min, 'yyyy-MM-dd') : undefined}
            max={minMaxOrderDates.max ? format(minMaxOrderDates.max, 'yyyy-MM-dd') : undefined}
            disabled={loadingDateBounds}
          />
          <input
            type="date"
            name="endDate"
            value={format(dateSelection.endDate, 'yyyy-MM-dd')}
            onChange={handleInputChange}
            className="p-2 border rounded"
            min={minMaxOrderDates.min ? format(minMaxOrderDates.min, 'yyyy-MM-dd') : undefined}
            max={minMaxOrderDates.max ? format(minMaxOrderDates.max, 'yyyy-MM-dd') : undefined}
            disabled={loadingDateBounds}
          />
        </div>

        {/* Status */}

        {/* Uncomment to add status filter back */}
        {/* <select
          value={tempFilters.status}
          onChange={e => setTempFilters({ ...tempFilters, status: e.target.value })}
          className="p-3 border rounded"
        >
          <option value="">All Statuses</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
        </select> */}

        {/* Payment Method */}
        <select
          value={tempFilters.paymentMethod}
          onChange={e => setTempFilters({ ...tempFilters, paymentMethod: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="">All Payment Methods</option>
          <option value="upi">UPI</option>
          <option value="cod">Cash on Delivery</option>
          <option value="wallet">Wallet</option>
        </select>
      </div>

      <div className="mt-2 text-sm text-gray-700">{displayedDateRange}</div>

      <button
        onClick={handleMainApply}
        className="mt-4 bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
      >
        Apply Filters
      </button>
    </div>
  );
}

export default FilterComponent;
