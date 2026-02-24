FROM python:3.11-slim

WORKDIR /app

# Install system deps (if needed) and pip packages
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy project
COPY . .

ENV PYTHONUNBUFFERED=1

# Default command: change this to your actual entrypoint/module
CMD ["python", "-m", "blue_ocean_engine"]
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p config data/templates

EXPOSE 5000

CMD ["python", "dashboard.py"]
