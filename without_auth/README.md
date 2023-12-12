# NATS-Setup and Deploy Applicaiton

## NATS setup

```shell
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm upgrade --install nats nats/nats -f auth-values.yaml
```

## Deploy Application to connects NATS with authentication

```bash
## Build Docker Image
docker build  -t naresh240/nats-auth-test:v1
docker push naresh240/nats-auth-test:v1

## Deploy Application
kubectl apply -f deployment.yaml
```