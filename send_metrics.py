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
        vulnerability_id = vuln['VulnerabilityID']
        severity = vuln['Severity']
        results.append({
            "Target": target,
            "VulnerabilityID": vulnerability_id,
            "Severity": severity
        })

# Count the number of vulnerabilities by severity
high_count = sum(1 for r in results if r['Severity'] == 'HIGH')
critical_count = sum(1 for r in results if r['Severity'] == 'CRITICAL')
medium_count = sum(1 for r in results if r['Severity'] == 'MEDIUM')
low_count = sum(1 for r in results if r['Severity'] == 'LOW')
total_count = high_count + critical_count + medium_count + low_count

# Get repository name from environment
repo_name = os.getenv('GITHUB_REPO', 'unknown_repo')  # Default to 'unknown_repo' if not set

# Prepare the data payload for Datadog
timestamp = int(time.time())
data_payload = {
    "series": [
        {
            "metric": "trivy.vulnerabilities.count",
            "type": "gauge",
            "points": [[timestamp, total_count]],
            "tags": [f"repo:{repo_name}", "source:trivy"]
        }
    ]
}

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
