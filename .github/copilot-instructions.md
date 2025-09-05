# VPS Web Application - Flask + Docker + Traefik

## Project Overview
This is a Flask web application running in Docker containers, orchestrated via docker-compose with Traefik as reverse proxy. The application serves bluedjedi.com and integrates with multiple services.

## Architecture
- **Flask App**: Main web application (port 5000)
- **Traefik**: Reverse proxy with SSL termination (ports 80/443)
- **Network**: Custom 'vps' Docker network
- **Management**: Uses custom 'dok' script for orchestration

## Tech Stack
- Python/Flask for web framework
- Docker & docker-compose for containerization
- Traefik for reverse proxy and SSL
- Custom bash scripts for deployment

## File Structure
- `/opt/vps/web/` - Main application directory
- `docker-compose.yml` - Service definitions
- `app.py` - Flask application entry point
- `requirements.txt` - Python dependencies
- Custom 'dok' script for container management

## Development Standards
- Use environment variables for configuration
- Follow Flask best practices for routing
- Maintain Docker health checks
- Use semantic commit messages
- Test locally before deployment via 'dok' commands

## Deployment Commands
- `dok web ud` - Deploy web service
- `dok web r` - Restart web service  
- `dok web lf` - Follow logs
- `dok ps` - Check container status
