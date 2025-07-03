// src/App.jsx
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar.jsx';
import OrdersRevenue from './pages/OrdersRevenue.jsx';
import OverallRevenue from './pages/OverAllRevenue.jsx';

function App() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 p-6 overflow-auto">
        <Routes>
          <Route path="/orders" element={<OrdersRevenue />} />
          <Route path="/overall-revenue" element={<OverallRevenue />} />
          {/* default route */}
          <Route path="/" element={<OrdersRevenue />} />
          {/* fallback: redirect to orders if path not matched */}
          <Route path="*" element={<OrdersRevenue />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
