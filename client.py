import requests
import random
import time

REGISTRY = "http://localhost:5001"
SERVICE_NAME = "my-service"

def discover_and_call():
    print("\n" + "="*50)
    print(f"Client discovering '{SERVICE_NAME}'...")

    try:
        response = requests.get(f"{REGISTRY}/discover/{SERVICE_NAME}")
        data = response.json()
    except Exception as e:
        print(f"Discovery failed: {e}")
        return

    instances = data.get('instances', [])

    if not instances:
        print("No instances found!")
        return

    print(f"Found {len(instances)} instance(s):")
    for inst in instances:
        print(f"  → {inst['address']}")

    # Pick RANDOM instance
    chosen = random.choice(instances)
    address = chosen['address']
    print(f"\nRandomly chose: {address}")

    # Call that instance
    try:
        result = requests.get(f"{address}/hello")
        print(f"Response: {result.json()}")
    except Exception as e:
        print(f"Call failed: {e}")

if __name__ == "__main__":
    print("Client starting — calling service every 5 seconds")
    print("Press Ctrl+C to stop\n")
    while True:
        discover_and_call()
        time.sleep(5)
