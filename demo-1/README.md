# Docker & Kubernetes

This repository describes how to deploy a docker by using kubernetes.

### Deployment

1. Launch minikube
```bash
# start minikube
minikube start --vm-driver xhyve
# or hyperkit
minikube start --vm-driver hyperkit
```

```bash
# Delete current minikube cluster 
minikube delete 
```

2. Configure `kubectl` to use Minikube
```bash
# list all available contexts
kubectl config get-contexts

# link current context to minikube
kubectl config set-context minikube

# Confirm kubectl is using minikube
kubectl config current-context
```

3. List clusters
    
    kubectl get nodes

4. Connect docker with Minikube's docker

    eval $(minikube docker-env)

so now, you can only see docker images within Minikube.

5. Build a new docker image

    docker build -t k8s-demo:0.1 .

6. Create a `pod.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: k8s-demo
  labels:
    app: k8s-demo
spec:
  containers:
    - name: k8s-demo
      image: k8s-demo:0.1
      ports:
        - containerPort: 80
```

```bash
# Create pod
kubectl create -f pod.yml

# Or,  apply the changes
kubectl apply -f pod.yml

# List pod
kubectl get pods
```

7. Create a `service.yaml`.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: k8s-demo-svc
  labels:
    app: k8s-demo
spec:
  type: NodePort
  ports:
    - port: 80
      nodePort: 30050
  selector:
    app: k8s-demo
```

```bash
# display pod labels
kubectl describe pods | grep Labels

# Create a new service
kubectl create -f service.yml
```

8. Get URL
```bash
minikube service k8s-demo-svc --url
```


### Scalable, rollout, and rollback

1. Delete pod
```bash
# Delete deployed pod
kubectl delete pod k8s-demo
```

2. Create `deployment.yaml`

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: k8s-demo-deployment
spec:
  replicas: 10
  template:
    metadata:
      labels:
        app: k8s-demo
    spec:
      containers:
        - name: k8s-demo-pod
          image: k8s-demo:0.1
          ports:
            - containerPort: 80
```

3. Create deployment
```bash
kubectl create -f deployment.yml
```

4. Get replica set (rs)
```bash
kubectl get rs
```

5. Update docker image, and `deployment.yaml` with latest image tag

6. Rollout
```bash
kubectl apply -f deployment.yaml --record=true
```

`--record=true` flag enables the deployment history

```bash
# Display deployment status in real time
kubectl rollout status deployment k8s-demo-deployment

# Display rollout history
kubectl rollout history deployment k8s-demo-deployment
```

7. Roll back
```bash
# Roll back one version
kubectl rollout undo deployment k8s-demo-deployment --to-revision=1

# Check roll back status
kubectl rollout status deployment k8s-demo-deployment
```
