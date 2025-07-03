import { Bar, Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Tooltip, Legend);

function ChartComponent({ type, data, options }) {
  const ChartType = type === 'bar' ? Bar : type === 'line' ? Line : Pie;
  return (
    <div className="bg-white p-4 rounded shadow">
      <ChartType data={data} options={options} />
    </div>
  );
}

export default ChartComponent;