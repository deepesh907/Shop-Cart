import requests
import json

API_PUBLISHABLE_KEY = 'ISPubKey_test_40029710-dd74-4535-af5a-60721c998ff5'
API_TOKEN = 'ISSecretKey_test_d16688d2-d8f4-413c-a312-715a54b79957'

# API endpoint
url = 'https://sandbox.intasend.com/api/v1/payment/mpesa-stk-push/'

# Request headers
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# Request payload
payload = {
    'phone_number': '254722345678',  # Changed to start with 2547 for Safaricom
    'email': 'test@gmail.com',
    'amount': '100',
    'narrative': 'Purchase of items'
}

# Make the request
response = requests.post(url, headers=headers, json=payload)

# Print response
print(response.json())