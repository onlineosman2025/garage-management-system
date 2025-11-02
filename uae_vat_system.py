#!/usr/bin/env python3
"""
UAE VAT System Module
Implements UAE Federal Tax Authority (FTA) compliant VAT system
"""
import database as db
from datetime import datetime, timedelta
from collections import defaultdict
import json

# UAE VAT Rates
UAE_VAT_RATES = {
    'standard': 5.0,      # Standard rated (5%)
    'zero': 0.0,          # Zero-rated (0%)
    'exempt': 0.0,        # Exempt (no VAT)
    'out_of_scope': 0.0   # Out of scope
}

# UAE VAT Categories
VAT_CATEGORIES = {
    'standard': 'Standard Rated Supply (5%)',
    'zero': 'Zero Rated Supply (0%)',
    'exempt': 'Exempt Supply',
    'out_of_scope': 'Out of Scope'
}

def calculate_vat(amount, vat_category='standard'):
    """
    Calculate VAT based on UAE tax rules
    
    Args:
        amount: Pre-tax amount (exclusive)
        vat_category: 'standard', 'zero', 'exempt', or 'out_of_scope'
    
    Returns:
        dict with tax_rate, tax_amount, total_amount
    """
    tax_rate = UAE_VAT_RATES.get(vat_category, 5.0)
    tax_amount = round(amount * (tax_rate / 100), 2)
    total_amount = round(amount + tax_amount, 2)
    
    return {
        'amount': round(amount, 2),
        'tax_rate': tax_rate,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'vat_category': vat_category,
        'vat_category_name': VAT_CATEGORIES.get(vat_category, 'Standard Rated')
    }

def validate_trn(trn):
    """
    Validate UAE Tax Registration Number (TRN)
    Format: 15 digits
    
    Args:
        trn: Tax Registration Number string
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not trn:
        return False
    
    # Remove spaces and hyphens
    trn = trn.replace(' ', '').replace('-', '')
    
    # Must be 15 digits
    if len(trn) != 15:
        return False
    
    # Must be all digits
    if not trn.isdigit():
        return False
    
    return True

def format_trn(trn):
    """Format TRN with proper spacing: XXX-XXXX-XXXX-XXX"""
    if not trn:
        return ''
    
    trn = trn.replace(' ', '').replace('-', '')
    if len(trn) == 15:
        return f"{trn[0:3]}-{trn[3:7]}-{trn[7:11]}-{trn[11:15]}"
    return trn

def get_vat_return_report(start_date, end_date):
    """
    Generate UAE VAT Return Report (Form 201)
    
    Box 1: Standard rated supplies (5%)
    Box 2: Tax on standard rated supplies
    Box 3: Zero rated supplies
    Box 6: Exempt supplies
    Box 7: Total supplies (Box 1 + 3 + 6)
    Box 8: Standard rated expenses
    Box 9: Tax on standard rated expenses
    Box 11: Total VAT due (Box 2 - Box 9)
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        dict: VAT return data
    """
    invoices = db.get_all_invoices()
    
    # Filter by date range and paid status
    period_invoices = [
        i for i in invoices 
        if i['status'] == 'paid' 
        and start_date <= i['created_at'] <= end_date
    ]
    
    # Initialize boxes
    box1_standard_supplies = 0.0  # Standard rated sales
    box2_output_tax = 0.0          # VAT on sales
    box3_zero_rated = 0.0          # Zero rated sales
    box6_exempt = 0.0              # Exempt sales
    
    for invoice in period_invoices:
        amount = float(invoice['amount'])
        tax_rate = float(invoice.get('tax_rate', 5.0))
        tax_amount = float(invoice.get('tax_amount', 0))
        
        if tax_rate == 5.0:
            box1_standard_supplies += amount
            box2_output_tax += tax_amount
        elif tax_rate == 0.0:
            # Check if zero-rated or exempt (for now, treat as zero-rated)
            box3_zero_rated += amount
    
    box7_total_supplies = box1_standard_supplies + box3_zero_rated + box6_exempt
    
    # For input tax (purchases), you would need expense tracking
    # Placeholder for now
    box8_standard_expenses = 0.0
    box9_input_tax = 0.0
    
    box11_net_vat = box2_output_tax - box9_input_tax
    
    return {
        'period': {
            'start_date': start_date,
            'end_date': end_date,
            'tax_period': get_tax_period_name(start_date)
        },
        'vat_on_sales': {
            'box1_standard_supplies': round(box1_standard_supplies, 2),
            'box2_output_tax': round(box2_output_tax, 2),
            'box3_zero_rated': round(box3_zero_rated, 2),
            'box6_exempt': round(box6_exempt, 2),
            'box7_total_supplies': round(box7_total_supplies, 2)
        },
        'vat_on_purchases': {
            'box8_standard_expenses': round(box8_standard_expenses, 2),
            'box9_input_tax': round(box9_input_tax, 2)
        },
        'summary': {
            'box11_net_vat_due': round(box11_net_vat, 2),
            'invoice_count': len(period_invoices),
            'total_revenue': round(box7_total_supplies + box2_output_tax, 2)
        },
        'generated_at': datetime.now().isoformat()
    }

def get_tax_period_name(date_str):
    """Get tax period name from date (e.g., 'Q1 2024' or 'Jan 2024')"""
    date = datetime.strptime(date_str, '%Y-%m-%d')
    quarter = (date.month - 1) // 3 + 1
    return f"Q{quarter} {date.year}"

def get_monthly_vat_report(year, month):
    """
    Generate monthly VAT report
    
    Args:
        year: Year (e.g., 2024)
        month: Month (1-12)
    
    Returns:
        dict: Monthly VAT summary
    """
    start_date = f"{year}-{month:02d}-01"
    
    # Calculate last day of month
    if month == 12:
        end_date = f"{year}-12-31"
    else:
        next_month = datetime(year, month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        end_date = f"{year}-{month:02d}-{last_day}"
    
    return get_vat_return_report(start_date, end_date)

def get_quarterly_vat_report(year, quarter):
    """
    Generate quarterly VAT report (UAE standard filing period)
    
    Args:
        year: Year (e.g., 2024)
        quarter: Quarter (1-4)
    
    Returns:
        dict: Quarterly VAT summary
    """
    quarter_months = {
        1: (1, 3),   # Jan-Mar
        2: (4, 6),   # Apr-Jun
        3: (7, 9),   # Jul-Sep
        4: (10, 12)  # Oct-Dec
    }
    
    start_month, end_month = quarter_months[quarter]
    start_date = f"{year}-{start_month:02d}-01"
    
    # Last day of quarter
    if end_month == 12:
        end_date = f"{year}-12-31"
    else:
        next_month = datetime(year, end_month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        end_date = f"{year}-{end_month:02d}-{last_day}"
    
    return get_vat_return_report(start_date, end_date)

def get_vat_audit_trail(invoice_id=None):
    """
    Get VAT audit trail for invoices
    Useful for FTA audits
    
    Args:
        invoice_id: Optional specific invoice ID
    
    Returns:
        list: Audit trail entries
    """
    if invoice_id:
        invoices = [db.get_invoice_by_id(invoice_id)]
        invoices = [i for i in invoices if i is not None]
    else:
        invoices = db.get_all_invoices()
    
    audit_trail = []
    for invoice in invoices:
        customer = db.get_customer_by_id(invoice['customer_id'])
        
        audit_trail.append({
            'invoice_id': invoice['id'],
            'invoice_date': invoice['created_at'],
            'customer_name': customer['name'] if customer else 'Unknown',
            'customer_trn': customer.get('trn', 'N/A') if customer else 'N/A',
            'amount_excl_vat': round(invoice['amount'], 2),
            'vat_rate': invoice['tax_rate'],
            'vat_amount': round(invoice['tax_amount'], 2),
            'total_incl_vat': round(invoice['total_amount'], 2),
            'status': invoice['status'],
            'payment_date': invoice.get('paid_at', 'Not Paid')
        })
    
    return audit_trail

def generate_tax_invoice_number(invoice_id):
    """
    Generate FTA compliant tax invoice number
    Format: GMS-TAX-YYYY-NNNNN
    
    Args:
        invoice_id: Invoice ID
    
    Returns:
        str: Tax invoice number
    """
    year = datetime.now().year
    return f"GMS-TAX-{year}-{invoice_id:05d}"

def get_vat_summary_dashboard():
    """
    Get VAT summary for dashboard display
    
    Returns:
        dict: Current period VAT summary
    """
    now = datetime.now()
    current_quarter = (now.month - 1) // 3 + 1
    
    quarterly_report = get_quarterly_vat_report(now.year, current_quarter)
    monthly_report = get_monthly_vat_report(now.year, now.month)
    
    settings = db.get_all_settings()
    garage_trn = settings.get('garage_tax_number', 'Not Set')
    
    return {
        'garage_trn': garage_trn,
        'current_quarter': {
            'period': quarterly_report['period']['tax_period'],
            'vat_collected': quarterly_report['vat_on_sales']['box2_output_tax'],
            'net_vat_due': quarterly_report['summary']['box11_net_vat_due'],
            'total_sales': quarterly_report['vat_on_sales']['box7_total_supplies']
        },
        'current_month': {
            'month': now.strftime('%B %Y'),
            'vat_collected': monthly_report['vat_on_sales']['box2_output_tax'],
            'net_vat_due': monthly_report['summary']['box11_net_vat_due'],
            'invoice_count': monthly_report['summary']['invoice_count']
        },
        'compliance_status': 'Compliant' if garage_trn != 'Not Set' else 'TRN Not Set'
    }

if __name__ == "__main__":
    print("UAE VAT System Module")
    print("=" * 50)
    
    # Example usage
    print("\n1. Calculate VAT on AED 1000:")
    vat_calc = calculate_vat(1000, 'standard')
    print(f"   Amount: AED {vat_calc['amount']}")
    print(f"   VAT (5%): AED {vat_calc['tax_amount']}")
    print(f"   Total: AED {vat_calc['total_amount']}")
    
    print("\n2. Validate TRN:")
    test_trn = "123456789012345"
    print(f"   TRN {test_trn}: {'Valid' if validate_trn(test_trn) else 'Invalid'}")
    print(f"   Formatted: {format_trn(test_trn)}")
    
    print("\n3. Get current period VAT summary:")
    summary = get_vat_summary_dashboard()
    print(f"   Quarter: {summary['current_quarter']['period']}")
    print(f"   VAT Collected: AED {summary['current_quarter']['vat_collected']}")
    print(f"   Net VAT Due: AED {summary['current_quarter']['net_vat_due']}")
