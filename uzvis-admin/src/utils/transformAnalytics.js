// src/utils/transformAnalytics.js

/**
 * Normalize order count/revenue API response for Recharts.
 * Converts ISO date strings into JS Date objects or formatted labels.
 */
export function transformPeriodData(rawData, dateKey = 'period', valueKey = 'count') {
  return rawData.map(item => ({
    date: new Date(item[dateKey]),
    value: item[valueKey],
  }));
}

/**
 * Normalize payment method data for a Recharts PieChart.
 * Ensures each entry has "name" and "value" keys.
 */
export function transformPieData(rawData, nameKey = 'payment_method', valueKey = 'count') {
  return rawData.map(item => ({
    name: item[nameKey],
    value: item[valueKey],
  }));
}

/**
 * Normalize status breakdown data for a Recharts PieChart or BarChart.
 * Assumes each object has 'status' and 'count' keys.
 */
export function transformStatusData(rawStatusData) {
  if (!Array.isArray(rawStatusData)) {
    console.error("transformStatusData: Expected an array of objects, but received:", rawStatusData);
    return [];
  }

  return rawStatusData.map(item => ({
    name: item.status,
    value: item.count,
  }));
}

/**
 * Normalize detailed revenue data grouped by product or category.
 * Input: [{ group, variant_name, total_quantity, price_per_unit, total_price }, ...]
 * Output: array suitable for bar/line charts or tables.
 */
export function transformRevenueDetailData(rawData) {
  if (!Array.isArray(rawData)) {
    console.error("transformRevenueDetailData: Expected an array of objects, but received:", rawData);
    return [];
  }

  return rawData.map(item => ({
    group: item.group,
    variant: item.variant_name,
    totalQuantity: item.total_quantity,
    pricePerUnit: item.price_per_unit,
    totalPrice: item.total_price,
  }));
}
