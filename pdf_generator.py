#!/usr/bin/env python3
"""
PDF Invoice Generator for Garage Management System
Uses HTML to PDF conversion without external dependencies
"""
from pathlib import Path
from datetime import datetime

def generate_invoice_html(invoice, customer, garage_info):
    """Generate HTML for invoice that can be printed as PDF"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice #{invoice['id']}</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
        }}
        
        @media print {{
            body {{ 
                margin: 0;
                width: 210mm;
                height: 297mm;
            }}
            .no-print {{ display: none; }}
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.4;
            color: #333;
            width: 210mm;
            height: 297mm;
            margin: 0 auto;
            padding: 15mm;
            background: white;
            position: relative;
        }}
        
        .invoice-header {{
            background: linear-gradient(135deg, #FF6600 0%, #FF8C32 100%);
            color: white;
            padding: 20px 25px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(255, 102, 0, 0.2);
        }}
        
        .invoice-header h1 {{
            margin: 0;
            font-size: 1.8em;
        }}
        
        .invoice-header .company-name {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 3px;
        }}
        
        .invoice-header div {{
            font-size: 0.9em;
            line-height: 1.3;
        }}
        
        .invoice-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .info-box {{
            background: #f9f9f9;
            padding: 12px 15px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }}
        
        .info-box h3 {{
            margin: 0 0 8px 0;
            color: #FF6600;
            font-size: 1em;
            border-bottom: 2px solid #FF6600;
            padding-bottom: 3px;
        }}
        
        .info-box p {{
            margin: 3px 0;
            font-size: 0.9em;
        }}
        
        .invoice-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .invoice-table th {{
            background: linear-gradient(135deg, #FF6600 0%, #FF8C32 100%);
            color: white;
            padding: 10px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
        }}
        
        .invoice-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 0.9em;
        }}
        
        .invoice-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .invoice-table .amount {{
            text-align: right;
            font-weight: 500;
        }}
        
        .totals {{
            margin-top: 15px;
            text-align: right;
        }}
        
        .totals table {{
            margin-left: auto;
            min-width: 250px;
        }}
        
        .totals td {{
            padding: 6px 15px;
            font-size: 0.95em;
        }}
        
        .totals .label {{
            font-weight: 500;
            color: #666;
        }}
        
        .totals .subtotal {{
            border-top: 1px solid #e0e0e0;
        }}
        
        .totals .tax {{
            color: #666;
        }}
        
        .totals .total {{
            border-top: 2px solid #FF6600;
            font-size: 1.2em;
            font-weight: bold;
            color: #FF6600;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.8em;
            text-transform: uppercase;
        }}
        
        .status-paid {{
            background: #d1fae5;
            color: #10b981;
        }}
        
        .status-pending {{
            background: #ffe5d9;
            color: #FF6600;
        }}
        
        .footer {{
            margin-top: 20px;
            padding-top: 12px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.85em;
        }}
        
        .payment-info {{
            background: #fff8f5;
            border: 2px solid #FF6600;
            border-radius: 6px;
            padding: 12px 15px;
            margin: 15px 0;
        }}
        
        .payment-info h3 {{
            color: #FF6600;
            margin: 0 0 6px 0;
            font-size: 1em;
        }}
        
        .payment-info p {{
            margin: 3px 0;
            font-size: 0.85em;
        }}
        
        .print-button {{
            background: linear-gradient(135deg, #FF6600 0%, #FF8C32 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            margin: 15px 0;
            box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
            transition: all 0.3s;
        }}
        
        .print-button:hover {{
            background: linear-gradient(135deg, #FF7700 0%, #FF9D43 100%);
            box-shadow: 0 6px 16px rgba(255, 102, 0, 0.4);
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="no-print">
        <button class="print-button" onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>
    
    <div class="invoice-header">
        <div class="company-name">🏪 {garage_info.get('name', '')}</div>
        <div>{garage_info.get('address', '')}</div>
        <div>{garage_info.get('phone', '')}</div>
        <div>{garage_info.get('email', '')}</div>
        {f"<div style='margin-top: 8px; font-weight: bold;'>TRN: {garage_info.get('tax_number', 'Not Set')}</div>" if garage_info.get('tax_number') else ''}
    </div>
    
    <div style="text-align: center; margin: 12px 0;">
        <h1 style="margin: 0; color: #333; font-size: 1.8em;">INVOICE</h1>
        <p style="font-size: 1em; color: #666; margin: 5px 0;">#{invoice['id']}</p>
        <span class="status-badge status-{invoice['status']}">{invoice['status'].upper()}</span>
    </div>
    
    <div class="invoice-info">
        <div class="info-box">
            <h3>Bill To:</h3>
            <p><strong>{customer['name']}</strong></p>
            <p>{customer.get('email', '')}</p>
            <p>{customer.get('phone', '')}</p>
            <p>{customer.get('address', '')}</p>
        </div>
        
        <div class="info-box">
            <h3>Invoice Details:</h3>
            <p><strong>Invoice Number:</strong> #{invoice['id']}</p>
            <p><strong>Date Issued:</strong> {invoice['created_at']}</p>
            <p><strong>Due Date:</strong> {invoice.get('due_date', 'Upon Receipt')}</p>
            <p><strong>Payment Terms:</strong> {invoice.get('payment_terms', 'Net 30').replace('_', ' ').title()}</p>
            {f"<p><strong>Paid On:</strong> {invoice['paid_at']}</p>" if invoice['status'] == 'paid' else ''}
        </div>
    </div>
    
    <table class="invoice-table">
        <thead>
            <tr>
                <th style="width: 60%;">Description</th>
                <th style="width: 40%; text-align: right;">Amount</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <strong>{invoice.get('description', 'Service Charges')}</strong>
                    {f"<br><small style='color: #666;'>Job ID: {invoice['job_id']}</small>" if invoice.get('job_id') else ''}
                </td>
                <td class="amount">AED {invoice['amount']:.2f}</td>
            </tr>
        </tbody>
    </table>
    
    <div class="totals">
        <table>
            <tr class="subtotal">
                <td class="label">Subtotal:</td>
                <td class="amount">AED {invoice['amount']:.2f}</td>
            </tr>
            <tr class="tax">
                <td class="label">Tax ({invoice['tax_rate']}%):</td>
                <td class="amount">AED {invoice['tax_amount']:.2f}</td>
            </tr>
            <tr class="total">
                <td class="label">Total Amount:</td>
                <td class="amount">AED {invoice['total_amount']:.2f}</td>
            </tr>
        </table>
    </div>
    
    {f'''
    <div style="background: #d1fae5; border: 2px solid #10b981; border-radius: 6px; padding: 12px; margin: 15px 0; text-align: center; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);">
        <h3 style="color: #10b981; margin: 0; font-size: 1.2em;">✓ PAID IN FULL</h3>
        <p style="color: #059669; margin: 5px 0 0 0; font-size: 0.85em;">Payment received on {invoice['paid_at']}</p>
    </div>
    ''' if invoice['status'] == 'paid' else '''
    <div class="payment-info">
        <h3>Payment Information</h3>
        <p><strong>Amount Due:</strong> AED {invoice['total_amount']:.2f}</p>
        <p><strong>Bank:</strong> Emirates NBD | <strong>Account:</strong> XXXX-XXXX-XXXX-1234</p>
        <p><strong>IBAN:</strong> AE07 0331 2345 6789 0123 456</p>
    </div>
    '''}
    
    <div class="footer">
        <p style="margin: 5px 0;"><strong>Thank you for your business!</strong></p>
        <p style="margin: 5px 0; font-size: 0.8em;">
            {garage_info.get('name', '')} | {garage_info.get('address', '')}<br>
            {garage_info.get('phone', '')} | {garage_info.get('email', '')}
            {f"<br>TRN: {garage_info.get('tax_number', 'Not Registered')}" if garage_info.get('tax_number') else ''}
        </p>
        <p style="margin: 10px 0 5px 0; font-size: 0.75em; color: #999;">
            🇦🇪 <strong>UAE VAT Compliant Tax Invoice</strong> | This is a VAT invoice issued in accordance with UAE Federal Tax Authority requirements.
        </p>
    </div>
    
    <div class="no-print" style="text-align: center; margin-top: 15px;">
        <button class="print-button" onclick="window.print()">🖨️ Print / Save as PDF</button>
        <p style="color: #666; margin-top: 8px; font-size: 0.85em;">
            <small>Tip: Use your browser's Print function (Ctrl+P) and select "Save as PDF"</small>
        </p>
    </div>
</body>
</html>
    """
    return html

def save_invoice_html(invoice, customer, garage_info, output_dir=None):
    """Save invoice as HTML file"""
    if output_dir is None:
        output_dir = Path(__file__).parent / 'invoices'
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    html_content = generate_invoice_html(invoice, customer, garage_info)
    filename = f"invoice_{invoice['id']}_{datetime.now().strftime('%Y%m%d')}.html"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[PDF] Invoice HTML saved: {filepath}")
    return str(filepath)

# For future PDF generation with reportlab (when installed)
def generate_pdf_with_reportlab(invoice, customer, garage_info):
    """Generate PDF using reportlab (requires: pip install reportlab)"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        
        output_dir = Path(__file__).parent / 'invoices'
        output_dir.mkdir(exist_ok=True)
        
        filename = f"invoice_{invoice['id']}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = output_dir / filename
        
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"INVOICE #{invoice['id']}", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Company and customer info
        info_data = [
            ['From:', 'To:'],
            [garage_info.get('name', ''), customer['name']],
            [garage_info.get('address', ''), customer.get('email', '')],
            ['', customer.get('phone', '')],
        ]
        
        info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Invoice details
        details_data = [
            ['Description', 'Amount'],
            [invoice.get('description', 'Service Charges'), f"AED {invoice['amount']:.2f}"],
            ['', ''],
            ['Subtotal:', f"AED {invoice['amount']:.2f}"],
            [f"Tax ({invoice['tax_rate']}%):", f"AED {invoice['tax_amount']:.2f}"],
            ['TOTAL:', f"AED {invoice['total_amount']:.2f}"],
        ]
        
        details_table = Table(details_data, colWidths=[5*inch, 2*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -2), 1, colors.grey),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#667eea')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
        ]))
        story.append(details_table)
        
        # Build PDF
        doc.build(story)
        print(f"[PDF] PDF generated: {filepath}")
        return str(filepath)
        
    except ImportError:
        print("[PDF] reportlab not installed. Using HTML method instead.")
        return None

if __name__ == "__main__":
    print("PDF Generator Module")
    print("Use generate_invoice_html() or save_invoice_html()")
