'use client';
import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store/chatStore';

export function ChatInterface() {
  const [input, setInput] = useState('');
  const [threadId, setThreadId] = useState('');
  const { messages, addMessage, appendToken, isTyping, setTyping } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setThreadId(Math.random().toString(36).substring(7));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setInput('');
    addMessage({ id: Date.now().toString(), role: 'user', content: userMsg });
    setTyping(true);

    const aiMsgId = (Date.now() + 1).toString();
    addMessage({ id: aiMsgId, role: 'agent', content: '' });

    try {
      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thread_id: threadId, message: userMsg }),
      });

      if (!response.ok) throw new Error('Network response was not ok');
      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');

      if (reader) {
        let buffer = '';
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // keep the incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('event: ')) {
              const eventName = line.substring(7).trim();
              continue; // we can track state using eventName if needed
            }
            if (line.startsWith('data: ')) {
              const dataStr = line.substring(6).trim();
              if (dataStr === 'finished') continue;
              
              try {
                const data = JSON.parse(dataStr);
                if (data.token) {
                  appendToken(aiMsgId, data.token);
                } else if (data.status === 'paused_for_approval') {
                  addMessage({
                    id: Date.now().toString(),
                    role: 'system',
                    content: '⏸️ System paused: Awaiting Manager Approval for Escalation.',
                  });
                } else if (data.tool) {
                  // Tool execution visualization
                  addMessage({
                    id: Date.now().toString(),
                    role: 'tool',
                    content: `Executing: ${data.tool}`,
                  });
                }
              } catch (e) {
                // If it's not JSON, it might just be raw text, but our API sends JSON
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error streaming chat:', error);
      addMessage({ id: Date.now().toString(), role: 'system', content: '❌ Error connecting to backend.' });
    } finally {
      setTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-zinc-950 border border-zinc-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Header */}
      <div className="bg-zinc-900 border-b border-zinc-800 p-4 flex items-center justify-between">
        <h2 className="text-zinc-100 font-semibold flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          AutoSolve Support
        </h2>
        <span className="text-xs text-zinc-500 font-mono">Thread: {threadId}</span>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-zinc-500 mt-10">
            Send a message to start support (e.g., "I need a refund for my $150 invoice")
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                m.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : m.role === 'tool'
                  ? 'bg-zinc-800 text-amber-400 font-mono text-xs border border-zinc-700'
                  : m.role === 'system'
                  ? 'bg-red-900/50 text-red-200 border border-red-800 text-sm w-full text-center'
                  : 'bg-zinc-800 text-zinc-200 border border-zinc-700'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-3 text-zinc-400 text-sm flex gap-1">
              <span className="animate-bounce">.</span><span className="animate-bounce delay-75">.</span><span className="animate-bounce delay-150">.</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-4 bg-zinc-900 border-t border-zinc-800 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your issue..."
          className="flex-1 bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2 text-zinc-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
          disabled={isTyping}
        />
        <button
          type="submit"
          disabled={!input.trim() || isTyping}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  );
}
