import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

export default function ScoreMeter({ score = 0, label = "ATS Score" }) {
  // Determine color based on score
  let pathColor = '#ef4444'; // red-500
  if (score >= 80) pathColor = '#22c55e'; // green-500
  else if (score >= 60) pathColor = '#eab308'; // yellow-500

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="w-40 h-40">
        <CircularProgressbar
          value={score}
          text={`${score}`}
          styles={buildStyles({
            pathColor: pathColor,
            textColor: pathColor,
            trailColor: '#1e293b', // slate-800
            pathTransitionDuration: 1.5,
            textSize: '24px',
          })}
        />
      </div>
      <p className="mt-4 text-slate-400 font-semibold tracking-widest uppercase text-sm">
        {label}
      </p>
    </div>
  );
}
