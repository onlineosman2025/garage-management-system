#!/usr/bin/env python3
"""
Advanced Reports and Analytics Module for Garage Management System
"""
import database as db
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
import json

def get_revenue_report(start_date=None, end_date=None):
    """Get detailed revenue report"""
    invoices = db.get_all_invoices()
    
    # Filter by date if provided
    if start_date:
        invoices = [i for i in invoices if i['created_at'] >= start_date]
    if end_date:
        invoices = [i for i in invoices if i['created_at'] <= end_date]
    
    # Calculate metrics
    total_revenue = sum(i['total_amount'] for i in invoices if i['status'] == 'paid')
    pending_revenue = sum(i['total_amount'] for i in invoices if i['status'] == 'pending')
    total_tax = sum(i['tax_amount'] for i in invoices if i['status'] == 'paid')
    
    # Revenue by month
    monthly_revenue = defaultdict(float)
    for invoice in invoices:
        if invoice['status'] == 'paid':
            month = invoice['created_at'][:7]  # YYYY-MM
            monthly_revenue[month] += invoice['total_amount']
    
    # Revenue by customer
    customer_revenue = defaultdict(lambda: {'count': 0, 'total': 0})
    for invoice in invoices:
        if invoice['status'] == 'paid':
            cust_id = invoice['customer_id']
            customer_revenue[cust_id]['count'] += 1
            customer_revenue[cust_id]['total'] += invoice['total_amount']
    
    # Top customers
    top_customers = []
    for cust_id, data in customer_revenue.items():
        customer = db.get_customer_by_id(cust_id)
        if customer:
            top_customers.append({
                'customer_id': cust_id,
                'customer_name': customer['name'],
                'invoice_count': data['count'],
                'total_revenue': data['total']
            })
    top_customers.sort(key=lambda x: x['total_revenue'], reverse=True)
    
    return {
        'total_revenue': round(total_revenue, 2),
        'pending_revenue': round(pending_revenue, 2),
        'total_tax_collected': round(total_tax, 2),
        'invoice_count': len([i for i in invoices if i['status'] == 'paid']),
        'pending_invoice_count': len([i for i in invoices if i['status'] == 'pending']),
        'monthly_revenue': dict(sorted(monthly_revenue.items())),
        'top_customers': top_customers[:10],
        'average_invoice_value': round(total_revenue / len([i for i in invoices if i['status'] == 'paid']), 2) if invoices else 0
    }

def get_customer_analytics():
    """Get customer analytics"""
    customers = db.get_all_customers()
    jobs = db.get_all_jobs()
    invoices = db.get_all_invoices()
    
    # Customer metrics
    customer_data = []
    for customer in customers:
        cust_jobs = [j for j in jobs if j['customer_id'] == customer['id']]
        cust_invoices = [i for i in invoices if i['customer_id'] == customer['id']]
        paid_invoices = [i for i in cust_invoices if i['status'] == 'paid']
        
        customer_data.append({
            'id': customer['id'],
            'name': customer['name'],
            'email': customer['email'],
            'phone': customer.get('phone', ''),
            'total_jobs': len(cust_jobs),
            'completed_jobs': len([j for j in cust_jobs if j['status'] == 'completed']),
            'total_spent': sum(i['total_amount'] for i in paid_invoices),
            'pending_amount': sum(i['total_amount'] for i in cust_invoices if i['status'] == 'pending'),
            'last_visit': max([j['date'] for j in cust_jobs]) if cust_jobs else None,
            'customer_since': customer['created_at']
        })
    
    # Sort by total spent
    customer_data.sort(key=lambda x: x['total_spent'], reverse=True)
    
    # Customer lifetime value
    total_clv = sum(c['total_spent'] for c in customer_data)
    avg_clv = total_clv / len(customer_data) if customer_data else 0
    
    # New customers this month
    current_month = datetime.now().strftime('%Y-%m')
    new_customers = len([c for c in customers if c['created_at'].startswith(current_month)])
    
    return {
        'total_customers': len(customers),
        'active_customers': len([c for c in customer_data if c['total_jobs'] > 0]),
        'new_customers_this_month': new_customers,
        'average_customer_lifetime_value': round(avg_clv, 2),
        'total_customer_lifetime_value': round(total_clv, 2),
        'customers': customer_data,
        'top_customers': customer_data[:10]
    }

def get_service_analytics():
    """Get service/job analytics"""
    jobs = db.get_all_jobs()
    
    # Service type breakdown
    service_types = defaultdict(lambda: {'count': 0, 'revenue': 0})
    for job in jobs:
        service_type = job['service_type']
        service_types[service_type]['count'] += 1
        if job['status'] == 'completed':
            service_types[service_type]['revenue'] += float(job['estimated_cost'])
    
    # Job status breakdown
    status_counts = defaultdict(int)
    for job in jobs:
        status_counts[job['status']] += 1
    
    # Monthly job volume
    monthly_jobs = defaultdict(int)
    for job in jobs:
        month = job['date'][:7]  # YYYY-MM
        monthly_jobs[month] += 1
    
    # Average job value
    completed_jobs = [j for j in jobs if j['status'] == 'completed']
    avg_job_value = sum(float(j['estimated_cost']) for j in completed_jobs) / len(completed_jobs) if completed_jobs else 0
    
    # Service type list
    service_breakdown = []
    for service_type, data in service_types.items():
        service_breakdown.append({
            'service_type': service_type,
            'count': data['count'],
            'revenue': round(data['revenue'], 2),
            'percentage': round((data['count'] / len(jobs)) * 100, 1) if jobs else 0
        })
    service_breakdown.sort(key=lambda x: x['count'], reverse=True)
    
    return {
        'total_jobs': len(jobs),
        'completed_jobs': len(completed_jobs),
        'pending_jobs': status_counts.get('pending', 0),
        'in_progress_jobs': status_counts.get('in_progress', 0),
        'average_job_value': round(avg_job_value, 2),
        'total_revenue_from_jobs': round(sum(float(j['estimated_cost']) for j in completed_jobs), 2),
        'service_breakdown': service_breakdown,
        'monthly_job_volume': dict(sorted(monthly_jobs.items())),
        'status_breakdown': dict(status_counts)
    }

def get_financial_summary(period='month'):
    """Get financial summary for specified period"""
    invoices = db.get_all_invoices()
    jobs = db.get_all_jobs()
    
    # Determine date range
    now = datetime.now()
    if period == 'month':
        start_date = now.replace(day=1).strftime('%Y-%m-%d')
    elif period == 'year':
        start_date = now.replace(month=1, day=1).strftime('%Y-%m-%d')
    elif period == 'week':
        start_date = (now - timedelta(days=7)).strftime('%Y-%m-%d')
    else:
        start_date = None
    
    # Filter data
    if start_date:
        invoices = [i for i in invoices if i['created_at'] >= start_date]
        jobs = [j for j in jobs if j['date'] >= start_date]
    
    # Calculate metrics
    revenue = sum(i['total_amount'] for i in invoices if i['status'] == 'paid')
    pending = sum(i['total_amount'] for i in invoices if i['status'] == 'pending')
    tax_collected = sum(i['tax_amount'] for i in invoices if i['status'] == 'paid')
    
    # Profit margin (assuming 60% profit margin on services)
    estimated_costs = sum(float(j['estimated_cost']) * 0.4 for j in jobs if j['status'] == 'completed')
    profit = revenue - estimated_costs
    profit_margin = (profit / revenue * 100) if revenue > 0 else 0
    
    return {
        'period': period,
        'start_date': start_date,
        'end_date': now.strftime('%Y-%m-%d'),
        'revenue': round(revenue, 2),
        'pending_revenue': round(pending, 2),
        'tax_collected': round(tax_collected, 2),
        'estimated_profit': round(profit, 2),
        'profit_margin': round(profit_margin, 1),
        'invoice_count': len([i for i in invoices if i['status'] == 'paid']),
        'job_count': len(jobs),
        'average_transaction': round(revenue / len([i for i in invoices if i['status'] == 'paid']), 2) if invoices else 0
    }

def get_dashboard_analytics():
    """Get comprehensive dashboard analytics"""
    return {
        'revenue_report': get_revenue_report(),
        'customer_analytics': get_customer_analytics(),
        'service_analytics': get_service_analytics(),
        'financial_summary': get_financial_summary('month'),
        'generated_at': datetime.now().isoformat()
    }

def export_report_to_json(report_type='full', filename=None):
    """Export report to JSON file"""
    if report_type == 'revenue':
        data = get_revenue_report()
    elif report_type == 'customers':
        data = get_customer_analytics()
    elif report_type == 'services':
        data = get_service_analytics()
    else:
        data = get_dashboard_analytics()
    
    if filename is None:
        filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    filepath = Path(__file__).parent / 'reports' / filename
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[REPORTS] Report exported: {filepath}")
    return str(filepath)

if __name__ == "__main__":
    print("Reports and Analytics Module")
    print("Use get_dashboard_analytics() for comprehensive reports")
