import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar.jsx';
import OrdersRevenue from './pages/OrdersRevenue.jsx';

function App() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 p-6 overflow-auto">
        <Routes>
          <Route path="/orders" element={<OrdersRevenue />} />
          <Route path="/" element={<OrdersRevenue />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
