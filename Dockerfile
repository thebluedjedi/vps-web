FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install waitress for production WSGI server
RUN pip install waitress

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run with waitress instead of Flask dev server
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]