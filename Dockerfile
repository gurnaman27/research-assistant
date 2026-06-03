FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ agents/
COPY api/ api/
COPY cache/ cache/
COPY graph/ graph/
COPY rag/ rag/
COPY static/ static/

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
