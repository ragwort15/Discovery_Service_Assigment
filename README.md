# Microservice with Service Discovery

## Overview
A microservice system with service registration, discovery, and random load balancing built in Python.

## Architecture
- **Service Registry** (port 5001) — central registry where services register themselves
- **Instance 1** (port 8001) — microservice instance 1
- **Instance 2** (port 8002) — microservice instance 2
- **Client** — discovers all instances and calls a random one

## Files
| File | Description |
|------|-------------|
| `service_registry_improved.py` | Service registry server |
| `my_service.py` | Microservice (run 2 instances) |
| `client.py` | Client that discovers and calls random instance |

## How to Run

### Step 1 — Install dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2 — Start the Registry (Terminal 1)
```bash
python3 service_registry_improved.py
```

### Step 3 — Start Instance 1 (Terminal 2)
```bash
python3 my_service.py 8001
```

### Step 4 — Start Instance 2 (Terminal 3)
```bash
python3 my_service.py 8002
```

### Step 5 — Run the Client (Terminal 4)
```bash
python3 client.py
```

## Expected Output
```
Client discovering 'my-service'...
Found 2 instance(s):
  → http://localhost:8001
  → http://localhost:8002

Randomly chose: http://localhost:8002
Response: {'message': 'Hello from instance at port 8002!'}
```

## How It Works
1. Registry starts and listens on port 5001
2. Each service instance registers itself with the registry on startup
3. Instances send heartbeats every 10 seconds to stay active
4. Client queries the registry to discover all available instances
5. Client randomly picks one instance and calls it

 ##Screenshots of Terminals
 
 <img width="1124" height="838" alt="image" src="https://github.com/user-attachments/assets/ebc87e50-9ad0-4be4-b8c4-2ddaaf788f8f" />

 <img width="1227" height="861" alt="image" src="https://github.com/user-attachments/assets/afaf833b-db20-423e-8018-
  eb3a9b3bd5fd" />
  
<img width="1138" height="723" alt="image" src="https://github.com/user-attachments/assets/8d0d027a-1ff2-4d1c-959f-e3b8fe1cf0f5" />

<img width="1144" height="855" alt="image" src="https://github.com/user-attachments/assets/f4e30823-49f8-41ea-8a72-cecdb12ee2e4" />

<img width="1137" height="867" alt="image" src="https://github.com/user-attachments/assets/712967dd-a8fc-4100-a862-e26ec3025139" />





