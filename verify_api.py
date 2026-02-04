
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_execute_safe():
    print("\n[TEST] Safe Code Execution")
    code = "print('Hello from Sandbox')"
    try:
        response = requests.post(f"{BASE_URL}/execute", json={"code": code})
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        if data['success'] and "Hello from Sandbox" in data['stdout']:
             print("✅ Passed")
        else:
             print("❌ Failed")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_execute_unsafe():
    print("\n[TEST] Unsafe Code Execution (import os)")
    code = "import os\nprint(os.getcwd())"
    try:
        response = requests.post(f"{BASE_URL}/execute", json={"code": code})
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        if not data['success'] and "Security Violation" in data['error']:
             print("✅ Passed (Blocked)")
        else:
             print("❌ Failed (Should have been blocked)")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_chat_mock():
    print("\n[TEST] Chat Mock")
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"message": "Fix this code"})
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        if "Mock Mode" in data['response']:
             print("✅ Passed")
        else:
             print("❌ Failed")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_execute_safe()
    test_execute_unsafe()
    test_chat_mock()
