# Service Account Keys
ACCOUNT_KEY_FILE=$(GCP_SERVICE_ACCOUNT_KEY)

# Project ID
PROJECT_ID=$(GCP_PROJECT_ID)

# Cluster
CLUSTER_NAME=$(GCP_CLUSTER_NAME)
CLUSTER_ZONE=$(GCP_CLUSTER_ZONE)
CLUSTER_NODES=$(GCP_CLUSTER_NODES)

create-cluster:
	$(shell ./scripts/1.setup-cluster)

deploy-pods:
	$(shell ./scripts/2.deploy-pods)

deploy-service:
	$(shell ./scripts/3.deploy-services)

deploy-ingress:
	$(shell ./scripts/4.deploy-ingress)

cleanup:
	$(shell ./scripts/5.cleanup)
