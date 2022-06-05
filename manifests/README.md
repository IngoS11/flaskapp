# Kubernetes deployment files for the Flask App
## Secret Template Files
Before use, copy the *-secret.template.yaml files to *.secret.yaml files and generate
base64 endoded secrets for the fields.
```
> cp base/flaskapp/secret.template.yaml base/flaskapp/secret.yaml
```

## Install Zalando Postgres Operator
For the Postgres database the installation uses the [Zalando Postgres Operator](https://github.com/zalando/postgres-operator/blob/master/docs/quickstart.md#deployment-options). It must
be install on the kubernetes cluster before applying the application
```
kubectl apply -k github.com/zalando/postgres-operator/manifests
```

## Deployment
Deploy with Kustomize via `kubectl apply -k base`

## Initializing the Database
As of now the database must be initialized by hand by connecting to the flaskapp container
and using flask db reset
```
> kubectl exec -it $(kubectl get pods -l app=flaskapp -o jsonpath='{.items[*].metadata.name}') -- /bin/bash
>> flask db reset
>> exit
```