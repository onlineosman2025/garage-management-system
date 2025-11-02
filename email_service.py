#!/usr/bin/env python3
"""
Email Notification Service for Garage Management System
Sends invoice emails to customers
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import json

# Email configuration (can be moved to config file)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',  # Will be set by user
    'sender_password': '',  # Will be set by user
    'sender_name': 'Garage Management System'
}

def load_email_config():
    """Load email configuration from file"""
    config_file = Path(__file__).parent / 'email_config.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            EMAIL_CONFIG.update(config)
    return EMAIL_CONFIG

def save_email_config(config):
    """Save email configuration to file"""
    config_file = Path(__file__).parent / 'email_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    EMAIL_CONFIG.update(config)

def send_email(to_email, subject, html_body, attachments=None):
    """
    Send email with optional attachments
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML content of email
        attachments: List of file paths to attach
    
    Returns:
        True if successful, False otherwise
    """
    config = load_email_config()
    
    if not config.get('sender_email') or not config.get('sender_password'):
        print("[EMAIL] Email not configured. Please set sender_email and sender_password")
        return False
    
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['From'] = f"{config['sender_name']} <{config['sender_email']}>"
        message['To'] = to_email
        message['Subject'] = subject
        
        # Add HTML body
        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)
        
        # Add attachments if any
        if attachments:
            for file_path in attachments:
                if Path(file_path).exists():
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {Path(file_path).name}'
                        )
                        message.attach(part)
        
        # Send email
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['sender_email'], config['sender_password'])
            server.send_message(message)
        
        print(f"[EMAIL] Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL] Failed to send email: {str(e)}")
        return False

def generate_invoice_email_html(invoice, customer, garage_info):
    """Generate HTML email for invoice"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border: 1px solid #ddd;
            }}
            .invoice-details {{
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
            }}
            .detail-row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #f0f0f0;
            }}
            .detail-row:last-child {{
                border-bottom: none;
            }}
            .label {{
                font-weight: bold;
                color: #666;
            }}
            .value {{
                color: #333;
            }}
            .total {{
                font-size: 1.3em;
                font-weight: bold;
                color: #667eea;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 0.9em;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏪 {garage_info.get('name', '')}</h1>
            <p>{garage_info.get('address', '')}</p>
        </div>
        
        <div class="content">
            <h2>Invoice #{invoice['id']}</h2>
            <p>Dear {customer['name']},</p>
            <p>Thank you for your business! Please find your invoice details below:</p>
            
            <div class="invoice-details">
                <div class="detail-row">
                    <span class="label">Invoice Number:</span>
                    <span class="value">#{invoice['id']}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Date:</span>
                    <span class="value">{invoice['created_at']}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Due Date:</span>
                    <span class="value">{invoice.get('due_date', 'Upon Receipt')}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Description:</span>
                    <span class="value">{invoice.get('description', 'Service charges')}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Amount:</span>
                    <span class="value">AED {invoice['amount']:.2f}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Tax ({invoice['tax_rate']}%):</span>
                    <span class="value">AED {invoice['tax_amount']:.2f}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Total Amount:</span>
                    <span class="value total">AED {invoice['total_amount']:.2f}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Status:</span>
                    <span class="value" style="color: {'green' if invoice['status'] == 'paid' else 'orange'}; font-weight: bold;">
                        {invoice['status'].upper()}
                    </span>
                </div>
            </div>
            
            {f'<p style="color: green; font-weight: bold;">✓ This invoice has been paid on {invoice["paid_at"]}</p>' if invoice['status'] == 'paid' else '<p>Please make payment at your earliest convenience.</p>'}
            
            <center>
                <a href="http://localhost:3000/invoices.html" class="button">View Invoice Online</a>
            </center>
        </div>
        
        <div class="footer">
            <p>Thank you for choosing {garage_info.get('name', '')}!</p>
            <p>If you have any questions, please don't hesitate to contact us.</p>
        </div>
    </body>
    </html>
    """
    return html

def send_invoice_email(invoice, customer, garage_info=None):
    """Send invoice email to customer"""
    if not garage_info:
        garage_info = {'name': '', 'address': ''}
    
    subject = f"Invoice #{invoice['id']} from {garage_info['name']}"
    html_body = generate_invoice_email_html(invoice, customer, garage_info)
    
    return send_email(customer['email'], subject, html_body)

def send_payment_confirmation_email(invoice, customer, garage_info=None):
    """Send payment confirmation email"""
    if not garage_info:
        garage_info = {'name': '', 'address': ''}
    
    subject = f"Payment Received - Invoice #{invoice['id']}"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border: 1px solid #ddd;
            }}
            .success-icon {{
                font-size: 48px;
                text-align: center;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>✓ Payment Received</h1>
        </div>
        
        <div class="content">
            <div class="success-icon">✓</div>
            <h2>Thank You, {customer['name']}!</h2>
            <p>We have received your payment for Invoice #{invoice['id']}.</p>
            <p><strong>Amount Paid:</strong> AED {invoice['total_amount']:.2f}</p>
            <p><strong>Payment Date:</strong> {invoice['paid_at']}</p>
            <p>Your receipt has been recorded in our system.</p>
            <p>We appreciate your business and look forward to serving you again!</p>
        </div>
        
        <div style="text-align: center; padding: 20px; color: #666; font-size: 0.9em;">
            <p>{garage_info['name']}</p>
            <p>{garage_info.get('address', '')}</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(customer['email'], subject, html_body)

# Test function
if __name__ == "__main__":
    print("Email Service Module")
    print("Configure email settings using save_email_config()")
