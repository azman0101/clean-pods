# Kubernetes: Clean pods older than X days
Delete pods older than X days. The python script uses the `Kubernetes API` and the `TOKEN` from a service account to calculate and delete pods older than X days.

I use this Docker for clean up the pods created by Airflow (Kubernetes Operator), when Airflow deploys a pod the pod get the status `Completed` or `Error` and is not delete after complete the task, also I don't want to delete them at the end of the execution because we lost the logs, so execute this Docker as a cronjob every day (at 2am) and delete the pods older than 5 days after the creation time.

## Pod status
The pods can get the following status:
- Pending
- Running
- Succeeded (Completed)
- Failed (Error)
- Unknown

## Cronjob for Kubernetes
- Replace the namespace `demo` for yours.
- Replace the service account `demo-user` for yours.
- The service account need to have permissions for list and delete pods for the namespace defined.
- The environment variable `POD_STATUS` supports a list separated by commas.

Manifest `clean-pods.yaml`
```
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: clean-pods
  namespace: demo
  labels:
    app: clean-pods
spec:
  schedule: "00 02 * * *"
  failedJobsHistoryLimit: 1
  successfulJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: demo-user
          restartPolicy: OnFailure
          containers:
          - name: clean-pods
            imagePullPolicy: Always
            image: dignajar/clean-pods:latest
            env:
              - name: API_URL
                value: "https://kubernetes.default.svc/api/"
              - name: NAMESPACE
                value: "demo"
              - name: MAX_DAYS
                value: "5"
              - name: POD_STATUS
                value: "Succeeded, Failed"
```

## Service account for Kubernetes
Service account for the namespace `demo` with enoght permissions to list and delete pods.

Manifest `service-account.yaml`
```
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-user
  namespace: demo

---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: demo-user-role
  namespace: demo
rules:
- apiGroups: [""]
  resources: ["pods","pods/exec","pods/log"]
  verbs: ["*"]

---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: demo-user
  namespace: demo
subjects:
- kind: ServiceAccount
  name: demo-user
  namespace: demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: demo-user-role
```

How to test local to a kind cluster:
```
export TOKEN=eyJhb_REDACTED
export API_URL=https://127.0.0.1:51920/
export POD_STATUS=Running
export MAX_HOURS=1
export NAMESPACE=gitlab
export STARTS_WITH=running-
```


You may want to test this chart deployment locally. We recommand you to spin up with `kind`.
To ease this step of cluster building with a local registry, download [ctlptl](https://github.com/tilt-dev/ctlptl)

Follow this install steps https://github.com/tilt-dev/ctlptl#how-do-i-install-it

```bash

cat <<EOF | ctlptl apply -f -
apiVersion: ctlptl.dev/v1alpha1
kind: Registry
name: ctlptl-registry
port: 5005
---
apiVersion: ctlptl.dev/v1alpha1
kind: Cluster
product: kind
registry: ctlptl-registry
kubernetesVersion: v1.21.14
kindV1Alpha4Cluster:
  name: cluster
  nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF
```

Once your local cluster up&running, you may want to test it:

```bash
kind get clusters

kind get nodes --name cluster
cluster-control-plane
cluster-worker
cluster-worker2
```

Then with kubectl:

```bash
kubectl get no
```

To avoid data transfert to a remote registry, retreive the registry endpoint:

```bash
ctlptl get cluster kind-cluster -o template --template '{{ .status.localRegistryHosting.host }}'
localhost:5005
```

Now your local registry is `localhost:5005`

```bash
docker buildx build --platform=linux/amd64 -t localhost:5005/clean-pods:latest .
```

## Usage of Tiltfile

Tilt

```bash
tilt up --stream=true &
```

## Live debug with Tilt and vscode

Le fichier launch.json doit être modifié pour correspondre à votre configuration, ici le port-forward vers le debugger est fait
depuis le port 5555.

```json
{
    // Utilisez IntelliSense pour en savoir plus sur les attributs possibles.
    // Pointez pour afficher la description des attributs existants.
    // Pour plus d'informations, visitez : https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python : attachement distant",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5555
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/app/",
                    "remoteRoot": "."
                }
            ],
            "justMyCode": true
        }
    ]
}
```
