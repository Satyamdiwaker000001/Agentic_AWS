import { ArrowRight } from "lucide-react";

export default function PredictedScoreCard({ currentScore, predictedScore }) {
  const current = currentScore || 74;
  const predicted = predictedScore || Math.min(100, current + 17);

  return (
    <div className="glass-card p-8 flex flex-col justify-center">
      <h2 className="text-xl font-bold mb-6 text-slate-300">
        ATS Improvement Simulator
      </h2>
      
      <div className="flex justify-between items-center bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
        <div className="text-center">
          <p className="text-slate-400 mb-2 uppercase tracking-wider text-xs font-semibold">Current</p>
          <h1 className="text-5xl font-black text-orange-400">{current}</h1>
        </div>

        <div className="text-slate-500">
          <ArrowRight size={32} />
        </div>

        <div className="text-center">
          <p className="text-slate-400 mb-2 uppercase tracking-wider text-xs font-semibold">Predicted</p>
          <h1 className="text-5xl font-black text-green-400">{predicted}</h1>
        </div>
      </div>
      
      <p className="text-sm text-slate-500 mt-6 text-center">
        Implementing all AI suggestions can boost your score by {predicted - current} points!
      </p>
    </div>
  );
}