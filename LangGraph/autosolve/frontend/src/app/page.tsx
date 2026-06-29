import { ChatInterface } from '@/components/ChatInterface';
import { AdminDashboard } from '@/components/AdminDashboard';

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white p-4 md:p-8 font-sans selection:bg-blue-500/30">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            AutoSolve Enterprise
          </h1>
          <p className="text-zinc-400 mt-2">
            Multi-Agent LangGraph System with Server-Sent Events (SSE) & Human-in-the-Loop.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[700px]">
          {/* Left Column: User Chat Interface */}
          <section className="h-full">
            <ChatInterface />
          </section>

          {/* Right Column: Admin Dashboard */}
          <section className="h-full flex flex-col gap-8">
            <div className="h-[300px]">
               <AdminDashboard />
            </div>
            
            <div className="flex-1 bg-zinc-950 border border-zinc-800 rounded-xl p-6 shadow-2xl">
              <h2 className="text-lg font-semibold text-zinc-100 mb-4 flex items-center gap-2">
                <span className="text-blue-500">⚡</span> Agent Capabilities
              </h2>
              <ul className="space-y-3 text-sm text-zinc-400">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 mt-1">✓</span>
                  <div>
                    <strong className="text-zinc-300 block">Triage Router (AI)</strong>
                    Routes queries to "billing" or "general".
                  </div>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 mt-1">✓</span>
                  <div>
                    <strong className="text-zinc-300 block">Billing Tools (AI)</strong>
                    Can look up invoices and process refunds up to $100.
                  </div>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-500 mt-1">⚠</span>
                  <div>
                    <strong className="text-zinc-300 block">Escalation Policy (HITL)</strong>
                    Refunds &gt; $100 will pause the LangGraph and require approval via the Admin Dashboard.
                  </div>
                </li>
              </ul>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
