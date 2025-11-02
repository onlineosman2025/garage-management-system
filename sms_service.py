#!/usr/bin/env python3
"""
SMS Notification Service for Garage Management System
Twilio SMS integration (requires: pip install twilio)
"""
import json
from pathlib import Path
from datetime import datetime

# SMS configuration
SMS_CONFIG = {
    'twilio_account_sid': '',  # Set your Twilio Account SID
    'twilio_auth_token': '',  # Set your Twilio Auth Token
    'twilio_phone_number': '',  # Your Twilio phone number
    'enabled': False
}

def load_sms_config():
    """Load SMS configuration from file"""
    config_file = Path(__file__).parent / 'sms_config.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            SMS_CONFIG.update(config)
    return SMS_CONFIG

def save_sms_config(config):
    """Save SMS configuration to file"""
    config_file = Path(__file__).parent / 'sms_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    SMS_CONFIG.update(config)

def send_sms(to_phone, message):
    """
    Send SMS message
    
    Args:
        to_phone: Recipient phone number (with country code)
        message: SMS message text
    
    Returns:
        dict: Success status and message SID or error
    """
    config = load_sms_config()
    
    if not config.get('enabled'):
        print("[SMS] SMS service not enabled")
        return {'error': 'SMS service not enabled'}
    
    if not config.get('twilio_account_sid') or not config.get('twilio_auth_token'):
        print("[SMS] Twilio not configured")
        return {'error': 'Twilio not configured. Please set account SID and auth token.'}
    
    try:
        from twilio.rest import Client
        
        client = Client(config['twilio_account_sid'], config['twilio_auth_token'])
        
        message = client.messages.create(
            body=message,
            from_=config['twilio_phone_number'],
            to=to_phone
        )
        
        print(f"[SMS] SMS sent to {to_phone}: {message.sid}")
        return {
            'success': True,
            'message_sid': message.sid,
            'to': to_phone,
            'status': message.status
        }
        
    except ImportError:
        return {'error': 'Twilio library not installed. Run: pip install twilio'}
    except Exception as e:
        print(f"[SMS] Error sending SMS: {str(e)}")
        return {'error': str(e)}

def send_job_status_notification(customer_phone, customer_name, job_id, status):
    """Send job status update SMS"""
    status_messages = {
        'pending': f"Hi {customer_name}, your service request #{job_id} has been received and is pending review.",
        'in_progress': f"Hi {customer_name}, your vehicle service #{job_id} is now in progress. We'll notify you when it's ready!",
        'completed': f"Great news {customer_name}! Your vehicle service #{job_id} is completed and ready for pickup.",
        'cancelled': f"Hi {customer_name}, service request #{job_id} has been cancelled. Please contact us for details."
    }
    
    message = status_messages.get(status, f"Job #{job_id} status updated to: {status}")
    return send_sms(customer_phone, message)

def send_invoice_reminder(customer_phone, customer_name, invoice_id, amount):
    """Send invoice payment reminder"""
    message = f"Hi {customer_name}, friendly reminder: Invoice #{invoice_id} for AED {amount:.2f} is pending. Pay online or visit us. Thank you!"
    return send_sms(customer_phone, message)

def send_payment_confirmation(customer_phone, customer_name, invoice_id, amount):
    """Send payment confirmation SMS"""
    message = f"Payment received! Thank you {customer_name}. Invoice #{invoice_id} for AED {amount:.2f} has been paid. Receipt sent to your email."
    return send_sms(customer_phone, message)

def send_appointment_reminder(customer_phone, customer_name, appointment_date, appointment_time):
    """Send appointment reminder"""
    message = f"Hi {customer_name}, reminder: Your service appointment is on {appointment_date} at {appointment_time}. See you soon!"
    return send_sms(customer_phone, message)

def send_custom_message(customer_phone, message):
    """Send custom SMS message"""
    return send_sms(customer_phone, message)

def get_sms_status():
    """Get SMS service status"""
    config = load_sms_config()
    return {
        'enabled': config.get('enabled', False),
        'configured': bool(config.get('twilio_account_sid') and config.get('twilio_auth_token')),
        'phone_number': config.get('twilio_phone_number', 'Not set')
    }

# Mock SMS for testing (when Twilio not configured)
def send_mock_sms(to_phone, message):
    """Send mock SMS for testing"""
    mock_sid = f"SM{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"[SMS MOCK] To: {to_phone}")
    print(f"[SMS MOCK] Message: {message}")
    
    return {
        'success': True,
        'message_sid': mock_sid,
        'to': to_phone,
        'status': 'sent',
        'mock': True,
        'message': 'This is a mock SMS. Configure Twilio for real SMS.'
    }

if __name__ == "__main__":
    print("SMS Service Module")
    print("Requires: pip install twilio")
    print("\nConfiguration:")
    print("1. Sign up at https://www.twilio.com/")
    print("2. Get Account SID, Auth Token, and Phone Number")
    print("3. Save in sms_config.json")
    print("4. Test with send_sms()")
