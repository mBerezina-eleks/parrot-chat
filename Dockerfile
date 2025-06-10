# Use an official Python base image
FROM python:3.11-slim
 
WORKDIR /app
 
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    sqlite3 \
    && sqlite3 --version \
    && rm -rf /var/lib/apt/lists/*
 
# Install uv package manager
RUN pip install --no-cache-dir uv
 
COPY pyproject.toml uv.lock ./
 
# Install dependencies with uv
RUN uv sync --frozen
 
# Copy project files
COPY . .
 
EXPOSE 8000
 
# Run the Streamlit app
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port", "8000", "--server.address", "0.0.0.0"]