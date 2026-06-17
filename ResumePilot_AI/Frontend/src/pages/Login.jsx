import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Login() {
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        localStorage.setItem("loggedIn", "true");
        navigate("/dashboard");
    };

    return (
        <div className="min-h-screen flex justify-center items-center px-6 relative overflow-hidden">
            
            {/* Background decoration */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-2xl h-96 bg-indigo-600/20 blur-[120px] rounded-full pointer-events-none" />

            <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="glass-card w-[450px] p-10 z-10"
            >
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold gradient-text pb-2">ResumePilot AI</h1>
                    <p className="text-slate-400 mt-2">Welcome back. Let's land that dream job.</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-5">
                    <div>
                        <input
                            type="email"
                            placeholder="Email"
                            required
                            className="w-full p-4 rounded-xl bg-slate-900/80 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                        />
                    </div>

                    <div>
                        <input
                            type="password"
                            placeholder="Password"
                            required
                            className="w-full p-4 rounded-xl bg-slate-900/80 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                        />
                    </div>

                    <button type="submit" className="primary-btn w-full mt-2">
                        Login
                    </button>
                </form>
            </motion.div>
        </div>
    );
}