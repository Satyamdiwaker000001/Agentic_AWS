from utils.generate import generate_response
import re

def coding_agent(state):
    message = state["message"]
    query_lower = message.lower()
    
    # 1. Check for standard demo query
    if "react login" in query_lower:
        code_content = """import React, { useState } from 'react';
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

        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center text-neutral-400 cursor-pointer">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="mr-2 rounded border-neutral-800 bg-neutral-950 text-violet-500 focus:ring-0"
            />
            Remember me
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-violet-600 hover:bg-violet-500 text-white font-semibold transition-colors disabled:opacity-50"
        >
          {loading ? 'Signing in...' : 'Sign In'}
          <ArrowRight className="w-4 h-4" />
        </button>
      </form>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-neutral-800" /></div>
        <div className="relative flex justify-center text-xs uppercase"><span className="bg-neutral-900/50 px-2 text-neutral-500">Or continue with</span></div>
      </div>

      <button className="w-full flex items-center justify-center gap-2 py-3 rounded-lg border border-neutral-800 bg-neutral-950 hover:bg-neutral-900 text-white transition-colors">
        <Github className="w-5 h-5" />
        GitHub
      </button>
    </div>
  );
}"""
        return {
            "response": "Here is a clean, modern React Login Form styled with TailwindCSS and Lucide icons. I have loaded it into the dynamic workspace's code editor. It features state tracking, loading behavior, and a sleek dark design.",
            "metadata": {
                "language": "jsx",
                "filename": "LoginForm.jsx",
                "code": code_content
            }
        }
        
    # 2. General code generation fallback
    # Instruct the LLM to write everything in a single file so Monaco editor and Preview tab work seamlessly.
    prompt = (
        f"Write clean code for the following task. "
        f"CRITICAL RULE: If this is a web development task (HTML, CSS, JS), you MUST provide ONLY ONE single `html` file with embedded <style> and <script> tags. Do NOT split into multiple files. "
        f"If this is another language, provide the main script. "
        f"Format the output in Markdown with a clear code block. Task: {message}"
    )
    raw_response = generate_response(prompt)
    
    # Try to parse language and code block
    language = "javascript"
    filename = "index.js"
    code = raw_response
    
    # Try to extract code block, even if it's missing closing backticks
    code_match = re.search(r"```(\w+)?\n([\s\S]+?)(?:```|$)", raw_response)
    if code_match:
        language = code_match.group(1) or "javascript"
        code = code_match.group(2)
        
        # Deduce a reasonable filename
        if language == "python":
            filename = "script.py"
        elif language in ["javascript", "js"]:
            filename = "index.js"
            language = "javascript"
        elif language in ["typescript", "ts"]:
            filename = "index.ts"
            language = "typescript"
        elif language in ["jsx", "tsx"]:
            filename = "component.jsx"
        elif language == "html":
            filename = "index.html"
        elif language == "css":
            filename = "styles.css"
            
    return {
        "response": raw_response,
        "metadata": {
            "language": language,
            "filename": filename,
            "code": code.strip()
        }
    }