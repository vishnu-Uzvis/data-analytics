function TableComponent({ data, columns }) {
  return (
    <div className="bg-white p-4 rounded shadow overflow-x-auto text-black">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="border p-2 text-left">{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.isArray(data) && data.length > 0 ? (
            data.map((row, index) => (
              <tr key={index}>
                {columns.map((col) => (
                  <td key={col.key} className="border p-2">{row[col.key]}</td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={columns.length} className="border p-2 text-center">
                No data available
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default TableComponent;