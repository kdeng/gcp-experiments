#!/usr/bin/env bash

# Force the shell to immediately if a single command exits with a non-zero exit value.
set -e

# Turn on / off the debug mode
#set -x

PROJECT=kdeng-gae-demos
CLUSTER_NAME=kdeng-gke-cluster
CLUSTER_ZONE=australia-southeast1

# Delete the cluster
echo -e "\n-> Deleting kubernetes cluster '$CLUTER_NAME' ..."
gcloud deployment-manager deployments delete $CLUSTER_NAME --project=$PROJECT

# Disable Kubernetes Engine
echo -e "\n-> Disabling Deployment Manager APIs ..."
gcloud services disable deploymentmanager.googleapis.com --project=$PROJECT
