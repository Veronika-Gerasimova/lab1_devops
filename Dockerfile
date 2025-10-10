# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY test_app.py .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check (use Python, no curl dependency)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python - <<'PY'
import sys, urllib.request
try:
    with urllib.request.urlopen('http://localhost:5000/', timeout=2) as r:
        sys.exit(0 if r.status == 200 else 1)
except Exception:
    sys.exit(1)
PY

# Run the application
CMD ["python", "app.py"]
