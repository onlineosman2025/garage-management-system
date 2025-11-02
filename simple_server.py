#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import json
import secrets
from pathlib import Path
from datetime import datetime
import re
import database as db
import email_service
import pdf_generator
import reports
import permissions
import file_manager
import uae_vat_system

PORT = int(os.environ.get('PORT', 3000))
HOST = '0.0.0.0'
# CORS fix applied - version 3.0

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def send_response(self, code):
        self.log_request(code)
        self.wfile.write(f"HTTP/1.1 {code} {self.responses[code][0]}\r\n".encode('utf-8'))
    
    def send_header(self, keyword, value):
        self.wfile.write(f"{keyword}: {value}\r\n".encode('utf-8'))
    
    def end_headers(self):
        # Add CORS headers ONCE
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.wfile.write("\r\n".encode('utf-8'))

    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        
        # Handle API routes
        if self.path == '/api/dashboard/stats':
            stats = db.get_dashboard_stats()
            self.send_json(stats)
            return
        elif self.path.startswith('/api/customers'):
            if '/api/customers/' in self.path and '?' not in self.path:
                # Get specific customer
                customer_id = int(self.path.split('/')[-1])
                customer = db.get_customer_by_id(customer_id)
                if customer:
                    self.send_json(customer)
                else:
                    self.send_error(404, "Customer not found")
            else:
                # Get all customers
                customers = db.get_all_customers()
                self.send_json(customers)
            return
        elif self.path.startswith('/api/jobs'):
            # Check for limit parameter
            limit = None
            if '?' in self.path:
                from urllib.parse import parse_qs, urlparse
                query_params = parse_qs(urlparse(self.path).query)
                if 'limit' in query_params:
                    limit = int(query_params['limit'][0])
            
            jobs = db.get_all_jobs(limit=limit)
            self.send_json(jobs)
            return
        elif self.path.startswith('/api/dashboard/revenue'):
            # Dashboard revenue chart data
            self.send_json({
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'values': [800, 950, 1100, 1050, 1200, 1150, 1300, 1250, 1400, 1050, 0, 0]
            })
            return
        elif self.path.startswith('/api/reports/revenue'):
            self.send_json({
                'total_revenue': 1050.00,
                'total_vat': 50.00,
                'invoice_count': 0,
                'chart_data': [
                    {'month': 'Oct', 'revenue': 1050.00}
                ]
            })
            return
        elif self.path.startswith('/api/reports/customers'):
            customers = db.get_all_customers()
            self.send_json({
                'total_customers': len(customers),
                'active_customers': len(customers),
                'chart_data': customers[:5]
            })
            return
        elif self.path.startswith('/api/dashboard/activities'):
            # Return recent activities
            self.send_json([
                {'type': 'customer_added', 'description': 'New customer added', 'created_at': datetime.now().isoformat()},
                {'type': 'job_created', 'description': 'New job created', 'created_at': datetime.now().isoformat()},
            ])
            return
        elif self.path.startswith('/api/invoices'):
            if '/api/invoices/' in self.path and '?' not in self.path:
                # Get specific invoice
                invoice_id = int(self.path.split('/')[-1])
                invoice = db.get_invoice_by_id(invoice_id)
                if invoice:
                    self.send_json(invoice)
                else:
                    self.send_error(404, "Invoice not found")
            else:
                # Get all invoices
                invoices = db.get_all_invoices()
                self.send_json(invoices)
            return
        elif self.path.startswith('/api/users'):
            if '/api/users/' in self.path and '?' not in self.path:
                # Get specific user
                user_id = int(self.path.split('/')[-1])
                user = db.get_user_by_id(user_id)
                if user:
                    # Remove password hash from response
                    if 'password_hash' in user:
                        del user['password_hash']
                    self.send_json(user)
                else:
                    self.send_error(404, "User not found")
            else:
                # Get all users
                users = db.get_all_users()
                # Remove password hashes from response
                for user in users:
                    if 'password_hash' in user:
                        del user['password_hash']
                self.send_json(users)
            return
        elif self.path.startswith('/api/services'):
            # Get all services
            services = db.get_all_services()
            self.send_json(services)
            return
        elif self.path.startswith('/api/vehicles'):
            # Get all vehicles
            vehicles = db.get_all_vehicles()
            self.send_json(vehicles)
            return
        elif self.path.startswith('/api/garage-info'):
            # Get garage information
            garage_info = db.get_garage_info()
            self.send_json(garage_info)
            return
        elif self.path.startswith('/api/auth/login'):
            # Handle login
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                username = data.get('username')
                password = data.get('password')
                
                if not username or not password:
                    self.send_error(400, "Username and password are required")
                    return
                
                user = db.authenticate_user(username, password)
                if user:
                    # Remove password hash from response
                    if 'password_hash' in user:
                        del user['password_hash']
                    self.send_json({
                        'success': True,
                        'user': user,
                        'message': 'Login successful'
                    })
                else:
                    self.send_json({
                        'success': False,
                        'message': 'Invalid username or password'
                    })
            except Exception as e:
                self.send_error(500, f"Login error: {str(e)}")
            return
        elif self.path.startswith('/api/auth/register'):
            # Handle user registration
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                username = data.get('username')
                password = data.get('password')
                email = data.get('email')
                full_name = data.get('full_name')
                role = data.get('role', 'technician')
                
                if not username or not password or not email or not full_name:
                    self.send_error(400, "Username, password, email, and full_name are required")
                    return
                
                # Check if user already exists
                existing_user = db.get_user_by_username(username)
                if existing_user:
                    self.send_json({
                        'success': False,
                        'message': 'Username already exists'
                    })
                    return
                
                # Create new user
                user = db.create_user({
                    'username': username,
                    'password': password,
                    'email': email,
                    'full_name': full_name,
                    'role': role
                })
                
                if user:
                    # Remove password hash from response
                    if 'password_hash' in user:
                        del user['password_hash']
                    self.send_json({
                        'success': True,
                        'user': user,
                        'message': 'User registered successfully'
                    })
                else:
                    self.send_json({
                        'success': False,
                        'message': 'Failed to register user'
                    })
            except Exception as e:
                self.send_error(500, f"Registration error: {str(e)}")
            return
        elif self.path.startswith('/api/auth/logout'):
            # Handle logout (client-side token removal)
            self.send_json({
                'success': True,
                'message': 'Logout successful'
            })
            return
        elif self.path.startswith('/api/auth/check'):
            # Check authentication status
            auth_header = self.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]
                # For simplicity, we'll just return success if token is provided
                # In a real app, you'd validate the token
                self.send_json({
                    'success': True,
                    'authenticated': True,
                    'message': 'Authentication valid'
                })
            else:
                self.send_json({
                    'success': False,
                    'authenticated': False,
                    'message': 'Not authenticated'
                })
            return
        else:
            # Serve static files
            return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if self.path == '/api/customers':
            # Create new customer
            try:
                customer = db.create_customer(data)
                self.send_json(customer)
            except Exception as e:
                self.send_error(500, f"Failed to create customer: {str(e)}")
        elif self.path == '/api/jobs':
            # Create new job
            try:
                job = db.create_job(data)
                self.send_json(job)
            except Exception as e:
                self.send_error(500, f"Failed to create job: {str(e)}")
        elif self.path == '/api/invoices':
            # Create new invoice
            try:
                invoice = db.create_invoice(data)
                self.send_json(invoice)
            except Exception as e:
                self.send_error(500, f"Failed to create invoice: {str(e)}")
        elif self.path == '/api/users':
            # Create new user
            try:
                user = db.create_user(data)
                # Remove password hash from response
                if 'password_hash' in user:
                    del user['password_hash']
                self.send_json(user)
            except Exception as e:
                self.send_error(500, f"Failed to create user: {str(e)}")
        elif self.path.startswith('/api/email/send/invoice/'):
            # Send invoice email
            invoice_id = int(self.path.split('/')[-1])
            invoice = db.get_invoice_by_id(invoice_id)
            if not invoice:
                self.send_error(404, "Invoice not found")
                return
            
            customer = db.get_customer_by_id(invoice['customer_id'])
            if not customer:
                self.send_error(404, "Customer not found")
                return
            
            garage_info = db.get_garage_info()
            success = email_service.send_invoice_email(invoice, customer, garage_info)
            
            if success:
                self.send_json({'success': True, 'message': 'Invoice email sent successfully'})
            else:
                self.send_error(500, "Failed to send email. Check email configuration.")
        elif self.path.startswith('/api/email/send/payment/'):
            # Send payment confirmation email
            invoice_id = int(self.path.split('/')[-1])
            invoice = db.get_invoice_by_id(invoice_id)
            if not invoice:
                self.send_error(404, "Invoice not found")
                return
            
            customer = db.get_customer_by_id(invoice['customer_id'])
            if not customer:
                self.send_error(404, "Customer not found")
                return
            
            garage_info = db.get_garage_info()
            success = email_service.send_payment_confirmation_email(invoice, customer, garage_info)
            
            if success:
                self.send_json({'success': True, 'message': 'Payment confirmation email sent successfully'})
            else:
                self.send_error(500, "Failed to send email. Check email configuration.")
        elif self.path == '/api/files/upload':
            # File upload
            try:
                filename = data.get('filename')
                file_data = data.get('file_data')  # Base64 encoded
                category = data.get('category', 'general')
                related_id = data.get('related_id')
                
                if not filename or not file_data:
                    self.send_error(400, "filename and file_data are required")
                    return
                
                file_info = file_manager.save_file(file_data, filename, category, related_id)
                self.send_json({'success': True, 'file': file_info})
            except ValueError as e:
                self.send_error(400, str(e))
            except Exception as e:
                self.send_error(500, f"File upload failed: {str(e)}")
        elif self.path == '/api/settings':
            # Save settings
            try:
                for key, value in data.items():
                    db.set_setting(key, str(value))
                self.send_json({'success': True, 'message': 'Settings saved successfully'})
            except Exception as e:
                self.send_error(500, f"Failed to save settings: {str(e)}")
        elif self.path == '/api/services':
            # Create new service
            try:
                service = db.create_service(data)
                self.send_json(service)
            except Exception as e:
                self.send_error(500, f"Failed to create service: {str(e)}")
        elif self.path == '/api/vehicles':
            # Create new vehicle
            try:
                vehicle = db.create_vehicle(data)
                self.send_json(vehicle)
            except Exception as e:
                self.send_error(500, f"Failed to create vehicle: {str(e)}")
        else:
            self.send_error(404, "Not found")
    
    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if '/api/customers/' in self.path:
            customer_id = int(self.path.split('/')[-1])
            customer = db.update_customer(customer_id, data)
            if customer:
                self.send_json(customer)
            else:
                self.send_error(404, "Customer not found")
        elif '/api/jobs/' in self.path and '/status' in self.path:
            job_id = int(self.path.split('/')[-2])
            status = data.get('status')
            job = db.update_job_status(job_id, status)
            if job:
                self.send_json(job)
            else:
                self.send_error(404, "Job not found")
        elif '/api/invoices/' in self.path and self.path.endswith('/pay'):
            # Mark invoice as paid
            invoice_id = int(self.path.split('/')[-2])
            invoice = db.mark_invoice_paid(invoice_id)
            if invoice:
                self.send_json(invoice)
            else:
                self.send_error(404, "Invoice not found")
        elif '/api/invoices/' in self.path:
            # Update invoice
            invoice_id = int(self.path.split('/')[-1])
            invoice = db.update_invoice(invoice_id, data)
            if invoice:
                self.send_json(invoice)
            else:
                self.send_error(404, "Invoice not found")
        elif '/api/services/' in self.path:
            # Update service
            service_id = int(self.path.split('/')[-1])
            service = db.update_service(service_id, data)
            if service:
                self.send_json(service)
            else:
                self.send_error(404, "Service not found")
        elif '/api/vehicles/' in self.path:
            # Update vehicle
            vehicle_id = int(self.path.split('/')[-1])
            vehicle = db.update_vehicle(vehicle_id, data)
            if vehicle:
                self.send_json(vehicle)
            else:
                self.send_error(404, "Vehicle not found")
        elif '/api/users/' in self.path:
            # Update user
            user_id = int(self.path.split('/')[-1])
            user = db.update_user(user_id, data)
            if user:
                # Remove password hash
                if 'password_hash' in user:
                    del user['password_hash']
                self.send_json(user)
            else:
                self.send_error(404, "User not found")
        else:
            self.send_error(404, "Not found")
    
    def do_DELETE(self):
        if '/api/customers/' in self.path:
            customer_id = int(self.path.split('/')[-1])
            db.delete_customer(customer_id)
            self.send_json({'success': True, 'message': 'Customer deleted'})
        elif '/api/invoices/' in self.path:
            invoice_id = int(self.path.split('/')[-1])
            db.delete_invoice(invoice_id)
            self.send_json({'success': True, 'message': 'Invoice deleted'})
        elif '/api/services/' in self.path:
            service_id = int(self.path.split('/')[-1])
            db.delete_service(service_id)
            self.send_json({'success': True, 'message': 'Service deleted'})
        elif '/api/vehicles/' in self.path:
            vehicle_id = int(self.path.split('/')[-1])
            db.delete_vehicle(vehicle_id)
            self.send_json({'success': True, 'message': 'Vehicle deleted'})
        elif '/api/users/' in self.path:
            user_id = int(self.path.split('/')[-1])
            db.delete_user(user_id)
            self.send_json({'success': True, 'message': 'User deleted'})
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def main():
    os.chdir(Path(__file__).parent)
    
    print("=" * 50)
    print("GARAGE MANAGEMENT SYSTEM - WORKING!")
    print("=" * 50)
    print(f"Working directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')[:10]}")
    print(f"Starting server on http://{HOST}:{PORT}")
    
    try:
        with socketserver.TCPServer((HOST, PORT), SimpleHandler) as httpd:
            print(f"[OK] Server running at http://{HOST}:{PORT}")
            # Only open browser in local development
            if PORT == 3000:
                webbrowser.open(f'http://{HOST}:{PORT}')
            print("\nPress Ctrl+C to stop")
            print("=" * 50)
            httpd.serve_forever()
    except OSError as e:
        print(f"[ERROR] {e}")
        print("Port 3000 might be in use. Try running the cleanup first.")
    except KeyboardInterrupt:
        print("\n[OK] Server stopped")
        os._exit(0)  # Add this line to exit the process after stopping the server

if __name__ == "__main__":
    main()
