import Sidebar from "../components/Sidebar";
import { History as HistoryIcon } from "lucide-react";
import { motion } from "framer-motion";

export default function History() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex relative overflow-hidden">
      <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600/10 blur-[150px] pointer-events-none" />
      <Sidebar />
      <main className="flex-1 ml-72 p-10 z-10 h-screen overflow-y-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-16 text-center border-dashed border-slate-700/50 mt-10"
        >
          <div className="w-24 h-24 bg-slate-800/50 rounded-full flex items-center justify-center mx-auto mb-6">
            <HistoryIcon size={48} className="text-slate-500" />
          </div>
          <h3 className="text-2xl font-bold text-slate-400">Scan History</h3>
          <p className="text-slate-500 mt-2 max-w-xl mx-auto">
            View your past resume scores and track your improvement over time. Connect to a database to enable this feature.
          </p>
        </motion.div>
      </main>
    </div>
  );
}
