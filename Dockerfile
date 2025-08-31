#cat > /opt/vps/web/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system utilities and Node.js
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy package files first for better caching
COPY package*.json ./

# Install Node dependencies
RUN npm install

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Build Tailwind CSS
RUN npm run build-css

# Expose port
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
#EOF