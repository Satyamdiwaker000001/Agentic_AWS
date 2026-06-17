import { useState } from "react";
import Sidebar from "../components/Sidebar";
import { Sparkles, Upload, Briefcase, CheckCircle, AlertCircle, FileText, Lightbulb } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";

import RadarAnalysis from "../components/charts/RadarAnalysis";
import ScoreBreakdown from "../components/charts/ScoreBreakdown";
import RoleMatchCard from "../components/charts/RoleMatchCard";
import PredictedScoreCard from "../components/charts/PredictedScoreCard";
import ScoreMeter from "../components/charts/ScoreMeter";

export default function Dashboard() {
    const [status, setStatus] = useState("idle"); // idle, uploading, analyzing, complete, error
    const [file, setFile] = useState(null);
    const [jdFile, setJdFile] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [jobTitle, setJobTitle] = useState("");
    const [results, setResults] = useState(null);
    const [errorMsg, setErrorMsg] = useState("");

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };

    const handleJdFileChange = async (e) => {
        if (e.target.files.length > 0) {
            const selectedFile = e.target.files[0];
            setJdFile(selectedFile);
            
            // Upload JD immediately to get text
            try {
                const formData = new FormData();
                formData.append("file", selectedFile);
                const response = await axios.post("http://localhost:8000/api/upload-jd", formData);
                setJobDescription(response.data.extracted_text);
            } catch (err) {
                console.error("Failed to upload JD", err);
            }
        }
    };

    const handleAnalyze = async () => {
        if (!file || (!jobDescription && !jdFile)) {
            setErrorMsg("Please provide a resume and a job description (text or file).");
            return;
        }

        setErrorMsg("");
        setStatus("analyzing");

        try {
            const formData = new FormData();
            formData.append("file", file);
            formData.append("jobTitle", jobTitle || "Target Role");
            formData.append("jobDescription", jobDescription);

            // Fetch comprehensive analysis
            const response = await axios.post("http://localhost:8000/api/analyze", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });

            setResults(response.data);
            setStatus("complete");
        } catch (error) {
            console.error("Analysis failed:", error);
            setErrorMsg("Failed to analyze resume. Make sure the backend is running.");
            setStatus("error");
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex relative overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600/10 blur-[150px] pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-600/10 blur-[150px] pointer-events-none" />

            <Sidebar />

            <main className="flex-1 ml-72 p-10 space-y-10 z-10 h-screen overflow-y-auto">
                <motion.section 
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-10 border-l-4 border-l-blue-500 relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 p-8 opacity-20 pointer-events-none">
                        <Sparkles size={120} />
                    </div>
                    <h1 className="text-5xl font-black gradient-text pb-2">
                        ResumePilot AI
                    </h1>
                    <p className="text-slate-400 mt-4 text-lg max-w-2xl font-light">
                        Transform your profile. AI-powered analysis to bridge skill gaps and beat ATS filters.
                    </p>
                </motion.section>

                <section className="grid lg:grid-cols-2 gap-6">
                    <motion.div 
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 }}
                        className="glass-card p-8 flex flex-col"
                    >
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-3 bg-blue-500/20 rounded-xl text-blue-400">
                                <Upload size={24} />
                            </div>
                            <h2 className="text-2xl font-bold">1. Upload Resume</h2>
                        </div>
                        <label className="flex-1 border-2 border-dashed border-slate-700/50 bg-slate-900/50 hover:bg-slate-800/50 rounded-3xl p-10 text-center hover:border-blue-500 transition-all duration-300 cursor-pointer flex flex-col items-center justify-center group">
                            <div className="p-4 bg-slate-800 rounded-full mb-4 group-hover:scale-110 group-hover:bg-blue-500/20 transition-all duration-300">
                                <Upload size={32} className="text-slate-400 group-hover:text-blue-400" />
                            </div>
                            <p className="text-slate-300 font-medium">{file ? file.name : "Drag & Drop PDF or Click to Upload"}</p>
                            <p className="text-slate-500 text-sm mt-2">Supports PDF up to 5MB</p>
                            <input type="file" accept=".pdf" hidden onChange={handleFileChange} />
                        </label>
                    </motion.div>

                    <motion.div 
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                        className="glass-card p-8"
                    >
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-3 bg-green-500/20 rounded-xl text-green-400">
                                <Briefcase size={24} />
                            </div>
                            <h2 className="text-2xl font-bold">2. Target Role</h2>
                        </div>
                        
                        <div className="space-y-4">
                            <input 
                                type="text" 
                                placeholder="Job Title (e.g. Senior Frontend Developer)" 
                                value={jobTitle}
                                onChange={(e) => setJobTitle(e.target.value)}
                                className="w-full p-4 rounded-2xl bg-slate-900/80 border border-slate-700/50 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors" 
                            />
                            
                            <div className="relative">
                                <textarea 
                                    rows="4" 
                                    placeholder="Paste Job Description here or upload below..." 
                                    value={jobDescription}
                                    onChange={(e) => setJobDescription(e.target.value)}
                                    className="w-full p-4 rounded-2xl bg-slate-900/80 border border-slate-700/50 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors resize-none" 
                                />
                            </div>
                            
                            <label className="flex items-center justify-center gap-2 p-3 border border-slate-700/50 rounded-xl bg-slate-800/30 hover:bg-slate-700/50 cursor-pointer transition-colors text-sm text-slate-400 hover:text-slate-200">
                                <FileText size={16} />
                                {jdFile ? jdFile.name : "Upload Job Description File (PDF/DOCX)"}
                                <input type="file" accept=".pdf,.txt,.docx" hidden onChange={handleJdFileChange} />
                            </label>
                            
                            {errorMsg && <p className="text-red-400 text-sm mt-2 flex items-center gap-2"><AlertCircle size={16} />{errorMsg}</p>}

                            <button
                                onClick={handleAnalyze}
                                disabled={status === "analyzing"}
                                className={`primary-btn w-full mt-4 flex items-center justify-center gap-2 ${status === "analyzing" ? "opacity-70 cursor-not-allowed" : ""}`}
                            >
                                {status === "analyzing" ? (
                                    <>
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Analyzing with AI...
                                    </>
                                ) : "Run AI Analysis"}
                            </button>
                        </div>
                    </motion.div>
                </section>

                <AnimatePresence mode="wait">
                    {status === "idle" || status === "error" ? (
                        <motion.div 
                            key="idle"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="glass-card p-16 text-center border-dashed border-slate-700/50"
                        >
                            <div className="w-24 h-24 bg-slate-800/50 rounded-full flex items-center justify-center mx-auto mb-6">
                                <Sparkles size={48} className="text-slate-500" />
                            </div>
                            <h3 className="text-2xl font-bold text-slate-400">Ready for Analysis</h3>
                            <p className="text-slate-500 mt-2">Upload your resume and provide a job description to get started.</p>
                        </motion.div>
                    ) : status === "analyzing" ? (
                        <motion.div 
                            key="analyzing"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="glass-card p-16 text-center"
                        >
                            <div className="relative w-24 h-24 mx-auto mb-6">
                                <div className="absolute inset-0 border-4 border-blue-500/20 rounded-full"></div>
                                <div className="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                                <Sparkles size={32} className="absolute inset-0 m-auto text-blue-400 animate-pulse" />
                            </div>
                            <h3 className="text-2xl font-bold text-slate-200">AI is analyzing your profile...</h3>
                            <p className="text-slate-400 mt-2">Extracting skills, matching keywords, and scoring compatibility.</p>
                        </motion.div>
                    ) : (
                        <motion.div 
                            key="results"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="space-y-6"
                        >
                            <div className="grid lg:grid-cols-3 gap-6">
                                <motion.div 
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: 0.1 }}
                                    className="glass-card p-8 border-b-4 border-green-500 relative overflow-hidden flex flex-col items-center justify-center"
                                >
                                    <ScoreMeter score={results?.score || 82} label="Overall Match" />
                                </motion.div>
                                <motion.div 
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: 0.2 }}
                                    className="glass-card p-8 lg:col-span-2 flex flex-col justify-center"
                                >
                                    <p className="text-sm text-slate-400 uppercase tracking-widest font-semibold mb-4">Key Findings</p>
                                    <div className="grid sm:grid-cols-2 gap-4">
                                        <div className="bg-slate-900/50 p-4 rounded-2xl flex items-start gap-3 border border-green-500/20">
                                            <CheckCircle size={24} className="text-green-400 shrink-0" /> 
                                            <div>
                                                <h4 className="font-bold text-slate-200">Skills Aligned</h4>
                                                <p className="text-sm text-slate-400 mt-1">{results?.findings?.aligned || "React, JavaScript, Tailwind CSS"}</p>
                                            </div>
                                        </div>
                                        <div className="bg-slate-900/50 p-4 rounded-2xl flex items-start gap-3 border border-red-500/20">
                                            <AlertCircle size={24} className="text-red-400 shrink-0" /> 
                                            <div>
                                                <h4 className="font-bold text-slate-200">Missing Keywords</h4>
                                                <p className="text-sm text-slate-400 mt-1">{results?.findings?.missing || "Next.js, GraphQL, AWS"}</p>
                                            </div>
                                        </div>
                                    </div>
                                </motion.div>
                            </div>

                            {/* Suggestions Section */}
                            {results?.suggestions && results.suggestions.length > 0 && (
                                <motion.div 
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.25 }}
                                    className="glass-card p-8 border-l-4 border-l-yellow-500"
                                >
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="p-2 bg-yellow-500/20 rounded-lg text-yellow-500">
                                            <Lightbulb size={24} />
                                        </div>
                                        <h3 className="text-xl font-bold text-slate-200">Actionable Suggestions</h3>
                                    </div>
                                    <ul className="space-y-4">
                                        {results.suggestions.map((suggestion, index) => (
                                            <li key={index} className="flex gap-4 p-4 bg-slate-900/50 rounded-xl border border-slate-700/30">
                                                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center text-sm font-bold mt-0.5">
                                                    {index + 1}
                                                </div>
                                                <p className="text-slate-300">{suggestion}</p>
                                            </li>
                                        ))}
                                    </ul>
                                </motion.div>
                            )}
                            
                            <motion.div 
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.3 }}
                                className="grid lg:grid-cols-2 gap-6"
                            >
                                <RadarAnalysis data={results?.radarData} />
                                <ScoreBreakdown data={results?.scoreBreakdown} />
                            </motion.div>
                            
                            <motion.div 
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.4 }}
                                className="grid lg:grid-cols-2 gap-6"
                            >
                                <RoleMatchCard roleMatch={results?.roleMatch} />
                                <PredictedScoreCard currentScore={results?.score} />
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
}