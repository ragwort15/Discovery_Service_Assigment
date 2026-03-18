# Microservice with Service Discovery

## Overview
A microservice system with service registration, discovery, and random load balancing built in Python. Includes an optional Service Mesh implementation using Istio on Kubernetes.

---

## Architecture
- **Service Registry** (port 5001) — central registry where services register themselves
- **Instance 1** (port 8001) — microservice instance 1
- **Instance 2** (port 8002) — microservice instance 2
- **Client** — discovers all instances and calls a random one

---

## Files

| File | Description |
|---|---|
| `service_registry_improved.py` | Service registry server |
| `my_service.py` | Microservice (run 2 instances) |
| `client.py` | Client that discovers and calls random instance |
| `k8s/my-service.yaml` | Kubernetes deployment (2 replicas) |
| `k8s/istio-routing.yaml` | Istio VirtualService + DestinationRule |

---

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

### Expected Output
```
Client discovering 'my-service'...
Found 2 instance(s):
  → http://localhost:8001
  → http://localhost:8002

Randomly chose: http://localhost:8002
Response: {'message': 'Hello from instance at port 8002!'}
```

---

## How It Works
1. Registry starts and listens on port 5001
2. Each service instance registers itself with the registry on startup
3. Instances send heartbeats every 10 seconds to stay active
4. Client queries the registry to discover all available instances
5. Client randomly picks one instance and calls it

---

## Optional: Service Mesh with Istio

### What is a Service Mesh?
A service mesh is an infrastructure layer that handles service-to-service communication automatically without changing any application code. Instead of the app managing traffic, security, and monitoring, the mesh handles it at the network level via an **Envoy sidecar proxy** injected into every pod.
```
Client → Envoy sidecar → Pod 1 (Python app + Envoy)
                       → Pod 2 (Python app + Envoy)
```

### Core Project vs Istio Mesh

| | Core Project | With Istio |
|---|---|---|
| Runs on | Local machine | Kubernetes |
| 2 instances | Started manually | Managed by Kubernetes |
| Load balancing | Python `random.choice()` | ROUND_ROBIN at network level |
| Discovery | Python registry (port 5001) | Kubernetes DNS + Istio |
| Security | None | mTLS between every pod automatically |
| Traffic control | None | VirtualService with 50/50 split |
| Monitoring | None | Envoy metrics on every request |
| Crash recovery | Manual restart | Kubernetes restarts automatically |

### Benefits
- **Traffic routing** — VirtualService splits traffic 50/50 across both instances
- **Security** — mTLS encrypts all pod-to-pod communication automatically
- **Observability** — Envoy proxy collects metrics and traces on every request

### How to Run with Istio

**Step 1 — Enable Istio**
```bash
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

**Step 2 — Deploy to Kubernetes**
```bash
kubectl apply -f k8s/my-service.yaml
```

**Step 3 — Apply Istio routing**
```bash
kubectl apply -f k8s/istio-routing.yaml
```

**Step 4 — Verify**
```bash
kubectl get pods
kubectl get virtualservice
kubectl get destinationrule
```

**Expected output**
```
NAME                          READY   STATUS    RESTARTS   AGE
my-service-69b6bd9569-hz7hq   2/2     Running   0          18m
my-service-69b6bd9569-mvz6j   2/2     Running   0          18m
```
The `2/2` confirms both the Python app and Envoy sidecar are running in each pod.

---
<img width="934" height="376" alt="image" src="https://github.com/user-attachments/assets/d7d9fa0c-1fdb-4dd2-a590-4a63f68a60c5" />



