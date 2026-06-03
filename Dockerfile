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
COPY start.py .

# Expose default port (Render overrides with $PORT)
EXPOSE 8000

# start.py reads $PORT at runtime
CMD ["python", "start.py"]
