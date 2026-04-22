import requests

# Location was originally :5001 during testing
BASE_URL = "http://127.0.0.1:5000"

sample_data = {
    "delivery_days": 12.0,
    "delivery_vs_estimated": 3.0,
    "price": 149.99,
    "freight_ratio": 0.29,
    "product_category": "electronics",
    "customer_state": "BA",
    "seller_state": "SP",
    "payment_type": "credit_card",
    "distance_miles": 11.5,
    "product_volume_cm^3": 1975.0,
    "total_order_value": 89.97
}

# Test 1: Health
res = requests.get(f"{BASE_URL}/health")
print("Test 1:", res.json())

# Test 2: Single prediction
res = requests.post(f"{BASE_URL}/predict", json=sample_data)
print("Test 2:", res.json())

# Test 3: Batch (5 records)
batch = [sample_data] * 5
res = requests.post(f"{BASE_URL}/predict/batch", json=batch)
print("Test 3:", res.json())

# Test 4: Missing field
bad_data = sample_data.copy()
del bad_data["price"]
res = requests.post(f"{BASE_URL}/predict", json=bad_data)
print("Test 4:", res.json())

# Test 5: Invalid type
bad_data = sample_data.copy()
bad_data["price"] = "invalid"
res = requests.post(f"{BASE_URL}/predict", json=bad_data)
try:
    print("Test 5:", res.json())
except:
    print("Test 5 (raw):", res.text)