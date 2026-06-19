import { useState, useRef } from 'react';
import { uploadFileForChunking } from './api';
import './App.css'; // if there's any specific css
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [method, setMethod] = useState('semantic'); // 'fixed' | 'recursive' | 'semantic'
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError('');
      setResult(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
      setError('');
      setResult(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await uploadFileForChunking(file, method);
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred while processing the document.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="background-blobs">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>
      
      <div className="container animate-fade">
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <h1 style={{ fontSize: '3.5rem', marginBottom: '0.75rem' }} className="title-glow">
            <span className="gradient-text">SmartChunk AI</span>
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.25rem', maxWidth: '600px', margin: '0 auto', lineHeight: '1.6' }}>
            Intelligent Document Parsing & Semantic Chunking Engine
          </p>
        </div>

        <div className="glass-panel" style={{ maxWidth: '850px', margin: '0 auto' }}>
          
          {/* File Upload Area */}
          <div 
            className={`upload-area ${file ? 'active' : ''}`} 
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              accept=".txt,.pdf,.docx" 
            />
            <div style={{ pointerEvents: 'none', position: 'relative', zIndex: 2 }}>
              <div className="upload-icon">
                {file ? '📄' : '📤'}
              </div>
              {file ? (
                <>
                  <h3 style={{ color: '#e0e7ff', fontSize: '1.5rem', marginBottom: '0.5rem' }}>{file.name}</h3>
                  <p style={{ color: 'var(--accent)', fontSize: '0.9rem', fontWeight: '500' }}>Click or drop to replace file</p>
                </>
              ) : (
                <>
                  <h3 style={{ fontSize: '1.5rem', color: 'var(--text-main)', marginBottom: '0.5rem' }}>Drag & Drop your document here</h3>
                  <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                    Supports .txt, .pdf, .docx
                  </p>
                </>
              )}
            </div>
          </div>

          {/* Method Switcher */}
          <div className="switcher">
            <button 
              className={`switcher-btn ${method === 'semantic' ? 'active' : ''}`}
              onClick={() => setMethod('semantic')}
            >
              ✨ Semantic
            </button>
            <button 
              className={`switcher-btn ${method === 'recursive' ? 'active' : ''}`}
              onClick={() => setMethod('recursive')}
            >
              Recursive
            </button>
            <button 
              className={`switcher-btn ${method === 'fixed' ? 'active' : ''}`}
              onClick={() => setMethod('fixed')}
            >
              Fixed
            </button>
          </div>

          {error && (
            <div className="error-msg">
              <span>⚠️</span> {error}
            </div>
          )}

          <div style={{ textAlign: 'center', marginTop: '2.5rem' }}>
            <button 
              className="btn" 
              onClick={handleSubmit} 
              disabled={!file || loading}
              style={{ width: '100%', padding: '1.2rem', fontSize: '1.25rem', maxWidth: '400px' }}
            >
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                  <svg className="animate-spin" style={{ width: '24px', height: '24px', animation: 'spin 1s linear infinite' }} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle style={{ opacity: 0.25 }} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path style={{ opacity: 0.75 }} fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing Document...
                </span>
              ) : 'Generate AI Chunks'}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="animate-fade" style={{ marginTop: '4rem' }}>
            <div className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1.5rem 2.5rem', marginBottom: '2rem' }}>
              <div>
                <h2 style={{ fontSize: '1.8rem', margin: 0 }}>Processing Results</h2>
                <p style={{ color: 'var(--text-muted)', marginTop: '0.25rem', fontSize: '0.9rem' }}>
                  Method applied: <span style={{ color: 'var(--accent)', fontWeight: '600', textTransform: 'capitalize' }}>{result.method}</span>
                </p>
              </div>
              <div className="stats-badge">
                <span className="stats-number">{result.total_chunks}</span> chunks generated
              </div>
            </div>

            <div className="chunks-grid">
              {result.chunks.map((chunk, index) => (
                <div key={index} className="chunk-card" style={{ animationDelay: `${index * 0.08}s` }}>
                  <div className="chunk-header">
                    <span className="chunk-badge">Chunk {index + 1}</span>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '500' }}>
                      {chunk.length} chars
                    </span>
                  </div>
                  <div className="chunk-content">
                    {chunk}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <style dangerouslySetInnerHTML={{__html: `
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .animate-spin { animation: spin 1s linear infinite; }
      `}} />
    </>
  );
}

export default App;
