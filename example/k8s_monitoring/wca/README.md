Getting started
===============

To run wca in daemon set: 

1. Build image (from main project repo)

```
make REPO=100.64.176.12:80/ wca_docker_devel
#and push to your 
sudo docker push 100.64.176.12:80/wca:devel
```


2. (optionally) Overwrite image name to your local repository in kustomization.yaml

```yaml
...
# kustomization.yaml
images:
  - name: wca
    newName: REPO/wca
    newTag: devel
```

3. (optionally) Choose (**disable the default goal=service**) nodes to deploy owca using node selector

```yaml
# daemonset.yaml
spec:
    node-selector:
        kubernetes.io/hostname: node12

```

3. Create namespace

```shell
kubectl create namespace wca
```

4. Deploy wca (using kustomize)

```shell
kubectl apply -k .
```

Optionally, you can use token to connect to Kube API Server 

```
SERVICE_ACCOUNT=wca

# Get the serviceaccount token secret name
SECRET=$(kubectl get serviceaccount ${SERVICE_ACCOUNT} -o json | jq -Mr '.secrets[].name | select(contains("token"))')

# Extract the Bearer token from the Secret and decode
kubectl get secret ${SECRET} -o json | jq -Mr '.data.token' | base64 -d > token

# Extract ca.crt from the Secret and decode
kubectl get secret ${SECRET} -o json | jq -Mr '.data["ca.crt"]' | base64 -d > ca.crt

# Get the API Server location
echo https://$(kubectl -n default get endpoints kubernetes --no-headers | awk '{ print $2 }') > server
```

```
TOKEN=$(cat token)
APISERVER=$(cat server)
curl -s $APISERVER/openapi/v2  --header "Authorization: Bearer $TOKEN" --cacert ca.crt | less
```
