import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function ScoreBreakdown({ data }) {

  const defaultData = [
    { name: "Skills", value: 90 },
    { name: "Projects", value: 75 },
    { name: "Experience", value: 60 },
    { name: "Education", value: 80 },
    { name: "Certifications", value: 55 },
  ];

  const chartData = data || defaultData;

  return (
    <div className="glass-card p-8 h-[450px]">
      <h2 className="text-2xl font-bold mb-6">
        Score Breakdown
      </h2>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip cursor={{ fill: 'rgba(255, 255, 255, 0.1)' }} contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
          <Bar dataKey="value" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}