// src/components/Sidebar.jsx
import { NavLink } from 'react-router-dom';

function Sidebar() {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-4">
      <h1 className="text-2xl font-bold mb-6">Uzvis Admin Panel</h1>
      <nav className="space-y-2">
        <NavLink
          to="/orders"
          className={({ isActive }) =>
            isActive
              ? 'block p-2 bg-gray-600 rounded'
              : 'block p-2 hover:bg-gray-600 rounded'
          }
        >
          Order and Revenue
        </NavLink>

        <NavLink
          to="/overall-revenue"
          className={({ isActive }) =>
            isActive
              ? 'block p-2 bg-gray-600 rounded'
              : 'block p-2 hover:bg-gray-600 rounded'
          }
        >
          Overall Revenue
        </NavLink>

        {/* Add other modules later */}
      </nav>
    </div>
  );
}

export default Sidebar;
