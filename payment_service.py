#!/usr/bin/env python3
"""
Payment Gateway Integration for Garage Management System
Stripe payment processing (requires: pip install stripe)
"""
import json
from pathlib import Path
from datetime import datetime

# Payment configuration
PAYMENT_CONFIG = {
    'stripe_secret_key': '',  # Set your Stripe secret key
    'stripe_publishable_key': '',  # Set your Stripe publishable key
    'currency': 'AED',
    'payment_methods': ['card'],
    'webhook_secret': ''  # For webhook verification
}

def load_payment_config():
    """Load payment configuration from file"""
    config_file = Path(__file__).parent / 'payment_config.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            PAYMENT_CONFIG.update(config)
    return PAYMENT_CONFIG

def save_payment_config(config):
    """Save payment configuration to file"""
    config_file = Path(__file__).parent / 'payment_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    PAYMENT_CONFIG.update(config)

def create_payment_intent(amount, currency='AED', description='', metadata=None):
    """
    Create a Stripe payment intent
    
    Args:
        amount: Amount in smallest currency unit (fils for AED)
        currency: Currency code
        description: Payment description
        metadata: Additional metadata
    
    Returns:
        dict: Payment intent details or error
    """
    try:
        import stripe
        config = load_payment_config()
        
        if not config.get('stripe_secret_key'):
            return {'error': 'Stripe not configured. Please set API keys.'}
        
        stripe.api_key = config['stripe_secret_key']
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to fils
            currency=currency.lower(),
            description=description,
            metadata=metadata or {},
            automatic_payment_methods={'enabled': True}
        )
        
        print(f"[PAYMENT] Created payment intent: {intent.id}")
        return {
            'success': True,
            'payment_intent_id': intent.id,
            'client_secret': intent.client_secret,
            'amount': amount,
            'currency': currency,
            'status': intent.status
        }
        
    except ImportError:
        return {'error': 'Stripe library not installed. Run: pip install stripe'}
    except Exception as e:
        print(f"[PAYMENT] Error creating payment intent: {str(e)}")
        return {'error': str(e)}

def confirm_payment(payment_intent_id):
    """Confirm a payment intent"""
    try:
        import stripe
        config = load_payment_config()
        stripe.api_key = config['stripe_secret_key']
        
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        return {
            'success': True,
            'payment_intent_id': intent.id,
            'status': intent.status,
            'amount': intent.amount / 100,
            'currency': intent.currency.upper()
        }
        
    except ImportError:
        return {'error': 'Stripe library not installed'}
    except Exception as e:
        return {'error': str(e)}

def create_invoice_payment(invoice_id, invoice_amount, customer_email):
    """Create payment for an invoice"""
    metadata = {
        'invoice_id': invoice_id,
        'customer_email': customer_email,
        'created_at': datetime.now().isoformat()
    }
    
    description = f"Payment for Invoice #{invoice_id}"
    
    return create_payment_intent(
        amount=invoice_amount,
        currency='AED',
        description=description,
        metadata=metadata
    )

def process_webhook(payload, signature):
    """Process Stripe webhook events"""
    try:
        import stripe
        config = load_payment_config()
        
        if not config.get('webhook_secret'):
            return {'error': 'Webhook secret not configured'}
        
        stripe.api_key = config['stripe_secret_key']
        
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, signature, config['webhook_secret']
        )
        
        # Handle different event types
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            print(f"[PAYMENT] Payment succeeded: {payment_intent['id']}")
            # Update invoice status in database
            return {'success': True, 'event': 'payment_succeeded', 'payment_intent_id': payment_intent['id']}
        
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            print(f"[PAYMENT] Payment failed: {payment_intent['id']}")
            return {'success': True, 'event': 'payment_failed', 'payment_intent_id': payment_intent['id']}
        
        return {'success': True, 'event': event['type']}
        
    except ImportError:
        return {'error': 'Stripe library not installed'}
    except Exception as e:
        return {'error': str(e)}

def get_payment_methods():
    """Get available payment methods"""
    return {
        'methods': ['card', 'bank_transfer'],
        'currencies': ['AED', 'USD', 'EUR'],
        'stripe_configured': bool(PAYMENT_CONFIG.get('stripe_secret_key'))
    }

# Mock payment for testing (when Stripe not configured)
def create_mock_payment(amount, description=''):
    """Create a mock payment for testing"""
    mock_id = f"mock_pi_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        'success': True,
        'payment_intent_id': mock_id,
        'client_secret': f"{mock_id}_secret",
        'amount': amount,
        'currency': 'AED',
        'status': 'requires_payment_method',
        'mock': True,
        'message': 'This is a mock payment. Configure Stripe for real payments.'
    }

if __name__ == "__main__":
    print("Payment Service Module")
    print("Requires: pip install stripe")
    print("\nConfiguration:")
    print("1. Get Stripe API keys from https://dashboard.stripe.com/apikeys")
    print("2. Save keys in payment_config.json")
    print("3. Test with create_payment_intent()")
