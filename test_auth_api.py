import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

BASE_URL = 'http://localhost:8000/api/auth'

def test_auth_endpoints():
    print("Testing Authentication API...")
    
    # Test data
    test_user = {
        'email': 'testapi@example.com',
        'username': 'testapiuser',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'role': 'customer'
    }
    
    try:
        # Test registration
        print("1. Testing user registration...")
        response = requests.post(f"{BASE_URL}/register/", json=test_user)
        if response.status_code == 201:
            print("   SUCCESS: User registered")
            print(f"   Response: {response.json()}")
        else:
            print(f"   FAILED: {response.status_code} - {response.json()}")
            return
        
        # Test login
        print("2. Testing user login...")
        login_data = {
            'email': test_user['email'],
            'password': test_user['password']
        }
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            print("   SUCCESS: User logged in")
            print(f"   Access token received: {len(access_token)} chars")
        else:
            print(f"   FAILED: {response.status_code} - {response.json()}")
            return
        
        # Test profile access with token
        print("3. Testing profile access...")
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print("   SUCCESS: Profile accessed")
            print(f"   User email: {profile['email']}")
            print(f"   User role: {profile['role']}")
        else:
            print(f"   FAILED: {response.status_code} - {response.json()}")
            return
        
        print("ALL AUTH TESTS PASSED!")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_auth_endpoints()