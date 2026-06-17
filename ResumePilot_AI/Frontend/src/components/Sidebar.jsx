import {
  LayoutDashboard,
  FileSearch,
  History,
  Target,
  BrainCircuit,
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();
  const currentPath = location.pathname;

  const isActive = (path) => currentPath === path;

  return (
    <aside
      className="
      fixed
      left-0
      top-0
      w-72
      h-screen
      bg-slate-950
      border-r
      border-slate-800
      p-8
      z-50
      "
    >
      <div className="flex items-center gap-3 mb-12">
        <BrainCircuit
          size={34}
          className="text-cyan-400"
        />
        <div>
          <h1 className="text-2xl font-bold">
            ResumePilot
          </h1>
          <p className="text-slate-500 text-sm">
            AI Career Engine
          </p>
        </div>
      </div>

      <div className="space-y-3">
        <Link to="/dashboard" className={`sidebar-btn flex items-center gap-3 w-full text-left ${isActive('/dashboard') ? 'bg-slate-800 text-blue-400' : ''}`}>
          <LayoutDashboard size={18} />
          Dashboard
        </Link>

        <Link to="/analysis" className={`sidebar-btn flex items-center gap-3 w-full text-left ${isActive('/analysis') ? 'bg-slate-800 text-blue-400' : ''}`}>
          <FileSearch size={18} />
          Analysis
        </Link>

        <Link to="/history" className={`sidebar-btn flex items-center gap-3 w-full text-left ${isActive('/history') ? 'bg-slate-800 text-blue-400' : ''}`}>
          <History size={18} />
          History
        </Link>

        <Link to="/ats-guide" className={`sidebar-btn flex items-center gap-3 w-full text-left ${isActive('/ats-guide') ? 'bg-slate-800 text-blue-400' : ''}`}>
          <Target size={18} />
          ATS Guide
        </Link>
      </div>

      <div className="mt-12 glass-card p-4">
        <p className="text-xs text-slate-500">
          ResumePilot AI
        </p>
        <h3 className="text-cyan-400 mt-2">
          Career Intelligence
        </h3>
      </div>
    </aside>
  );
}