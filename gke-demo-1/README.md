# Docker & Kubernetes

This repository describes how to deploy a docker by using kubernetes.

### Deployment

1.Launch minikube

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

2.Configure `kubectl` to use Minikube

```bash
# list all available contexts
kubectl config get-contexts

# link current context to minikube
kubectl config set-context minikube

# Confirm kubectl is using minikube
kubectl config current-context
```

3.List clusters

    kubectl get nodes

4.Connect docker with Minikube's docker

    eval $(minikube docker-env)

so now, you can only see docker images within Minikube.

5.Build a new docker image

    cd app && docker build -t k8s-demo .

6.Create pod

```bash
# Create pod
kubectl create -f ./config/pod.yml

# Or,  apply the changes
kubectl apply -f ./config/pod.yml

# List pod
kubectl get pods
```

7.Create service

```bash
# display pod labels
kubectl describe pods | grep Labels

# Create a new service
kubectl create -f ./config/service.yml
```

8.Get URL

```bash
minikube service k8s-demo-svc --url
```

### Scalable, rollout, and rollback

1.Delete pod

```bash
# Delete deployed pod
kubectl delete pod k8s-demo
```

2.Create deployment

```bash
kubectl apply -f ./config/deployment.yml
```

3.Get replica set (rs)

```bash
kubectl get rs
```

4.Update docker image, and `deployment.yaml` with latest image tag

5.Rollout

```bash
kubectl apply -f ./config/deployment.yaml --record=true
```

`--record=true` flag enables the deployment history

```bash
# Display deployment status in real time
kubectl rollout status deployment k8s-demo-deployment

# Display rollout history
kubectl rollout history deployment k8s-demo-deployment
```

6.Roll back

```bash
# Roll back one version
kubectl rollout undo deployment k8s-demo-deployment --to-revision=1

# Check roll back status
kubectl rollout status deployment k8s-demo-deployment
```
