FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Note: In production, use environment variables instead of copying service account files
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Expose the port that Flask runs on
EXPOSE 8080

# Run the Flask application
CMD ["python", "app.py"]
