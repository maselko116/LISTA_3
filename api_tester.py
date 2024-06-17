import json
import pycurl
from io import BytesIO


def send_get_request(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    status_code = c.getinfo(c.RESPONSE_CODE)
    response_data = buffer.getvalue().decode('utf-8')
    c.close()
    return status_code, response_data


def check_http_status(status_code):
    if status_code == 200:
        return True
    else:
        return False


def check_json_response(json_data, expected_keys):
    try:
        data = json.loads(json_data)
        for key in expected_keys:
            if key not in data:
                return False
        return True
    except json.JSONDecodeError:
        return False


def test_api_endpoints():
    endpoints = [
        ("https://jsonplaceholder.typicode.com/posts/1", ["userId", "id", "title"]),
        ("https://jsonplaceholder.typicode.com/comments?postId=1", ["postId", "id", "name"]),
        
    ]

    for endpoint, expected_keys in endpoints:
        status_code, response_data = send_get_request(endpoint)
        http_status_ok = check_http_status(status_code)
        json_response_valid = check_json_response(response_data, expected_keys)

        if http_status_ok and json_response_valid:
            print(f"Test for {endpoint}: PASSED")
        else:
            print(f"Test for {endpoint}: FAILED")
            if not http_status_ok:
                print(f"HTTP status code: {status_code}")
            if not json_response_valid:
                print("Missing expected keys in JSON response")


test_api_endpoints()