# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables
ENV PORT=8000
ENV MCP_TRANSPORT=streamable-http

# Expose port 8000
EXPOSE 8000

# Run the server directly
CMD ["python", "server.py"]