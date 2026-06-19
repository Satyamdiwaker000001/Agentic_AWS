import { useState, useRef } from 'react';
import { uploadFileForChunking } from './api';

function App() {
  const [file, setFile] = useState(null);
  const [method, setMethod] = useState('fixed'); // 'fixed' | 'recursive'
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
      setError(err.message || 'An error occurred while uploading.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container animate-fade">
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>
          <span className="gradient-text">SmartChunk AI</span>
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>
          Intelligent Document Parsing & Chunking Engine
        </p>
      </div>

      <div className="glass-panel" style={{ maxWidth: '800px', margin: '0 auto' }}>
        
        {/* File Upload Area */}
        <div 
          className="upload-area" 
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
          <div style={{ pointerEvents: 'none' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📁</div>
            {file ? (
              <h3 style={{ color: 'var(--primary)' }}>{file.name}</h3>
            ) : (
              <>
                <h3>Drag & Drop your document here</h3>
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
            className={`switcher-btn ${method === 'fixed' ? 'active' : ''}`}
            onClick={() => setMethod('fixed')}
          >
            Fixed Chunking
          </button>
          <button 
            className={`switcher-btn ${method === 'recursive' ? 'active' : ''}`}
            onClick={() => setMethod('recursive')}
          >
            Recursive Chunking
          </button>
        </div>

        {error && <div className="error-msg">{error}</div>}

        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button 
            className="btn" 
            onClick={handleSubmit} 
            disabled={!file || loading}
            style={{ width: '100%', padding: '1rem', fontSize: '1.2rem' }}
          >
            {loading ? 'Processing Document...' : 'Generate Chunks'}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className="animate-fade" style={{ marginTop: '3rem' }}>
          <div className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>Results <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 'normal' }}>({result.method} method)</span></h2>
            <div style={{ background: 'rgba(168, 85, 247, 0.2)', padding: '0.5rem 1rem', borderRadius: '8px', color: '#e9d5ff' }}>
              <strong>{result.total_chunks}</strong> chunks generated
            </div>
          </div>

          <div className="chunks-grid">
            {result.chunks.map((chunk, index) => (
              <div key={index} className="chunk-card" style={{ animationDelay: `${index * 0.05}s` }}>
                <div className="chunk-header">
                  <span className="chunk-badge">Chunk {index + 1}</span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{chunk.length} chars</span>
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
  );
}

export default App;
