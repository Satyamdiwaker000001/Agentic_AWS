export default function RoleMatchCard({ roleMatch }) {

  const title = roleMatch?.title || "Backend Engineer";
  const percentage = roleMatch?.matchPercentage || 91;

  return (
    <div className="glass-card p-8 flex flex-col justify-center">
      <h2 className="text-xl font-bold mb-5 text-slate-300">
        Best Matching Role
      </h2>
      <h1 className="text-4xl font-black text-cyan-400">
        {title}
      </h1>
      <p className="mt-6 text-slate-400">
        Match Confidence
      </p>
      <h2 className="text-5xl font-bold text-green-400 mt-2">
        {percentage}%
      </h2>
    </div>
  );
}