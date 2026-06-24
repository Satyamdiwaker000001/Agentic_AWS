import React, { useState, useEffect, useRef } from 'react';
import { 
  MessageSquare, Plus, Brain, Sliders,
  Copy, Download, RefreshCw, Layers, 
  ChevronLeft, ChevronRight, Cpu, Zap, Activity, 
  Send, Trash2, Code, FileCode, Check, TerminalSquare, Eye, PlayCircle
} from 'lucide-react';
import Editor from '@monaco-editor/react';
import ReactMarkdown from 'react-markdown';
import confetti from 'canvas-confetti';

// Interface declarations
interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  intent?: string;
  agent?: string;
  confidence?: number;
  metadata?: any;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  activeIntent?: string;
  metadata?: any;
}

export default function App() {
  // Navigation & UI States
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'fallback'>('checking');
  
  // Chat & History States
  const [sessions, setSessions] = useState<ChatSession[]>(() => {
    const saved = localStorage.getItem('nexus_sessions');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) { console.error(e); }
    }
    return [
      {
        id: 'session-1',
        title: 'React Login Form UI',
        messages: [
          { id: 'm1', sender: 'user', text: 'Write a React Login Form', timestamp: '9:30 PM' },
          { 
            id: 'm2', 
            sender: 'bot', 
            text: 'Here is a clean, modern React Login Form styled with TailwindCSS and Lucide icons. I have loaded it into the dynamic workspace\'s code editor. It features state tracking, loading behavior, and a sleek dark design.', 
            timestamp: '9:31 PM',
            intent: 'coding',
            agent: 'Coding Agent',
            confidence: 0.96,
            metadata: {
              language: 'jsx',
              filename: 'LoginForm.jsx',
              code: `import React, { useState } from 'react';
import { Mail, Lock, ArrowRight, Github } from 'lucide-react';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert('Logged in successfully!');
    }, 1500);
  };

  return (
    <div className="w-full max-w-md mx-auto p-8 rounded-2xl bg-neutral-900/50 border border-neutral-800 backdrop-blur-xl shadow-2xl">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold tracking-tight text-white">Welcome back</h2>
        <p className="mt-2 text-sm text-neutral-400">Enter your credentials to access your workspace</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-2">
            Email Address
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-lg bg-neutral-950 border border-neutral-800 text-white placeholder-neutral-500 focus:outline-none focus:border-violet-500 transition-colors"
              placeholder="you@domain.com"
              required
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
              Password
            </label>
            <a href="#" className="text-xs text-violet-400 hover:text-violet-300 transition-colors">
              Forgot password?
            </a>
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-lg bg-neutral-950 border border-neutral-800 text-white placeholder-neutral-500 focus:outline-none focus:border-violet-500 transition-colors"
              placeholder="••••••••"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-violet-600 hover:bg-violet-500 text-white font-semibold transition-colors"
        >
          {loading ? 'Signing in...' : 'Sign In'}
          <ArrowRight className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}`
            }
          }
        ],
        activeIntent: 'coding'
      }
    ];
  });
  
  const [currentSessionId, setCurrentSessionId] = useState<string>('session-1');
  const [inputVal, setInputVal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [thinkingStep, setThinkingStep] = useState<'idle' | 'input' | 'routing' | 'agent' | 'reasoning' | 'generating'>('idle');

  
  // Dynamic Workspace Interactive States
  const [editorCode, setEditorCode] = useState<string>('// Enter coding mode to view generated scripts');
  const [editorLanguage, setEditorLanguage] = useState<string>('javascript');
  const [editorFilename, setEditorFilename] = useState<string>('workspace.js');
  const [isCopied, setIsCopied] = useState(false);
  const [workspaceExpanded, setWorkspaceExpanded] = useState(false);
  const [insightsExpanded, setInsightsExpanded] = useState(false);
  
  // Execution & Sandbox States
  const [workspaceTab, setWorkspaceTab] = useState<'editor' | 'preview' | 'terminal'>('editor');
  const [terminalOutput, setTerminalOutput] = useState<string>('');
  const [isExecuting, setIsExecuting] = useState(false);

  // Chat message container scroll ref
  const chatBottomRef = useRef<HTMLDivElement>(null);

  // Fetch FastAPI connection
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/dashboard/stats');
        if (res.ok) {
          setBackendStatus('connected');
        } else {
          setBackendStatus('fallback');
        }
      } catch (e) {
        setBackendStatus('fallback');
      }
    };
    fetchStats();
  }, []);

  // Save Sessions to localStorage
  useEffect(() => {
    localStorage.setItem('nexus_sessions', JSON.stringify(sessions));
  }, [sessions]);

  // Scroll to bottom when messages load
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    
    // Set dynamic workspace values from the last message in current session
    const currentSession = sessions.find(s => s.id === currentSessionId);
    if (currentSession && currentSession.messages.length > 0) {
      const lastBotMessage = [...currentSession.messages].reverse().find(m => m.sender === 'bot');
      if (lastBotMessage && lastBotMessage.metadata) {
        const meta = lastBotMessage.metadata;
        if (lastBotMessage.intent === 'coding') {
          setEditorCode(meta.code || '');
          setEditorLanguage(meta.language || 'javascript');
          setEditorFilename(meta.filename || 'workspace.js');
        } else if (lastBotMessage.intent === 'debug') {
          // Store coding states too
          setEditorCode(meta.fixedCode || '');
          setEditorLanguage('python');
          setEditorFilename('debugged.py');
        }
      }
    }
  }, [sessions, currentSessionId]);

  const activeSession = sessions.find(s => s.id === currentSessionId) || sessions[0];

  // Frontend local fallback response generator for offline simulation (Investor-Demo quality)
  const getSimulatedResponse = (query: string): { intent: string, agent: string, confidence: number, response: string, metadata: any } => {
    const queryLower = query.toLowerCase();
    
    // Detect intent from text
    let intent = 'general';
    if (queryLower.includes('fix') || queryLower.includes('bug') || queryLower.includes('error') || queryLower.includes('debug')) {
      intent = 'debug';
    } else if (queryLower.includes('acceleration') || queryLower.includes('velocity') || queryLower.includes('gravity') || queryLower.includes('physics') || queryLower.includes('speed')) {
      intent = 'physics';
    } else if (queryLower.includes('differentiate') || queryLower.includes('solve') || queryLower.includes('math') || queryLower.includes('derivative') || queryLower.includes('x^') || queryLower.includes('x²')) {
      intent = 'math';
    } else if (queryLower.includes('write') || queryLower.includes('react') || queryLower.includes('javascript') || queryLower.includes('code') || queryLower.includes('python') || queryLower.includes('html') || queryLower.includes('css') || queryLower.includes('js') || queryLower.includes('build')) {
      intent = 'coding';
    }

    const responseMap: Record<string, any> = {
      general: {
        agent: 'General Agent',
        confidence: 0.94,
        response: `## Comprehensive Answer

You asked about: **"${query}"**

This is an insightful question. The core concept behind this involves understanding the fundamental principles that govern the subject.

### Key Points:
1. **Historical Context**: The development of this idea revolutionized the field, shifting paradigms from classical models to more modern interpretations.
2. **Practical Applications**: Today, this concept is heavily utilized in various domains, including technology, natural sciences, and complex systems analysis.
3. **Future Implications**: Ongoing research continues to expand our understanding, potentially leading to breakthroughs in efficiency and scalability.

If you'd like a deeper dive into any specific aspect, just let me know!`,
        metadata: {}
      },
      coding: {
        agent: 'Coding Agent',
        confidence: 0.98,
        response: `I have generated a clean coding solution in response to your request. 
I have updated the **Monaco Code Editor** in the Dynamic Workspace pane with the full script. 

### Implementation Highlights:
* **Framework**: React / Web standard
* **Styling**: Tailwind CSS
* **Aesthetics**: Premium Glassmorphism, smooth micro-interactions
* **Exportable**: Copy or Download directly from the Editor tabs!`,
        metadata: {
          language: 'typescript',
          filename: 'Button.tsx',
          code: `import React from 'react';
import { Sparkles } from 'lucide-react';

interface PremiumButtonProps {
  label: string;
  onClick?: () => void;
  variant?: 'primary' | 'cyan';
}

export const PremiumButton: React.FC<PremiumButtonProps> = ({ 
  label, 
  onClick, 
  variant = 'primary' 
}) => {
  const baseStyles = "relative px-6 py-3 rounded-lg font-semibold overflow-hidden transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2 border shadow-lg";
  const variants = {
    primary: "bg-violet-600/20 text-violet-300 border-violet-500/30 hover:bg-violet-600/30 hover:border-violet-500/50 shadow-violet-900/10",
    cyan: "bg-cyan-600/20 text-cyan-300 border-cyan-500/30 hover:bg-cyan-600/30 hover:border-cyan-500/50 shadow-cyan-900/10"
  };

  return (
    <button 
      onClick={onClick}
      className={\`\${baseStyles} \${variants[variant]}\`}
    >
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full hover:animate-[shimmer_1.5s_infinite]" />
      <Sparkles className="w-4 h-4 animate-pulse text-violet-400" />
      {label}
    </button>
  );
};`
        }
      },
      debug: {
        agent: 'Debug Agent',
        confidence: 0.96,
        response: `I have reviewed the code. A logic flaw causing execution exceptions was detected.
The issue has been corrected, and a side-by-side comparison is loaded in the **Debug Panel** on the right. 

### Diagnostics:
* **Error Type**: ZeroDivisionError / Reference Exception
* **Impact**: Blocks standard container lists from resolving correctly.
* **Resolution**: Guard checks injected and shadowed globals removed.`,
        metadata: {
          errorType: 'ZeroDivisionError (division by zero)',
          rootCause: 'The function divides total_sum by len(numbers). When list numbers is empty [], it divides by 0, prompting a runtime crash.',
          suggestedFix: 'Implement an early return validation checks block `if not numbers: return 0.0` at the very entry of calculation.',
          bestPractices: '1. Guard boundaries. 2. Do not shadow built-in symbols (like "sum"). 3. Write unit assertions.',
          originalCode: `def calculate_average(numbers):
    sum = 0
    for n in numbers:
      sum += n
    return sum / len(numbers)

# Empty array throws Division Error
calculate_average([])`,
          fixedCode: `def calculate_average(numbers):
    # Safe checks for empty array
    if not numbers:
        return 0.0
        
    total_sum = 0
    for n in numbers:
        total_sum += n
    return total_sum / len(numbers)

# Resolves safely to 0.0
calculate_average([])`
        }
      },
      math: {
        agent: 'Math Agent',
        confidence: 0.97,
        response: `I have resolved the mathematical differentiation task. The step-by-step resolution has been generated.

Please check the **Mathematics Workspace** panel on the right for LaTeX-formatted derivatives and step descriptions.`,
        metadata: {
          problem: 'd/dx (x² + 5x)',
          method: 'Power Rule of Differentiation & Linearity of Derivatives',
          steps: [
            { title: 'Linearity Rule', content: 'Split the expression term-by-term: \n$$\\frac{d}{dx}(x^2 + 5x) = \\frac{d}{dx}(x^2) + \\frac{d}{dx}(5x)$$' },
            { title: 'Apply Power Rule to x²', content: 'By definition: $$\\frac{d}{dx}(x^n) = n x^{n-1}$$\nSubstituting $n=2$ gives: $$2x$$' },
            { title: 'Apply Constant Rule to 5x', content: 'Pull the constant coefficient out: $$5 \\cdot \\frac{d}{dx}(x) = 5 \\cdot 1 = 5$$' },
            { title: 'Sum Derivative Terms', content: 'Combine the resolved derivatives: $$2x + 5$$' }
          ],
          answer: '2x + 5'
        }
      },
      physics: {
        agent: 'Physics Agent',
        confidence: 0.95,
        response: `The physics kinematics numerical has been solved successfully. The step calculations, formula usage, and substituted values are rendered in the **Physics Card** panel to the right.`,
        metadata: {
          given: {
            "Initial velocity (u)": "0 m/s (starts from rest)",
            "Acceleration (a)": "2 m/s²",
            "Time interval (t)": "10 seconds"
          },
          formula: 'v = u + at',
          substitution: 'v = 0 m/s + (2 m/s² × 10 s)',
          calculation: 'v = 0 + 20 = 20 m/s',
          answer: '20 m/s'
        }
      }
    };

    return responseMap[intent] || responseMap['general'];
  };

  // Submit Prompt Handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim() || isLoading) return;

    const userMessageText = inputVal.trim();
    setInputVal('');
    setIsLoading(true);

    // 1. Append User Message
    const userMsg: Message = {
      id: `u-${Date.now()}`,
      sender: 'user',
      text: userMessageText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    // Add to active session messages
    const updatedSessions = sessions.map(s => {
      if (s.id === currentSessionId) {
        return { ...s, messages: [...s.messages, userMsg] };
      }
      return s;
    });
    setSessions(updatedSessions);

    // 2. Trigger AI Thinking Timeline Animation (Premium UX)
    setThinkingStep('input');
    await new Promise(r => setTimeout(r, 400));
    setThinkingStep('routing');
    await new Promise(r => setTimeout(r, 500));
    setThinkingStep('agent');
    await new Promise(r => setTimeout(r, 500));
    setThinkingStep('reasoning');
    await new Promise(r => setTimeout(r, 500));
    setThinkingStep('generating');
    await new Promise(r => setTimeout(r, 300));

    let finalIntent = 'general';
    let finalAgent = 'General Agent';
    let finalConfidence = 0.90;
    let responseText = '';
    let responseMetadata: any = {};

    // 3. Make Backend API Call
    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessageText })
      });

      if (response.ok) {
        const data = await response.json();
        finalIntent = data.intent;
        finalAgent = data.agent;
        finalConfidence = data.confidence;
        responseText = data.response;
        responseMetadata = data.metadata;
        setBackendStatus('connected');
      } else {
        // Fallback
        const fallback = getSimulatedResponse(userMessageText);
        finalIntent = fallback.intent;
        finalAgent = fallback.agent;
        finalConfidence = fallback.confidence;
        responseText = fallback.response;
        responseMetadata = fallback.metadata;
        setBackendStatus('fallback');
      }
    } catch (error) {
      // Fallback
      const fallback = getSimulatedResponse(userMessageText);
      finalIntent = fallback.intent;
      finalAgent = fallback.agent;
      finalConfidence = fallback.confidence;
      responseText = fallback.response;
      responseMetadata = fallback.metadata;
      setBackendStatus('fallback');
    }

    // Update dynamic view fields
    if (finalIntent === 'coding' && responseMetadata.code) {
      setEditorCode(responseMetadata.code);
      setEditorLanguage(responseMetadata.language || 'javascript');
      setEditorFilename(responseMetadata.filename || 'workspace.js');
    } else if (finalIntent === 'debug' && responseMetadata.fixedCode) {
      setEditorCode(responseMetadata.fixedCode);
      setEditorLanguage('python');
      setEditorFilename('debugged.py');
    }

    // 4. Append Bot Message
    const botMsg: Message = {
      id: `b-${Date.now()}`,
      sender: 'bot',
      text: responseText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      intent: finalIntent,
      agent: finalAgent,
      confidence: finalConfidence,
      metadata: responseMetadata
    };

    setSessions(prev => prev.map(s => {
      if (s.id === currentSessionId) {
        // Update session title if it's the first message query
        const title = s.messages.length === 1 ? (userMessageText.slice(0, 24) + (userMessageText.length > 24 ? '...' : '')) : s.title;
        return {
          ...s,
          title,
          activeIntent: finalIntent,
          messages: [...s.messages, botMsg]
        };
      }
      return s;
    }));

    // Trigger celebration for coding/math success!
    if (['coding', 'math', 'physics'].includes(finalIntent)) {
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.8 },
        colors: [finalIntent === 'coding' ? '#7C3AED' : '#06B6D4', '#22C55E', '#10B981']
      });
    }

    setThinkingStep('idle');
    setIsLoading(false);
  };

  // Create a New Chat Session
  const createNewSession = () => {
    const id = `session-${Date.now()}`;
    const newSession: ChatSession = {
      id,
      title: 'New Session',
      messages: [],
      activeIntent: 'general'
    };
    setSessions([newSession, ...sessions]);
    setCurrentSessionId(id);
    
    // Clear code editor
    setEditorCode('// Workspace cleared. Type a prompt in the chat input.');
    setEditorFilename('workspace.js');
    setEditorLanguage('javascript');
  };

  // Delete Session
  const deleteSession = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const remaining = sessions.filter(s => s.id !== id);
    if (remaining.length === 0) {
      const defaultSess: ChatSession = { id: 'default', title: 'New Session', messages: [] };
      setSessions([defaultSess]);
      setCurrentSessionId('default');
    } else {
      setSessions(remaining);
      if (currentSessionId === id) {
        setCurrentSessionId(remaining[0].id);
      }
    }
  };

  // Edit & Retry Message Feature
  const handleRegenerate = (msgId: string) => {
    const session = sessions.find(s => s.id === currentSessionId);
    if (!session) return;
    const msgIndex = session.messages.findIndex(m => m.id === msgId);
    if (msgIndex <= 0) return;
    
    const prevUserMsg = session.messages[msgIndex - 1];
    if (prevUserMsg.sender !== 'user') return;
    
    const newMessages = session.messages.slice(0, msgIndex);
    setSessions(prev => prev.map(s => s.id === currentSessionId ? { ...s, messages: newMessages } : s));
    setInputVal(prevUserMsg.text);
  };

  // Copy Editor Code Utility
  const copyToClipboard = () => {
    navigator.clipboard.writeText(editorCode);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  // Download Editor Code Utility
  const downloadCode = () => {
    const element = document.createElement("a");
    const file = new Blob([editorCode], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = editorFilename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Run Code Execution Utility
  const handleRunCode = async () => {
    const isWeb = ['html', 'javascript', 'js', 'jsx', 'tsx'].includes(editorLanguage.toLowerCase());
    
    if (isWeb) {
      setWorkspaceTab('preview');
    } else {
      setWorkspaceTab('terminal');
    }
    
    setIsExecuting(true);
    setTerminalOutput('Execution initialized... routing to backend pipeline...');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: editorLanguage, code: editorCode })
      });

      if (res.ok) {
        const data = await res.json();
        const out = data.stdout + (data.stderr ? `\n[STDERR]\n${data.stderr}` : '');
        setTerminalOutput(out || 'Execution completed with exit code 0.');
      } else {
        setTerminalOutput('Backend Error: Execution failed or is not supported for this language context.');
      }
    } catch (e) {
      setTerminalOutput('Network Error: Orchestrator backend unreachable.');
    } finally {
      setIsExecuting(false);
    }
  };

  // Determine active dynamic workspace layout template
  const lastBotResponse = [...activeSession.messages].reverse().find(m => m.sender === 'bot');
  const activeIntent = lastBotResponse?.intent || activeSession.activeIntent || 'general';
  const metadata = lastBotResponse?.metadata || {};

  return (
    <div className="flex h-screen bg-zinc-950 text-neutral-100 overflow-hidden font-sans">
      
      {/* ----------------- SIDEBAR ----------------- */}
      <div 
        className={`${
          sidebarOpen ? 'w-64' : 'w-16'
        } shrink-0 bg-zinc-900 border-r border-zinc-800 flex flex-col justify-between transition-all duration-300 ease-in-out z-20`}
      >
        <div className="flex flex-col overflow-y-auto flex-grow">
          {/* Logo Header */}
          <div className="p-4 flex items-center justify-between border-b border-zinc-800/50">
            {sidebarOpen ? (
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center glow-primary">
                  <Brain className="w-5 h-5 text-white animate-pulse" />
                </div>
                <span className="font-bold font-sans text-md bg-gradient-to-r from-white via-neutral-100 to-neutral-400 bg-clip-text text-transparent">
                  NEXUS AI
                </span>
              </div>
            ) : (
              <div className="w-8 h-8 mx-auto rounded-lg bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center glow-primary">
                <Brain className="w-5 h-5 text-white" />
              </div>
            )}
            
            {sidebarOpen && (
              <button 
                onClick={() => setSidebarOpen(false)}
                className="p-1.5 rounded bg-neutral-950 border border-neutral-800 text-neutral-400 hover:text-white transition-colors"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* New Chat Button */}
          <div className="p-3">
            <button 
              onClick={() => createNewSession()}
              className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg bg-violet-600 hover:bg-violet-500 text-white font-medium transition-all shadow-lg hover:shadow-violet-900/20 border border-violet-500/20"
            >
              <Plus className="w-4 h-4 shrink-0" />
              {sidebarOpen && <span>New Session</span>}
            </button>
          </div>

          {/* Main Navigation */}
          <div className="px-2 py-4 space-y-1 border-b border-zinc-800/50">
            <button 
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all bg-neutral-900 text-cyan-400 font-semibold border-l-2 border-cyan-500"
            >
              <MessageSquare className="w-4 h-4 shrink-0" />
              {sidebarOpen && <span>Dynamic Router</span>}
            </button>
          </div>

          {/* Session History List */}
          {sidebarOpen && (
            <div className="p-3 flex-grow overflow-y-auto">
              <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider block mb-2">
                Recent Chats
              </span>
              <div className="space-y-1.5 max-h-60 overflow-y-auto">
                {sessions.map(s => (
                  <div
                    key={s.id}
                    onClick={() => {
                      setCurrentSessionId(s.id);
                    }}
                    className={`group flex items-center justify-between p-2 rounded-lg text-xs cursor-pointer border transition-colors ${
                      currentSessionId === s.id
                        ? 'bg-neutral-900 border-neutral-800 text-white font-medium'
                        : 'border-transparent text-neutral-400 hover:bg-neutral-950 hover:text-neutral-200'
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      <MessageSquare className="w-3 h-3 text-neutral-500 shrink-0" />
                      <span className="truncate">{s.title}</span>
                    </div>
                    <button 
                      onClick={(e) => deleteSession(s.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-0.5 hover:text-red-400 transition-opacity shrink-0"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar Footer settings */}
        <div className="p-4 border-t border-zinc-800/50 flex flex-col gap-2">
          {!sidebarOpen && (
            <button 
              onClick={() => setSidebarOpen(true)}
              className="p-1.5 mx-auto rounded bg-neutral-950 border border-neutral-800 text-neutral-400 hover:text-white transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          )}

          {sidebarOpen && (
            <div className="flex items-center gap-2 mt-2 px-1 text-[10px] text-neutral-500">
              <Cpu className="w-3.5 h-3.5 text-neutral-600" />
              <span>V1.0.0 Stable</span>
            </div>
          )}
        </div>
      </div>

      {/* ----------------- MAIN LAYOUT CONTAINER ----------------- */}
      <div className="flex flex-col flex-grow h-full overflow-hidden">
        
        {/* Top Header Bar */}
        <header className="h-14 bg-zinc-950 border-b border-zinc-800/50 flex items-center justify-between px-6 z-10 shrink-0">
          <div className="flex items-center gap-4">
            <h1 className="text-sm font-semibold tracking-wide text-neutral-200">
              <span className="flex items-center gap-2">
                <span>ACTIVE DESK:</span>
                <span className="px-2 py-0.5 text-xs font-bold rounded-full bg-neutral-900 border border-neutral-800 text-cyan-400">
                  Orchestrator Router Mode
                </span>
              </span>
            </h1>
          </div>

          <div className="flex items-center gap-4">
            {/* Backend connection indicator */}
            <div className="flex items-center gap-2 bg-neutral-950/80 border border-zinc-800 py-1.5 px-3 rounded-full text-xs">
              <div className={`w-2 h-2 rounded-full ${
                backendStatus === 'connected' ? 'bg-green-500 active-pulse' : 
                backendStatus === 'fallback' ? 'bg-yellow-500' : 'bg-neutral-600 animate-pulse'
              }`} />
              <span className="text-[11px] font-medium text-neutral-400">
                {backendStatus === 'connected' ? 'Agent Graph Engine: Online' : 
                 backendStatus === 'fallback' ? 'Offline Simulator' : 'Connecting...'}
              </span>
            </div>
            
            {/* Global Panel Toggles */}
            <div className="flex items-center gap-2 ml-4 pl-4 border-l border-neutral-800">
              <button
                onClick={() => setWorkspaceExpanded(!workspaceExpanded)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  workspaceExpanded 
                    ? 'bg-violet-600/20 text-violet-400 border border-violet-500/30' 
                    : 'bg-neutral-900 text-neutral-400 border border-neutral-800 hover:text-white'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                Workspace
              </button>
              
              <button
                onClick={() => setInsightsExpanded(!insightsExpanded)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  insightsExpanded 
                    ? 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/30' 
                    : 'bg-neutral-900 text-neutral-400 border border-neutral-800 hover:text-white'
                }`}
              >
                <Activity className="w-3.5 h-3.5" />
                Insights
              </button>
            </div>
          </div>
        </header>

        {/* ----------------- CHAT & WORKSPACE AREA ----------------- */}
        <div className="flex-grow flex h-full overflow-hidden">


            
            {/* Left Chat Pane (Flex column) */}
            <div className={`flex flex-col h-full overflow-hidden ${
              workspaceExpanded && ['coding', 'debug', 'math', 'physics'].includes(activeIntent) 
                ? 'w-7/12 border-r border-zinc-800' 
                : 'w-full'
            } transition-all duration-300 ease-in-out`}>
              
              {/* Message scroll container */}
              <div className="flex-grow overflow-y-auto p-6 space-y-6">
                {activeSession.messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-center p-8 space-y-6">
                    <div className="w-16 h-16 rounded-2xl bg-neutral-950 border border-neutral-800 flex items-center justify-center shadow-xl glow-primary">
                      <Brain className="w-8 h-8 text-violet-500 animate-pulse" />
                    </div>
                    <div className="max-w-md">
                      <h3 className="text-lg font-bold text-white">NEXUS MULTI-AGENT ORCHESTRATOR</h3>
                      <p className="text-xs text-neutral-400 mt-2">
                        Nexus automatically detects prompt intent and routes it to specialized AI agents.
                      </p>
                    </div>

                    {/* Quick suggestion cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg w-full text-left">
                      {[
                        { title: 'React Login Form', prompt: 'Write a React Login Form', agent: 'Coding Expert' },
                        { title: 'Differentiate Expression', prompt: 'Differentiate x² + 5x', agent: 'Math Solver' },
                        { title: 'Python Bug Detection', prompt: 'Fix this Python code', agent: 'Debug Engine' },
                        { title: 'Kinetic Motion Solver', prompt: 'A car starts from rest with acceleration 2 m/s² for 10 seconds. Find velocity.', agent: 'Physics Lab' }
                      ].map((item, idx) => (
                        <div 
                          key={idx}
                          onClick={() => setInputVal(item.prompt)}
                          className="p-3 bg-neutral-950 border border-zinc-800 hover:border-neutral-800 rounded-xl cursor-pointer hover:bg-neutral-900/40 transition-all text-xs"
                        >
                          <div className="flex justify-between items-center font-bold text-neutral-200">
                            <span>{item.title}</span>
                            <span className="text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-400">
                              {item.agent}
                            </span>
                          </div>
                          <p className="text-neutral-400 mt-1 truncate">{item.prompt}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  activeSession.messages.map(msg => (
                    <div 
                      key={msg.id}
                      className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-2xl rounded-2xl p-5 text-sm leading-relaxed border ${
                        msg.sender === 'user' 
                          ? 'bg-neutral-950 border-neutral-800 text-white shadow-md' 
                          : 'bg-neutral-900/30 border-zinc-800/50 text-neutral-200 shadow-sm'
                      }`}>
                        
                        {/* Sender header */}
                        <div className="flex items-center gap-2 mb-3">
                          <div className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold ${
                            msg.sender === 'user' ? 'bg-neutral-900 text-neutral-400 border border-neutral-800' : 'bg-violet-600 text-white font-serif'
                          }`}>
                            {msg.sender === 'user' ? 'U' : 'N'}
                          </div>
                          <span className="text-xs font-bold text-neutral-400">
                            {msg.sender === 'user' ? 'You' : (msg.agent || 'Nexus Agent')}
                          </span>
                          <span className="text-[10px] text-neutral-500 ml-auto">{msg.timestamp}</span>
                        </div>

                        {/* Text / Markdown output */}
                        {msg.sender === 'bot' ? (
                          <div className="prose prose-invert prose-xs max-w-none text-neutral-300">
                            <ReactMarkdown>{msg.text}</ReactMarkdown>
                          </div>
                        ) : (
                          <p className="whitespace-pre-wrap">{msg.text}</p>
                        )}
                        
                        {/* Action buttons on bot responses */}
                        {msg.sender === 'bot' && (
                          <div className="mt-4 pt-3 border-t border-zinc-800 flex items-center gap-2 text-xs">
                            {msg.intent && (
                              <span className="px-2 py-0.5 rounded bg-neutral-950 border border-neutral-800 text-[10px] font-bold text-neutral-400 capitalize">
                                Intent: {msg.intent}
                              </span>
                            )}
                            
                            <button 
                              onClick={() => handleRegenerate(msg.id)}
                              className="flex items-center gap-1 text-neutral-400 hover:text-white transition-colors ml-2"
                              title="Edit & Retry"
                            >
                              <RefreshCw className="w-3.5 h-3.5" />
                              Regenerate
                            </button>
                            
                            {['coding', 'debug'].includes(msg.intent || '') && (
                              <button 
                                onClick={() => setWorkspaceExpanded(true)}
                                className="ml-auto flex items-center gap-1 text-violet-400 hover:text-violet-300 font-bold"
                              >
                                <Code className="w-3.5 h-3.5" />
                                Inspect Workspace
                              </button>
                            )}
                            {['math', 'physics'].includes(msg.intent || '') && (
                              <button 
                                onClick={() => setWorkspaceExpanded(true)}
                                className="ml-auto flex items-center gap-1 text-cyan-400 hover:text-cyan-300 font-bold"
                              >
                                <Activity className="w-3.5 h-3.5" />
                                View Formula Steps
                              </button>
                            )}
                          </div>
                        )}

                      </div>
                    </div>
                  ))
                )}
                
                {/* Loading typing indicators */}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-neutral-900/30 border border-zinc-800/50 rounded-2xl p-5 max-w-md">
                      <div className="flex items-center gap-3">
                        <div className="flex space-x-1.5">
                          <div className="w-2.5 h-2.5 bg-violet-500 rounded-full animate-bounce" />
                          <div className="w-2.5 h-2.5 bg-cyan-500 rounded-full animate-bounce [animation-delay:0.2s]" />
                          <div className="w-2.5 h-2.5 bg-neutral-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                        </div>
                        <span className="text-xs font-semibold text-neutral-400">
                          {thinkingStep === 'input' && 'Parsing request inputs...'}
                          {thinkingStep === 'routing' && 'Intent classification processing...'}
                          {thinkingStep === 'agent' && 'Selecting target agent...'}
                          {thinkingStep === 'reasoning' && 'Reasoning chains executing...'}
                          {thinkingStep === 'generating' && 'Rendering output streams...'}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={chatBottomRef} />
              </div>

              {/* Chat Input Area */}
              <div className="p-4 border-t border-zinc-800 shrink-0 bg-zinc-950/90">
                <form onSubmit={handleSubmit} className="relative">
                  <input
                    type="text"
                    value={inputVal}
                    onChange={(e) => setInputVal(e.target.value)}
                    placeholder="Ask anything (code generation, debugging, physics, math solver)..."
                    className="w-full pl-4 pr-12 py-3.5 bg-neutral-950 border border-neutral-800 rounded-xl text-sm placeholder-neutral-500 focus:outline-none focus:border-violet-500/80 transition-colors shadow-2xl"
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !inputVal.trim()}
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white transition-colors disabled:opacity-30 disabled:hover:bg-violet-600 cursor-pointer"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </form>
                <div className="flex items-center justify-between text-[10px] text-neutral-500 mt-2 px-1">
                  <span>Press enter to send prompt</span>
                </div>
              </div>

            </div>

            {/* ----------------- DYNAMIC WORKSPACE (Right 40%) ----------------- */}
            {workspaceExpanded && ['coding', 'debug', 'math', 'physics'].includes(activeIntent) && (
              <div className="w-5/12 bg-[#0C0C0C] flex flex-col overflow-hidden relative">
                
                {/* Header tabs */}
                <div className="h-12 border-b border-zinc-800/80 px-4 flex items-center justify-between shrink-0 bg-zinc-900">
                  <div className="flex items-center gap-2">
                    <Layers className="w-4 h-4 text-violet-400" />
                    <span className="text-xs font-bold text-neutral-300 uppercase tracking-wider">
                      {activeIntent === 'coding' && 'Code Workspace'}
                      {activeIntent === 'debug' && 'Debugger Canvas'}
                      {activeIntent === 'math' && 'Equation Resolver'}
                      {activeIntent === 'physics' && 'Physics Laboratory'}
                    </span>
                  </div>

                  <button 
                    onClick={() => setWorkspaceExpanded(false)}
                    className="p-1 rounded hover:bg-neutral-900 text-neutral-400 hover:text-white transition-colors"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>

                {/* Pane Content */}
                <div className="flex-grow overflow-y-auto p-5 space-y-6">
                  
                  {/* --- CODING WORKSPACE VIEW --- */}
                  {activeIntent === 'coding' && (
                    <div className="h-full flex flex-col">
                      
                      {/* Top Action & Tab Bar */}
                      <div className="flex items-center justify-between border-b border-zinc-800 pb-3 mb-4 shrink-0">
                        <div className="flex bg-zinc-900/50 p-1 rounded-lg border border-zinc-800/80">
                          <button
                            onClick={() => setWorkspaceTab('editor')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                              workspaceTab === 'editor' ? 'bg-zinc-800 text-zinc-100 shadow-sm' : 'text-zinc-500 hover:text-zinc-300'
                            }`}
                          >
                            <Code className="w-3.5 h-3.5" /> Editor
                          </button>
                          <button
                            onClick={() => setWorkspaceTab('preview')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                              workspaceTab === 'preview' ? 'bg-zinc-800 text-zinc-100 shadow-sm' : 'text-zinc-500 hover:text-zinc-300'
                            }`}
                          >
                            <Eye className="w-3.5 h-3.5" /> Preview
                          </button>
                          <button
                            onClick={() => setWorkspaceTab('terminal')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                              workspaceTab === 'terminal' ? 'bg-zinc-800 text-zinc-100 shadow-sm' : 'text-zinc-500 hover:text-zinc-300'
                            }`}
                          >
                            <TerminalSquare className="w-3.5 h-3.5" /> Terminal
                          </button>
                        </div>
                        
                        <div className="flex items-center gap-2">
                           <button 
                             onClick={handleRunCode}
                             disabled={isExecuting}
                             className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-50 transition-colors"
                           >
                             {isExecuting ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <PlayCircle className="w-3.5 h-3.5" />}
                             Run Code
                           </button>
                        </div>
                      </div>

                      {/* Content Area */}
                      <div className="flex-grow flex flex-col min-h-[400px] overflow-hidden relative border border-zinc-800 rounded-xl bg-zinc-950">
                        {/* Editor Tab */}
                        {workspaceTab === 'editor' && (
                          <div className="absolute inset-0 flex flex-col">
                            <div className="flex items-center justify-between bg-zinc-900 border-b border-zinc-800 px-3 py-2 text-xs shrink-0">
                              <div className="flex items-center gap-2 font-mono text-zinc-300">
                                <FileCode className="w-3.5 h-3.5 text-blue-400" />
                                <span>{editorFilename}</span>
                              </div>
                              <div className="flex gap-1">
                                <button onClick={copyToClipboard} className="p-1 hover:text-white text-zinc-400 transition-colors">
                                  {isCopied ? <Check className="w-3.5 h-3.5 text-green-500" /> : <Copy className="w-3.5 h-3.5" />}
                                </button>
                                <button onClick={downloadCode} className="p-1 hover:text-white text-zinc-400 transition-colors">
                                  <Download className="w-3.5 h-3.5" />
                                </button>
                              </div>
                            </div>
                            <div className="flex-grow">
                              <Editor
                                height="100%"
                                language={editorLanguage}
                                theme="vs-dark"
                                value={editorCode}
                                onChange={(val) => setEditorCode(val || '')}
                                options={{ minimap: { enabled: false }, fontSize: 13, scrollbar: { vertical: 'auto', horizontal: 'auto' }, fontFamily: 'Consolas, monospace', padding: { top: 16 } }}
                              />
                            </div>
                          </div>
                        )}

                        {/* Terminal Tab */}
                        {workspaceTab === 'terminal' && (
                          <div className="absolute inset-0 bg-[#0C0C0C] p-4 overflow-y-auto font-mono text-xs text-zinc-300">
                            <div className="mb-2 text-zinc-500">$ Execute: {editorLanguage} {editorFilename}</div>
                            {isExecuting && <div className="text-blue-400 animate-pulse">Running process...</div>}
                            <pre className="whitespace-pre-wrap">{terminalOutput}</pre>
                          </div>
                        )}

                        {/* Preview Tab */}
                        {workspaceTab === 'preview' && (
                          <div className="absolute inset-0 bg-white">
                            <iframe 
                              title="preview"
                              srcDoc={editorCode}
                              className="w-full h-full border-none bg-white"
                              sandbox="allow-scripts allow-forms allow-same-origin"
                            />
                          </div>
                        )}
                      </div>

                    </div>
                  )}

                  {/* --- DEBUGGING CANVAS VIEW --- */}
                  {activeIntent === 'debug' && (
                    <div className="space-y-6">
                      
                      {/* Diagnostic details widgets */}
                      <div className="grid grid-cols-1 gap-4">
                        <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-xl">
                          <span className="text-[9px] uppercase font-bold text-red-400 tracking-wider">Exception Type</span>
                          <h4 className="text-sm font-bold text-neutral-200 mt-1">{metadata.errorType || "ZeroDivisionError"}</h4>
                        </div>

                        <div className="bg-neutral-950 border border-zinc-800 p-4 rounded-xl space-y-2">
                          <span className="text-[9px] uppercase font-bold text-neutral-500 tracking-wider block">Root Cause</span>
                          <p className="text-xs text-neutral-300 leading-relaxed">
                            {metadata.rootCause}
                          </p>
                        </div>

                        <div className="bg-neutral-950 border border-zinc-800 p-4 rounded-xl space-y-2">
                          <span className="text-[9px] uppercase font-bold text-violet-400 tracking-wider block">Suggested Fix</span>
                          <p className="text-xs text-neutral-300 leading-relaxed">
                            {metadata.suggestedFix}
                          </p>
                        </div>
                      </div>

                      {/* Side-by-side Diffs */}
                      <div className="space-y-4">
                        <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider block">Code Corrections</span>
                        
                        <div className="space-y-3">
                          <div className="flex flex-col rounded-lg border border-zinc-800 overflow-hidden">
                            <div className="bg-red-950/20 border-b border-zinc-800 px-3 py-1.5 text-[10px] font-bold text-red-400">
                              Buggy Code
                            </div>
                            <pre className="p-3 bg-neutral-950 text-neutral-400 font-mono text-[11px] overflow-x-auto">
                              <code>{metadata.originalCode}</code>
                            </pre>
                          </div>

                          <div className="flex flex-col rounded-lg border border-zinc-800 overflow-hidden">
                            <div className="bg-green-950/20 border-b border-zinc-800 px-3 py-1.5 text-[10px] font-bold text-green-400">
                              Fixed Code
                            </div>
                            <pre className="p-3 bg-neutral-950 text-neutral-200 font-mono text-[11px] overflow-x-auto">
                              <code>{metadata.fixedCode}</code>
                            </pre>
                          </div>
                        </div>
                      </div>

                      {/* Best practices list */}
                      <div className="bg-neutral-950 border border-zinc-800 p-4 rounded-xl">
                        <span className="text-[9px] uppercase font-bold text-neutral-500 tracking-wider block mb-2">Best Practices</span>
                        <p className="text-xs text-neutral-300 whitespace-pre-line leading-relaxed">
                          {metadata.bestPractices}
                        </p>
                      </div>

                    </div>
                  )}

                  {/* --- MATHEMATICS SOLUTIONS VIEW --- */}
                  {activeIntent === 'math' && (
                    <div className="space-y-6">
                      
                      {/* Problem details header */}
                      <div className="bg-neutral-950 border border-zinc-800 p-5 rounded-xl">
                        <span className="text-[9px] uppercase font-bold text-cyan-400 tracking-wider">Problem Statement</span>
                        <h4 className="text-lg font-mono font-bold text-white mt-1">{metadata.problem}</h4>
                        <div className="mt-3 pt-3 border-t border-zinc-800 text-xs text-neutral-400">
                          <span className="font-semibold text-neutral-300">Method Used:</span> {metadata.method}
                        </div>
                      </div>

                      {/* Step-by-step Cards */}
                      <div className="space-y-4">
                        <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider block">Solution Breakdown</span>
                        
                        <div className="space-y-3">
                          {metadata.steps && metadata.steps.map((step: any, idx: number) => (
                            <div key={idx} className="glass-card p-4 rounded-xl border border-zinc-800 flex gap-4">
                              <div className="w-6 h-6 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800/40 font-bold text-xs flex items-center justify-center shrink-0">
                                {idx + 1}
                              </div>
                              <div className="space-y-1">
                                <h5 className="text-xs font-bold text-neutral-200">{step.title}</h5>
                                <p className="text-xs text-neutral-400 whitespace-pre-line">{step.content}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Final Answer Card */}
                      <div className="bg-gradient-to-tr from-cyan-600/10 to-violet-500/10 border border-cyan-500/25 p-5 rounded-xl text-center glow-secondary">
                        <span className="text-[9px] uppercase font-black text-cyan-400 tracking-widest block">Final Output</span>
                        <div className="text-2xl font-black text-white mt-2 font-mono">{metadata.answer}</div>
                      </div>

                    </div>
                  )}

                  {/* --- PHYSICS WORKSPACE VIEW --- */}
                  {activeIntent === 'physics' && (
                    <div className="space-y-6">
                      
                      {/* Given variables list */}
                      <div className="bg-neutral-950 border border-zinc-800 p-5 rounded-xl space-y-3">
                        <span className="text-[9px] uppercase font-bold text-amber-400 tracking-wider block">Given parameters</span>
                        <div className="grid grid-cols-1 gap-2">
                          {metadata.given && Object.entries(metadata.given).map(([key, val]: any) => (
                            <div key={key} className="flex justify-between items-center text-xs py-1.5 border-b border-zinc-800 last:border-0">
                              <span className="text-neutral-400">{key}</span>
                              <span className="font-mono text-neutral-200 font-semibold">{val}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Formula Card */}
                      <div className="bg-neutral-950 border border-zinc-800 p-4 rounded-xl flex items-center justify-between">
                        <div>
                          <span className="text-[9px] uppercase font-bold text-neutral-500 tracking-wider block">Formula Applied</span>
                          <span className="text-base font-mono font-bold text-white block mt-1">{metadata.formula}</span>
                        </div>
                        <Zap className="w-6 h-6 text-amber-400 animate-pulse" />
                      </div>

                      {/* Substitutions & calculation */}
                      <div className="space-y-4">
                        <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider block">Calculations</span>
                        
                        <div className="space-y-3">
                          <div className="glass-card p-4 rounded-xl border border-zinc-800 space-y-1">
                            <span className="text-[9px] uppercase font-bold text-neutral-500 tracking-wider block">Substitution Step</span>
                            <pre className="text-xs text-neutral-300 font-mono overflow-x-auto">{metadata.substitution}</pre>
                          </div>

                          <div className="glass-card p-4 rounded-xl border border-zinc-800 space-y-1">
                            <span className="text-[9px] uppercase font-bold text-neutral-500 tracking-wider block">Calculation Path</span>
                            <pre className="text-xs text-neutral-200 font-mono overflow-x-auto">{metadata.calculation}</pre>
                          </div>
                        </div>
                      </div>

                      {/* Final units answer card */}
                      <div className="bg-gradient-to-tr from-amber-600/10 to-violet-500/10 border border-amber-500/25 p-5 rounded-xl text-center">
                        <span className="text-[9px] uppercase font-black text-amber-400 tracking-widest block">Final Velocity Answer</span>
                        <div className="text-2xl font-black text-white mt-2 font-mono">{metadata.answer}</div>
                      </div>

                    </div>
                  )}

                </div>
              </div>
            )}

            {/* ----------------- RIGHT INSIGHTS PANEL (Far Right 300px) ----------------- */}
            {insightsExpanded && (
              <div className="w-[300px] shrink-0 bg-zinc-900 border-l border-zinc-800/80 flex flex-col overflow-y-auto">
              
              <div className="p-4 border-b border-zinc-800/50 flex items-center justify-between bg-zinc-950/40 shrink-0">
                <span className="text-xs font-bold text-neutral-400 uppercase tracking-wider">Graph Telemetry</span>
                <Sliders className="w-3.5 h-3.5 text-neutral-600" />
              </div>

              <div className="p-5 space-y-6">
                
                {/* Agent Status List */}
                <div className="space-y-3">
                  <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider block">Agent Status</span>
                  
                  <div className="space-y-2">
                    {[
                      { name: 'Router Agent', role: 'router', status: activeSession.messages.length > 0 && isLoading ? 'active' : 'idle' },
                      { name: 'General Agent', role: 'general', status: activeIntent === 'general' && isLoading ? 'active' : 'idle' },
                      { name: 'Coding Agent', role: 'coding', status: activeIntent === 'coding' && isLoading ? 'active' : 'idle' },
                      { name: 'Debug Agent', role: 'debug', status: activeIntent === 'debug' && isLoading ? 'active' : 'idle' },
                      { name: 'Math Agent', role: 'math', status: activeIntent === 'math' && isLoading ? 'active' : 'idle' },
                      { name: 'Physics Agent', role: 'physics', status: activeIntent === 'physics' && isLoading ? 'active' : 'idle' }
                    ].map(agent => (
                      <div 
                        key={agent.role}
                        className={`flex items-center justify-between text-xs p-2 rounded border transition-colors ${
                          activeIntent === agent.role 
                            ? 'bg-neutral-900/60 border-neutral-800' 
                            : 'bg-transparent border-transparent'
                        }`}
                      >
                        <span className={`font-semibold ${activeIntent === agent.role ? 'text-neutral-200' : 'text-neutral-500'}`}>
                          {agent.name}
                        </span>
                        
                        <div className="flex items-center gap-1.5">
                          <span className={`text-[9px] uppercase font-bold ${
                            agent.status === 'active' || activeIntent === agent.role ? 'text-green-500' : 'text-neutral-600'
                          }`}>
                            {agent.status === 'active' || (activeIntent === agent.role && isLoading) ? 'ACTIVE' : 
                             (activeIntent === agent.role ? 'RESOLVED' : 'IDLE')}
                          </span>
                          <div className={`w-1.5 h-1.5 rounded-full ${
                            agent.status === 'active' || (activeIntent === agent.role && isLoading) ? 'bg-green-500 active-pulse' : 
                            (activeIntent === agent.role ? 'bg-green-600' : 'bg-neutral-800')
                          }`} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Circular Confidence SVG Gauge */}
                <div className="space-y-3 pt-4 border-t border-zinc-800">
                  <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider block">Confidence Rating</span>
                  
                  <div className="flex flex-col items-center justify-center p-3 bg-neutral-950 border border-zinc-800 rounded-xl">
                    <div className="relative w-28 h-28 flex items-center justify-center">
                      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        {/* Track ring */}
                        <circle 
                          cx="50" cy="50" r="40" 
                          stroke="#171717" strokeWidth="6" 
                          fill="transparent" 
                        />
                        {/* Progress ring */}
                        <circle 
                          cx="50" cy="50" r="40" 
                          stroke={activeIntent === 'general' ? '#6B7280' : '#7C3AED'} 
                          strokeWidth="6" 
                          fill="transparent" 
                          strokeDasharray="251.2"
                          strokeDashoffset={251.2 - (251.2 * (lastBotResponse?.confidence || 0.90))}
                          strokeLinecap="round"
                          className="transition-all duration-1000 ease-out"
                        />
                      </svg>
                      {/* Percent text label */}
                      <div className="absolute text-center">
                        <span className="text-xl font-black text-white block">
                          {Math.round((lastBotResponse?.confidence || 0.90) * 100)}%
                        </span>
                        <span className="text-[8px] text-neutral-500 font-bold uppercase tracking-wider">Score</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* AI Thinking Step Timeline */}
                <div className="space-y-3 pt-4 border-t border-zinc-800">
                  <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider block">Routing Stage Pipeline</span>
                  
                  <div className="space-y-3 relative before:absolute before:left-3 before:top-2 before:bottom-2 before:w-[1px] before:bg-neutral-800">
                    {[
                      { step: 'input', label: 'User Input Parsing' },
                      { step: 'routing', label: 'Intent Classification' },
                      { step: 'agent', label: 'Expert Selection' },
                      { step: 'reasoning', label: 'Agent Reasoning Steps' },
                      { step: 'generating', label: 'Output Construction' }
                    ].map((pipeline, idx) => {
                      const stepsOrder = ['idle', 'input', 'routing', 'agent', 'reasoning', 'generating'];
                      const currentIdx = stepsOrder.indexOf(thinkingStep);
                      const stepIdx = stepsOrder.indexOf(pipeline.step);
                      
                      const isActive = thinkingStep === pipeline.step;
                      const isCompleted = currentIdx > stepIdx && thinkingStep !== 'idle';
                      
                      return (
                        <div key={pipeline.step} className="flex items-center gap-4 text-xs pl-1">
                          <div className={`w-4 h-4 rounded-full border flex items-center justify-center text-[8px] shrink-0 z-10 ${
                            isActive ? 'bg-violet-600 border-violet-500 text-white animate-pulse' : 
                            isCompleted ? 'bg-green-950 border-green-700 text-green-400' : 'bg-neutral-950 border-neutral-800 text-neutral-600'
                          }`}>
                            {isCompleted ? '✓' : idx + 1}
                          </div>
                          
                          <span className={`font-semibold ${
                            isActive ? 'text-violet-400' : 
                            isCompleted ? 'text-neutral-400' : 'text-neutral-600'
                          }`}>
                            {pipeline.label}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Response Metadata Card */}
                <div className="space-y-3 pt-4 border-t border-neutral-900">
                  <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider block">Metadata Summary</span>
                  
                  <div className="bg-neutral-950 border border-neutral-900 rounded-xl overflow-hidden divide-y divide-neutral-900">
                    {[
                      { key: 'Response Time', val: metadata.responseTime ? `${metadata.responseTime} s` : 'N/A' },
                      { key: 'Active Agent', val: metadata.agentUsed || 'N/A' },
                      { key: 'Tokens Logged', val: metadata.tokensUsed || 'N/A' },
                      { key: 'Graph Stage', val: metadata.stage || 'N/A' }
                    ].map((item, idx) => (
                      <div key={idx} className="flex justify-between items-center p-3 text-xs">
                        <span className="text-neutral-500">{item.key}</span>
                        <span className="font-mono text-neutral-300 font-semibold">{item.val}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
