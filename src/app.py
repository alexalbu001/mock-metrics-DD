from flask import Flask, Response, render_template
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

app = Flask(__name__)

# Create a counter metric to track requests to the main page
REQUESTS = Counter('homepage_requests_total', 'Total number of requests to the homepage')

@app.route('/')
def cv():
    REQUESTS.inc()  # Increment the counter
    return render_template('srt-resume.html')

@app.route('/metrics')
def metrics():
    # Expose the metrics for Prometheus
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
