import React, { useState, useEffect } from 'react';
import { Upload, FileText, ChevronRight, Download, Search, CheckCircle, AlertCircle, XCircle } from 'lucide-react';

export default function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [standards, setStandards] = useState({});
  const [selectedStandard, setSelectedStandard] = useState('IEEE-830-1998');

  useEffect(() => {
    fetch('/api/standards')
      .then(res => res.json())
      .then(data => setStandards(data))
      .catch(err => console.error(err));
  }, []);

  const handleUpload = async (e) => {
    if (!e.target.files[0]) return;
    setFile(e.target.files[0]);
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', e.target.files[0]);
    
    try {
      const res = await fetch(`/api/analyze?standard_id=${selectedStandard}`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message || "Failed to analyze document");
    } finally {
      setLoading(false);
    }
  };

  const matched = results ? Object.values(results.sections).filter(s => s.status === 'Matched').length : 0;
  const weak = results ? Object.values(results.sections).filter(s => s.status === 'Weak').length : 0;
  const missing = results ? Object.values(results.sections).filter(s => s.status === 'Missing').length : 0;
  const total = results ? Object.keys(results.sections).length : 0;

  return (
    <div className="min-h-screen bg-[#f5f4ef] flex flex-col items-center p-4">
      {/* Main Container Wrapper */}
      <div className="w-full max-w-[1400px] bg-white rounded-xl shadow-lg overflow-hidden flex flex-col min-h-[90vh]">
        
        {/* Top Navbar */}
        <div className="bg-[#1b2118] text-white flex items-center justify-between px-6 py-3">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
              <span className="text-xs font-bold">✨</span>
            </div>
            <h1 className="font-bold text-lg tracking-tight">SRS Builder</h1>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex flex-1 overflow-hidden">
          
          {/* Left Column (Main Form) */}
          <div className="w-2/3 p-8 overflow-y-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">SRS Configuration</h2>
            
            <div className="mb-8">
              <label className="block text-sm font-semibold text-[#7bc62d] mb-2 uppercase tracking-wide">Target Standard</label>
              <select 
                value={selectedStandard}
                onChange={(e) => setSelectedStandard(e.target.value)}
                className="w-full p-3 border border-gray-200 rounded-lg bg-gray-50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                {Object.keys(standards).map(k => (
                  <option key={k} value={k}>{standards[k].title}</option>
                ))}
              </select>
              <p className="mt-2 text-sm text-gray-500">
                {standards[selectedStandard]?.description}
              </p>
            </div>
            
            <div className="mb-8">
              <label className="block text-sm font-semibold text-[#7bc62d] mb-2 uppercase tracking-wide">Document Upload</label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-gray-100 transition p-8 text-center cursor-pointer relative">
                <input 
                  type="file" 
                  accept=".pdf,.docx,.txt"
                  onChange={handleUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <Upload size={32} className="mx-auto text-gray-400 mb-3" />
                <p className="font-medium text-gray-700">Click or drag file to upload</p>
                <p className="text-sm text-gray-500 mt-1">Supports PDF, DOCX, TXT</p>
              </div>
              {file && <p className="mt-2 text-sm font-medium text-green-600 flex items-center gap-2"><FileText size={16}/> {file.name}</p>}
              {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
            </div>

            {loading && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#7bc62d] mx-auto mb-4"></div>
                <p className="text-gray-500 font-medium">Analyzing semantics against {selectedStandard}...</p>
              </div>
            )}
          </div>
          
          {/* Right Column (Overview Panel) */}
          <div className="w-1/3 bg-white border-l border-gray-100 p-8 overflow-y-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Overview</h2>
            <p className="text-sm text-gray-500 mb-8">Welcome to your SRS document review!</p>
            
            {results ? (
              <>
                {/* Circular Score Ring */}
                <div className="flex flex-col items-center mb-8">
                  <div className="relative w-40 h-40 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#f3f4f6" strokeWidth="10" />
                      <circle 
                        cx="50" cy="50" r="45" fill="none" 
                        stroke="#7bc62d" strokeWidth="10" 
                        strokeDasharray="283" 
                        strokeDashoffset={283 - (283 * results.score) / 100}
                        className="transition-all duration-1000 ease-out"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-4xl font-bold text-gray-900">{results.score}%</span>
                    </div>
                  </div>
                  <p className="text-sm font-semibold text-gray-700 mt-4">Your document scored {results.score} out of 100</p>
                </div>
                
                {/* Metric Cards Grid */}
                <div className="grid grid-cols-2 gap-4 mb-8">
                  <div className="border border-gray-100 rounded-xl p-4 shadow-sm">
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Matched</div>
                    <div className="flex items-center justify-between">
                      <span className="text-3xl font-bold text-gray-900">{matched}</span>
                      <span className="text-[10px] font-bold px-2 py-1 bg-green-100 text-green-700 rounded uppercase">Excellent</span>
                    </div>
                  </div>
                  <div className="border border-gray-100 rounded-xl p-4 shadow-sm">
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Weak</div>
                    <div className="flex items-center justify-between">
                      <span className="text-3xl font-bold text-gray-900">{weak}</span>
                      <span className="text-[10px] font-bold px-2 py-1 bg-orange-100 text-orange-700 rounded uppercase">Average</span>
                    </div>
                  </div>
                  <div className="border border-gray-100 rounded-xl p-4 shadow-sm">
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Missing</div>
                    <div className="flex items-center justify-between">
                      <span className="text-3xl font-bold text-gray-900">{missing}</span>
                      <span className="text-[10px] font-bold px-2 py-1 bg-red-100 text-red-700 rounded uppercase">Poor</span>
                    </div>
                  </div>
                  <div className="border border-gray-100 rounded-xl p-4 shadow-sm">
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Total Sections</div>
                    <div className="flex items-center justify-between">
                      <span className="text-3xl font-bold text-gray-900">{total}</span>
                      <span className="text-[10px] font-bold px-2 py-1 bg-blue-100 text-blue-700 rounded uppercase">Good</span>
                    </div>
                  </div>
                </div>

                {/* Detailed List */}
                <div className="space-y-4">
                  {Object.entries(results.sections).map(([id, sec]) => (
                    <div key={id} className="flex items-center justify-between p-3 border-b border-gray-50 last:border-0 hover:bg-gray-50 rounded transition">
                      <div className="flex items-center gap-3">
                        {sec.status === 'Matched' ? <CheckCircle size={18} className="text-green-500" /> : 
                         sec.status === 'Weak' ? <AlertCircle size={18} className="text-orange-500" /> :
                         <XCircle size={18} className="text-red-500" />}
                        <span className="text-sm font-medium text-gray-700 truncate w-40" title={sec.name}>{sec.name}</span>
                      </div>
                      <span className={`text-sm font-bold ${sec.status === 'Matched' ? 'text-green-600' : sec.status === 'Weak' ? 'text-orange-500' : 'text-red-500'}`}>
                        {sec.status === 'Matched' ? '10/10' : sec.status === 'Weak' ? '5/10' : '0/10'}
                      </span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-center">
                <FileText size={48} className="text-gray-200 mb-4" />
                <p className="text-gray-500 font-medium">Upload a document on the left to generate your overview report.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
