import requests
import time

url = "http://127.0.0.1:8000/api/chat"

print("Testing API speed...")
print("=" * 50)

# Test 1: General query
start = time.time()
r = requests.post(url, json={"message": "Hello, how are you?"})
elapsed = round(time.time() - start, 2)
data = r.json()
print(f"Test 1 (General): {elapsed}s")
print(f"  Response: {data['response'][:150]}...")
print()

# Test 2: Math query
start = time.time()
r = requests.post(url, json={"message": "differentiate x^2 + 5x"})
elapsed = round(time.time() - start, 2)
data = r.json()
print(f"Test 2 (Math - cached): {elapsed}s")
print(f"  Response: {data['response'][:150]}...")
print()

# Test 3: Another general query
start = time.time()
r = requests.post(url, json={"message": "What is Python programming?"})
elapsed = round(time.time() - start, 2)
data = r.json()
print(f"Test 3 (General): {elapsed}s")
print(f"  Response: {data['response'][:150]}...")
print()

print("=" * 50)
print("Done!")
