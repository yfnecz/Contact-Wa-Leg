FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Set work directory
WORKDIR /app
ENV AI_CACHE_DB_PATH=/data/ai_cache.db

# Install dependencies
RUN apt-get update && apt-get install -y build-essential gcc sqlite3
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 10000

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]