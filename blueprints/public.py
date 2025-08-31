"""
Public Blueprint
Handles all public-facing routes
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

# Create blueprint
public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Main public page"""
    return render_template('pages/index.html')

@public_bp.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        # Get form data
        name = request.form.get('name', 'ANONYMOUS')
        email = request.form.get('email', 'NO EMAIL PROVIDED')
        message = request.form.get('message', '')
        
        # Validate message
        if not message.strip():
            return jsonify({
                'status': 'error',
                'message': 'MESSAGE IS REQUIRED'
            }), 400
        
        # Format message for Telegram
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        telegram_message = f"""🔷 NEW CONTACT FROM BLUEDJEDI.COM

📅 TIME: {timestamp}
👤 NAME: {name}
📧 EMAIL: {email}
💬 MESSAGE:
{message}

---
SENT FROM THE TEMPLE OF THE BLUE DJEDI"""

        # Try to send to Telegram
        try:
            # Read secrets from Docker mounted files
            with open(current_app.config['TELEGRAM_BOT_TOKEN_FILE'], 'r') as f:
                bot_token = f.read().strip()
            with open(current_app.config['TELEGRAM_USER_ID_FILE'], 'r') as f:
                chat_id = f.read().strip()
            
            # Send message to Telegram
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            telegram_data = {
                'chat_id': chat_id,
                'text': telegram_message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(telegram_url, json=telegram_data, timeout=10)
            
            if response.status_code == 200:
                logger.info("Contact form message sent to Telegram successfully")
            else:
                logger.error(f"Telegram API error: {response.status_code}")
                # Log to file as fallback
                _log_message_to_file(name, email, message, timestamp)
                
        except FileNotFoundError:
            logger.warning("Telegram secrets not found, logging to file")
            _log_message_to_file(name, email, message, timestamp)
        except Exception as e:
            logger.error(f"Error sending to Telegram: {e}")
            _log_message_to_file(name, email, message, timestamp)
        
        # Always return success to user
        return jsonify({
            'status': 'success',
            'message': 'THANK YOU FOR YOUR MESSAGE! WE WILL GET BACK TO YOU SOON.'
        })
        
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'FAILED TO SEND MESSAGE. PLEASE TRY AGAIN.'
        }), 500

def _log_message_to_file(name, email, message, timestamp):
    """Fallback to log messages to file"""
    try:
        with open('/tmp/contact_messages.log', 'a') as f:
            log_message = f"[{timestamp}] CONTACT FORM:\nNAME: {name}\nEMAIL: {email}\nMESSAGE: {message}\n{'-'*50}\n"
            f.write(log_message)
    except Exception as e:
        logger.error(f"Failed to write to log file: {e}")
