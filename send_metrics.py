import json
import os
import requests
import time

# Load the JSON data from the file
with open('trivy.json') as f:
    data = json.load(f)

# Extract the required fields
results = []
for result in data['Results']:
    target = result['Target']
    for vuln in result.get('Vulnerabilities', []):
        severity = vuln['Severity']
        results.append({
            "Target": target,
            "Severity": severity
        })

# Count the number of vulnerabilities by severity
severity_counts = {
    'HIGH': 0,
    'CRITICAL': 0,
    'MEDIUM': 0,
    'LOW': 0
}

for result in results:
    severity = result['Severity'].upper()
    if severity in severity_counts:
        severity_counts[severity] += 1

# Get repository name from environment
repo_name = os.getenv('GITHUB_REPO', 'unknown_repo')

# Prepare the data payload for Datadog
timestamp = int(time.time())
data_payload = {
    "series": []
}

# Add metrics for each severity level with appropriate tags
for severity, count in severity_counts.items():
    if count > 0:  # Only include if there are vulnerabilities of this severity
        data_payload["series"].append({
            "metric": "trivy.vulnerabilities.count",
            "type": "gauge",
            "points": [[timestamp, count]],
            "tags": [f"repo:{repo_name}", f"severity:{severity.lower()}", "source:trivy"]
        })

# Send the data to Datadog
datadog_api_key = os.getenv('DD_API_KEY')
if not datadog_api_key:
    raise ValueError("Datadog API key is not set")

url = "https://api.datadoghq.eu/api/v1/series"
headers = {
    "Content-Type": "application/json",
    "DD-API-KEY": datadog_api_key
}

response = requests.post(url, headers=headers, json=data_payload)
print("Response Status:", response.status_code)
print("Response Body:", response.text)
