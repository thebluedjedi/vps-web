# Blue Djedi Web Application

Flask web application serving the Blue Djedi Temple website and admin dashboard.

## Services Provided
- **Public Website**: `bluedjedi.com` - Landing page with social links and contact form
- **Admin Dashboard**: `admin.bluedjedi.com` - VPS monitoring with CPU, memory, storage metrics
- **API Endpoints**: System status and Prometheus proxy endpoints

## Architecture
- **Flask** backend with blueprint structure
- **Tailwind CSS** for responsive styling
- **Chart.js** for admin dashboard metrics visualization
- **Prometheus** integration for system monitoring
- **Telegram** notifications for contact form submissions
- **Traefik** reverse proxy with SSL termination

## Secrets Management
All sensitive data stored in `/opt/key/` directory and mounted as Docker secrets:
- `flask_secret_key.txt` - Flask session encryption key
- `telegram_bot_token.txt` - Telegram bot API token
- `telegram_user_id.txt` - Authorized Telegram user ID

## Deployment
```bash
# Deploy with existing secrets
docker-compose up -d

# View logs
docker logs vps-web -f
File Structure
/opt/vps/web/
├── blueprints/
│   ├── admin.py      # Admin dashboard routes and metrics
│   ├── api.py        # API endpoints and Prometheus proxy
│   └── public.py     # Public website and contact form
├── templates/
│   ├── pages/        # Main page templates
│   └── components/   # Reusable template components
├── static/css/       # Compiled Tailwind CSS
├── utils/
│   ├── prometheus.py # Prometheus query utilities
│   └── system.py     # System information helpers
├── config.py         # Flask configuration with secrets integration
├── docker-compose.yml # Container orchestration
└── app.py           # Flask application entry point# Last updated: Mon Sep  1 10:17:57 AM CEST 2025
