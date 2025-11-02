import json
from urllib.request import urlopen

response = urlopen('http://localhost:3000/api/reports/dashboard')
data = json.loads(response.read())

print("=" * 60)
print("REVENUE REPORT FROM API:")
print("=" * 60)
print(json.dumps(data['revenue_report'], indent=2))

print("\n" + "=" * 60)
print("CUSTOMER ANALYTICS FROM API:")
print("=" * 60)
print(json.dumps(data['customer_analytics'], indent=2))

print("\n" + "=" * 60)
print("SERVICE ANALYTICS FROM API:")
print("=" * 60)
print(json.dumps(data['service_analytics'], indent=2))

print("\n" + "=" * 60)
print("FINANCIAL SUMMARY FROM API:")
print("=" * 60)
print(json.dumps(data['financial_summary'], indent=2))
