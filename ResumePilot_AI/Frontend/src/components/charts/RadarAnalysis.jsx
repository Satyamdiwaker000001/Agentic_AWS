import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";

export default function RadarAnalysis({ data }) {

  const defaultData = [
    { subject: "Skills", A: 90, fullMark: 100 },
    { subject: "Projects", A: 75, fullMark: 100 },
    { subject: "Experience", A: 60, fullMark: 100 },
    { subject: "Education", A: 80, fullMark: 100 },
    { subject: "Certifications", A: 55, fullMark: 100 },
  ];

  const chartData = data || defaultData;

  return (
    <div className="glass-card p-8 h-[450px]">
      <h2 className="text-2xl font-bold mb-6">
        Resume Strength Radar
      </h2>

      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={chartData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar
            name="Resume"
            dataKey="A"
            stroke="#60A5FA"
            fill="#60A5FA"
            fillOpacity={0.5}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}