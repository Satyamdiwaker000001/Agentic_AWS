'use client';
import { useState } from 'react';

// Normally we would fetch this from the backend or WebSocket
export function AdminDashboard() {
  const [threadId, setThreadId] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleAction = async (approved: boolean) => {
    if (!threadId) return;
    setIsProcessing(true);
    try {
      const res = await fetch('http://localhost:8000/admin/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thread_id: threadId, approved }),
      });
      const data = await res.json();
      if (data.error) {
        setStatus(`Error: ${data.error}`);
      } else {
        setStatus(approved ? 'Approved ✅' : 'Rejected ❌');
      }
    } catch (error) {
      setStatus('Network error connecting to API');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-zinc-950 border border-zinc-800 rounded-xl overflow-hidden shadow-2xl p-6">
      <h2 className="text-xl text-zinc-100 font-bold mb-6 flex items-center gap-2">
        <span className="bg-red-500/20 text-red-500 px-2 py-1 rounded text-xs font-mono">HITL Node</span>
        Manager Approval Dashboard
      </h2>

      <div className="space-y-4">
        <p className="text-zinc-400 text-sm">
          Enter the Thread ID of a conversation that has been paused by the LangGraph Escalation node to approve or reject the refund.
        </p>

        <div>
          <label className="block text-zinc-500 text-xs font-semibold mb-1 uppercase tracking-wider">Thread ID</label>
          <input
            type="text"
            value={threadId}
            onChange={(e) => setThreadId(e.target.value)}
            placeholder="e.g. 1a2b3c"
            className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2 text-zinc-200 focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-4 mb-4">
          <h3 className="text-zinc-300 font-medium mb-2">Pending Request Details</h3>
          <ul className="text-zinc-500 text-sm space-y-1">
            <li><span className="text-zinc-400">Action:</span> High-Value Refund</li>
            <li><span className="text-zinc-400">Amount:</span> &gt; $100.00</li>
            <li><span className="text-zinc-400">Policy:</span> Requires manual verification</li>
          </ul>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => handleAction(true)}
            disabled={!threadId || isProcessing}
            className="flex-1 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 border border-emerald-600/50 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            Approve
          </button>
          <button
            onClick={() => handleAction(false)}
            disabled={!threadId || isProcessing}
            className="flex-1 bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-600/50 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            Reject
          </button>
        </div>

        {status && (
          <div className={`mt-4 p-3 rounded-lg text-sm text-center font-medium ${
            status.includes('Approved') ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 
            status.includes('Error') ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
            'bg-red-500/10 text-red-400 border border-red-500/20'
          }`}>
            {status}
          </div>
        )}
      </div>
    </div>
  );
}
