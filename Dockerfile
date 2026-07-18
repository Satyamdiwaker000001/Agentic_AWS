# Use official Python image as base (CPU version)
FROM python:3.11-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "SRS_Compliance_Analyzer/app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
