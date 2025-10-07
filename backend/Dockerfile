# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install uv and dependencies
RUN pip install uv && uv venv && uv pip install --system -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["uv", "run", "python", "app.py"]