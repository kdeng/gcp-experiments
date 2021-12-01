# Graceful shutdowns on Cloud run.

## How to build

```bash

### Build docker image
docker build -t australia-southeast1-docker.pkg.dev/kefeng-playground/node-app/express-app:1 .


### Push docker image
docker push australia-southeast1-docker.pkg.dev/kefeng-playground/node-app/express-app:1

```


## How to deploy

```bash

gcloud run deploy graceful-demo --image=australia-southeast1-docker.pkg.dev/kefeng-playground/node-app/express-app:1

```

## How to verify

After the new service be deployed onto cloud run, you can view the logs of cloud run service.


## How to delete

```bash

 gcloud run services delete graceful-demo

 ```

## Reference

https://cloud.google.com/blog/topics/developers-practitioners/graceful-shutdowns-cloud-run-deep-dive
