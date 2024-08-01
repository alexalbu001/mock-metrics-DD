# test_app.py
import requests

# This is the URL where your Flask app is running. 
# For local testing, it might be 'http://localhost:5000'.
# In a CI/CD pipeline, this should be the service URL where your app is exposed.
url = 'http://a8bd33b8692bf4efd8d9f0eed1af57ed-1644549184.eu-central-1.elb.amazonaws.com/' 

def test_home_page():
    # Make a GET request to the Flask app's home page
    response = requests.get(url)

    # Check that the HTTP response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the expected text
    assert 'Hello, World!' in response.text

if __name__ == '__main__':
    test_home_page()
    print("Everything passed")
