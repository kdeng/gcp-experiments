# Basic configuration
PROJECT_ID=$(GCP_PROJECT_ID)
CLUSTER_NAME=$(GCP_CLUSTER_NAME)
CLUSTER_ZONE=$(GCP_CLUSTER_ZONE)
CLUSTER_NODES=$(GCP_CLUSTER_NODES)

# Machine type list: n1-standard-1, f1-micro, g1-small
CLUSTER_MACHINE_TYPE=f1-micro
ACCOUNT_KEY=$(GCP_SERVICE_ACCOUNT_KEY)

login:
	$(info Activating service account with $(ACCOUNT_KEY))
	gcloud auth activate-service-account --key-file=$(ACCOUNT_KEY)
	gcloud auth list

create-cluster:
	$(info Creating cluster ...)
	$(info Project ID    = $(PROJECT_ID))
	$(info Cluster Name  = $(CLUSTER_NAME))
	$(info Cluster Zone  = $(CLUSTER_ZONE))

	gcloud container clusters create "$(CLUSTER_NAME)" --project "$(PROJECT_ID)" \
		--zone "$(CLUSTER_ZONE)" --machine-type "$(CLUSTER_MACHINE_TYPE)" \
		--image-type "COS" --disk-size "100" --num-nodes "$(CLUSTER_NODES)" --network "default" --enable-cloud-logging \
		--enable-cloud-monitoring --addons HttpLoadBalancing --enable-autoupgrade --enable-autorepair --enable-basic-auth \
		--scopes "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

	gcloud container clusters get-credentials "$(CLUSTER_NAME)" --zone australia-southeast1-a --project "$(PROJECT_ID)"

delete-cluster:
	gcloud container clusters delete "$(CLUSTER_NAME)" --project "$(PROJECT_ID)" --zone "$(CLUSTER_ZONE)" --quiet

build-app-images:
	docker build -t gcr.io/$(PROJECT_ID)/istiotest:1.0 ./code/code-only-istio
	docker build -t gcr.io/$(PROJECT_ID)/istio-opencensus-simple:1.0 ./code/code-opencensus-simple
	docker build -t gcr.io/$(PROJECT_ID)/istio-opencensus-full:1.0 ./code/code-opencensus-full

push-app-images:
	-gcloud auth configure-docker --quiet
	docker push gcr.io/$(PROJECT_ID)/istiotest:1.0
	docker push gcr.io/$(PROJECT_ID)/istio-opencensus-simple:1.0
	docker push gcr.io/$(PROJECT_ID)/istio-opencensus-full:1.0

delete-app-images:
	-gcloud auth configure-docker --quiet
	-gcloud container images delete gcr.io/$(PROJECT_ID)/istiotest:1.0 --quiet
	-gcloud container images delete gcr.io/$(PROJECT_ID)/istio-opencensus-simple:1.0  --quiet
	-gcloud container images delete gcr.io/$(PROJECT_ID)/istio-opencensus-full:1.0 --quiet

deploy-apps:
	kubectl apply -f ./configs/kubernetes/services.yaml
	-sed -e 's~<PROJECT_ID>~$(PROJECT_ID)~g' ./configs/kubernetes/deployments.yaml | kubectl apply -f -

get-apps:
	kubectl get pods && kubectl get svc && kubectl get svc istio-ingressgateway -n istio-system

deploy-istio:
	-kubectl create namespace istio-system
	kubectl apply -f ./configs/istio/istio.yaml
	kubectl label namespace default istio-injection=enabled --overwrite
	sleep 60
	kubectl delete pod -n istio-system -l app=prometheus

ingress:
	kubectl apply -f ./configs/istio/ingress.yaml

egress:
	kubectl apply -f ./configs/istio/egress.yaml
