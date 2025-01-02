import requests
import json

# Base URL of the Django application
BASE_URL = "http://127.0.0.1:8000"

# User credentials for testing
TEST_USER = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}

# Output file for test results
OUTPUT_FILE = "url_test_results.txt"

# List of test cases
TEST_CASES = [
    {"method": "POST", "path": "/upload/", "data": {}, "files": {"file": ("test.txt", "Sample file content")}},
    {"method": "POST", "path": "/prompt/", "data": {"prompt": "Hello AI"}},
    {"method": "GET", "path": "/chat-history/"},
    {"method": "POST", "path": "/chat-history/create/", "data": {"chat_name": "New Chat", "conversation": {}}},
    {"method": "PUT", "path": "/chat-history/update/<id>/", "data": {"chat_name": "Updated Chat"}},
    {"method": "DELETE", "path": "/chat-history/delete/<id>/", "data": {}},
    {"method": "GET", "path": "/chat-history/list/"},
    {"method": "POST", "path": "/logout/", "data": {}},
]

# Function to save test results to a file
def save_results(results):
    with open(OUTPUT_FILE, "w") as file:
        for result in results:
            file.write(f"{result}\n")

# Function to print and return the result
def log_result(test_results, result):
    print(result)
    test_results.append(result)

# Session for session authentication
session = requests.Session()

# Results list
test_results = []

try:
    # Step 1: Register the user
    register_url = f"{BASE_URL}/register/"
    register_response = session.post(register_url, json=TEST_USER)
    if register_response.status_code == 201:
        log_result(test_results, f"SUCCESS: User registration - {register_response.status_code}")
    else:
        log_result(test_results, f"ERROR: User registration - {register_response.status_code} - {register_response.text}")
        save_results(test_results)
        exit()

    # Step 2: Log in the user
    login_url = f"{BASE_URL}/login/"
    login_response = session.post(login_url, data={"username": TEST_USER["username"], "password": TEST_USER["password"]})
    if login_response.status_code == 200:
        log_result(test_results, f"SUCCESS: User login - {login_response.status_code}")
    else:
        log_result(test_results, f"ERROR: User login - {login_response.status_code} - {login_response.text}")
        save_results(test_results)
        exit()

    # Step 3: Test all endpoints
    for test in TEST_CASES:
        url = BASE_URL + test["path"]
        method = test["method"].upper()
        data = test.get("data", {})
        files = test.get("files", {})

        # Replace placeholder ID in URL if needed
        if "<id>" in url:
            url = url.replace("<id>", "some_valid_id")  # Replace with an actual valid ID for your testing

        try:
            # Make the request
            if method == "GET":
                response = session.get(url, params=data)
            elif method == "POST":
                response = session.post(url, data=data, files=files)
            elif method == "PUT":
                response = session.put(url, data=data)
            elif method == "DELETE":
                response = session.delete(url, data=data)
            else:
                log_result(test_results, f"Unsupported HTTP method: {method} for URL: {url}")
                continue

            # Determine the test result
            if 200 <= response.status_code < 300:
                log_result(test_results, f"SUCCESS: {method} {url} - {response.status_code} - {response.text}")
            else:
                log_result(test_results, f"ERROR: {method} {url} - {response.status_code} - {response.text}")

        except Exception as e:
            log_result(test_results, f"EXCEPTION: {method} {url} - {str(e)}")

    # Step 4: Log out the user
    logout_url = f"{BASE_URL}/logout/"
    logout_response = session.post(logout_url)
    if logout_response.status_code == 200:
        log_result(test_results, f"SUCCESS: User logout - {logout_response.status_code}")
    else:
        log_result(test_results, f"ERROR: User logout - {logout_response.status_code} - {logout_response.text}")

except Exception as e:
    log_result(test_results, f"EXCEPTION: {str(e)}")

# Save results to a file
save_results(test_results)
