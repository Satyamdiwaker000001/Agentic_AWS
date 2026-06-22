document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');
    
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const searchResults = document.getElementById('search-results');

    // API URL matches the host since it's mounted, 
    // but if running via VS Code Live Server (port 5500), point to the local FastAPI backend
    const API_URL = (window.location.port === '5500' || window.location.port === '5501') 
        ? 'http://127.0.0.1:8000' 
        : window.location.origin;

    // --- Drag and Drop Logic ---
    dropZone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type !== 'application/pdf') {
                showStatus('Please upload a PDF file.', 'error');
                return;
            }
            uploadFile(file);
        }
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        showStatus(`Uploading and processing ${file.name}...`, 'loading');

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Upload failed');
            }

            if (data.status === 'skipped') {
                showStatus('Document already exists in memory!', 'success');
            } else {
                showStatus(`Success! Generated ${data.num_chunks} memory chunks.`, 'success');
            }

        } catch (error) {
            console.error('Error:', error);
            showStatus(error.message, 'error');
        }
    }

    function showStatus(message, type) {
        uploadStatus.textContent = message;
        uploadStatus.className = `status-msg ${type}`;
        setTimeout(() => {
            if (type !== 'loading') {
                uploadStatus.textContent = '';
                uploadStatus.className = 'status-msg';
            }
        }, 5000);
    }

    // --- Search Logic ---
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    async function performSearch() {
        const query = searchInput.value.trim();
        if (!query) return;

        // Show loading state
        searchResults.innerHTML = '<div class="empty-state" style="animation: pulse 1.5s infinite; color: var(--accent-color)">Searching memory...</div>';

        try {
            const response = await fetch(`${API_URL}/search?query=${encodeURIComponent(query)}&n_results=5`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Search failed');
            }

            renderResults(data);

        } catch (error) {
            console.error('Error:', error);
            searchResults.innerHTML = `<div class="empty-state error" style="color: #ef4444;">Search failed: ${error.message}</div>`;
        }
    }

    function renderResults(data) {
        const results = data.results;
        const aiAnswer = data.synthesized_answer;

        if (!results || results.length === 0) {
            searchResults.innerHTML = '<div class="empty-state">No matching memories found. Try uploading a document!</div>';
            return;
        }

        searchResults.innerHTML = '';
        
        // Render AI Synthesized Answer if available
        if (aiAnswer) {
            const agentCard = document.createElement('div');
            agentCard.className = 'agent-response';
            agentCard.innerHTML = `
                <div class="agent-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                    Agent AI Synthesis
                </div>
                <div class="agent-text">${aiAnswer.replace(/\n/g, '<br>')}</div>
            `;
            searchResults.appendChild(agentCard);
            
            const divider = document.createElement('div');
            divider.className = 'source-divider';
            divider.textContent = 'Retrieved Source Chunks';
            searchResults.appendChild(divider);
        }

        results.forEach((result, index) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.style.animationDelay = `${index * 0.1}s`;
            
            // Format score (ChromaDB L2 distance -> pseudo confidence percentage for UI)
            const distance = parseFloat(result.score);
            let confidence = Math.max(0, 100 - (distance * 40)); 
            if(confidence > 99) confidence = 99;
            
            card.innerHTML = `
                <div class="result-header">
                    <span>${result.metadata.filename || 'Document ID: ' + result.document_id}</span>
                    <span class="score">${confidence.toFixed(1)}% Match</span>
                </div>
                <div class="result-text">${highlightText(result.text, searchInput.value)}</div>
            `;
            searchResults.appendChild(card);
        });
    }

    function highlightText(text, query) {
        if (!query) return text;
        const terms = query.toLowerCase().split(/\s+/).filter(t => t.length > 2);
        let highlighted = text;
        
        terms.forEach(term => {
            const regex = new RegExp(`(${term})`, 'gi');
            highlighted = highlighted.replace(regex, '<span style="background: rgba(99, 102, 241, 0.3); color: #a5b4fc; padding: 0 2px; border-radius: 2px;">$1</span>');
        });
        
        return highlighted;
    }
});
