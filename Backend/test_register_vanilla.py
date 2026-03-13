import http.client
import json

conn = http.client.HTTPConnection("127.0.0.1", 8000)
payload = json.dumps({
    "full_name": "Test User",
    "emailID": "test@example.com",
    "password": "password123"
})
headers = {
    'Content-Type': 'application/json'
}
try:
    conn.request("POST", "/users/register", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(f"Status Code: {res.status}")
    print(f"Response: {data.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
