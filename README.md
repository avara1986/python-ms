# Installation

## Run with VM and Docker compose:

    vagrant up
    vagrant ssh

## Run with Kubernetes

First, install docker, then:

* Installing Kubernetes...
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/

* Installing Minikube...
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/


# Run the project
minikube start
cd oauth/
docker build -t oauth-python:v4 .
cd ../template/
docker build -t colors-python:v3 .


kubectl run colors-python --image=colors-python:v4 --port=5000

kubectl run oauth-python --image=oauth-python:v3 --port=5000


kubectl expose deployment colors-python --type=LoadBalancer

kubectl get services

NAME            TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
colors-python   LoadBalancer   10.100.83.27   <pending>     5000:32283/TCP   7s
kubernetes      ClusterIP      10.96.0.1      <none>        443/TCP          30m


minikube service colors-python


# Update project

Update the image of your Deployment:

kubectl set image deployment/colors-python colors-python=colors-python:v4
kubectl set image deployment/oauth-python oauth-python=oauth-python:v4