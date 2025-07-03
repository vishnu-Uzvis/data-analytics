// src/components/KpiTile.jsx
function KpiTile({ title, value, icon }) {
  return (
    <div className="bg-white p-4 rounded shadow flex items-center">
      {icon && <span className="mr-2 text-2xl">{icon}</span>}
      <div>
       <h3 className="text-sm text-black">{title}</h3>
        <p className="text-lg font-semibold text-black">{value}</p>
      </div>
    </div>
  );
}

export default KpiTile;