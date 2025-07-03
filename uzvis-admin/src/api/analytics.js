import axios from 'axios';

const BASE = '/api/analytics';

function buildParams(filters) {
  const {
    period,       // daily|weekly|monthly
    dateRange,    // 'YYYY-MM-DD,YYYY-MM-DD'
    status,       // order status filter
    paymentMethod,
    location,     // pincode filter
    groupBy,      // 'product' or 'category'
    category,     // category id or name
    product,      // product id or name
  } = filters;

  return {
    period,
    date_range: dateRange,
    status,
    payment_method: paymentMethod,
    location,
    group_by: groupBy,
    category,
    product,
  };
}

export async function fetchKpis(filters) {
  const params = buildParams(filters);
  const { data } = await axios.get(`${BASE}/kpis/`, { params });
  return data.data;
}

export async function fetchOrderCount(filters) {
  const params = buildParams(filters);
  const { data } = await axios.get(`${BASE}/order-count/`, { params });
  return data.data;
}

export async function fetchRevenue(filters) {
  const params = buildParams(filters);
  const { data } = await axios.get(`${BASE}/revenue/`, { params });
  return data.data;
}

// ← New fetch for the overall revenue module
export async function fetchRevenueDetails(filters) {
  const params = buildParams(filters);
  const { data } = await axios.get(`${BASE}/revenue-details/`, { params });
  return data.data;
}

export async function fetchPaymentMethods(filters) {
  const params = buildParams(filters);
  const { data } = await axios.get(`${BASE}/payment-methods/`, { params });
  return data.data;
}

export async function fetchStatusBreakdown(filters) {
  const params = buildParams(filters);
  const { data } = await axios.get(`${BASE}/status-breakdown/`, { params });
  return data.data;
}

export async function fetchOrderDateBounds() {
  try {
    const { data } = await axios.get(`${BASE}/order-date-range/`);
    return data;
  } catch (error) {
    console.error("Error fetching order date bounds:", error);
    throw error;
  }
}
