# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app_root

# Copy requirements first (better Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project (includes app/, outputs/, tests/)
COPY . .

# Expose port
EXPOSE 8000

# Start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
