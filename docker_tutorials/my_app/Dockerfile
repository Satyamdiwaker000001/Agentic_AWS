# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining project files
COPY . .

# Command to run when the container starts
CMD ["python", "app.py"]