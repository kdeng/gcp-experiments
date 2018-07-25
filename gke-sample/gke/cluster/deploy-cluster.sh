#!/usr/bin/env bash

# Force the shell to immediately if a single command exits with a non-zero exit value.
set -e

# Turn on / off the debug mode
#set -x

# Project ID
PROJECT_ID=kdeng-gae-demos

# Cluster Name
CLUSTER_NAME=kdeng-gke-cluster

# Cluster Zone
CLUSTER_ZONE=australia-southeast1-a

# Number of nodes
NUM_NODES=1

echo -e "Current project configuration is:"
echo -e "-> Project ID      = $PROJECT_ID"
echo -e "-> Cluster Name    = $CLUSTER_NAME"
echo -e "-> Cluster Zone    = $CLUSTER_ZONE"
echo -e "-> Number Of Nodes = $NUM_NODES"
echo -e "\n"

# Enable Kubernetes Engine
echo -e "\n-> Enabling Deployment Manager APIs ..."
gcloud services enable deploymentmanager.googleapis.com --project=$PROJECT_ID

# Create a new cluster
echo -e "\n-> Creating cluster '$CLUSTER_NAME' ..."
gcloud deployment-manager deployments create $CLUSTER_NAME \
    --quiet \
    --template=cluster.py \
    --properties=CLUSTER_NAME:$CLUSTER_NAME,CLUSTER_ZONE:$CLUSTER_ZONE,NUM_NODES:$NUM_NODES \
    --project=$PROJECT_ID

#
#gcloud container clusters get-credentials kdeng-gke-cluster --zone australia-southeast1-a --project kdeng-gae-demos

# List all clusters under project
echo -e "\n-> Listing all clusters under project '$PROJECT_ID' ..."
gcloud container clusters list \
    --project=$PROJECT_ID