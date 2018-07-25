#!/usr/bin/env bash

# Re-tag a docker image
docker tag osnz/test:latest asia.gcr.io/kdeng-gae-demos/spring-boot-with-jib:latest

# Push docker image to GCR
docker push asia.gcr.io/kdeng-gae-demos/spring-boot-with-jib:latest

# List all versions
gcloud container images list-tags asia.gcr.io/kdeng-gae-demos/spring-boot-with-jib