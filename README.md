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


<img width="1416" height="853" alt="image" src="https://github.com/user-attachments/assets/94d56d11-3912-463a-9399-2f587cb523c6" />

## Service Mesh with Istio

**What is a Service Mesh?**
A service mesh is an infrastructure layer that handles service-to-service communication automatically — without changing any application code. Instead of your app managing traffic, security, and monitoring, the mesh handles it at the network level.
**How it works**
Every pod gets an Envoy sidecar proxy injected automatically by Istio. All traffic flows through this proxy, giving you routing control, encryption, and observability for free.
Client → Envoy sidecar → Istio control plane
                       → Pod 1 (Python app + Envoy)
                       → Pod 2 (Python app + Envoy)
The 2/2 in kubectl get pods confirms it — 1 is the Python app, 2 is the injected Envoy proxy.
Difference from the core project
Core projectWith IstioRuns onLocal machineKubernetes2 instancesStarted manuallyManaged by KubernetesLoad balancingPython random.choice()Istio ROUND_ROBIN at network levelDiscoveryPython registry (port 5001)Kubernetes DNS + IstioSecurityNonemTLS between every pod automaticallyTraffic controlNoneVirtualService (50/50 split, retries, timeouts)MonitoringNoneEnvoy metrics on every requestCrash recoveryManual restartKubernetes restarts automatically
Benefits achieved

**Traffic routing** — VirtualService splits traffic 50/50 across both instances with automatic retries
Security — mTLS encrypts all pod-to-pod communication automatically
Observability — Envoy proxy collects metrics and traces on every request

**How to run**
_Step 1 — Enable Istio sidecar injection:_
bashistioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
_Step 2 — Deploy to Kubernetes:_
bashkubectl apply -f k8s/my-service.yaml
_Step 3 — Apply Istio routing:_
bashkubectl apply -f k8s/istio-routing.yaml
_Step 4 — Verify:_
bashkubectl get pods              # both pods should show 2/2
kubectl get virtualservice    # should show my-service
kubectl get destinationrule   # should show my-service with ROUND_ROBIN
```

kubectl get pods              # both pods should show 2/2
kubectl get virtualservice    # should show my-service
kubectl get destinationrule   # should show my-service with ROUND_ROBIN
```

### Expected output
```
NAME                          READY   STATUS    RESTARTS   AGE
my-service-69b6bd9569-hz7hq   2/2     Running   0          18m
my-service-69b6bd9569-mvz6j   2/2     Running   0          18m
<img width="1440" height="1524" alt="image" src="https://github.com/user-attachments/assets/d52fa61c-89db-4895-8d5f-fd5998b98e5c" />






