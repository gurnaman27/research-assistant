FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model so it's baked into the image
# (avoids HuggingFace download failures at runtime on cloud environments)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

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
