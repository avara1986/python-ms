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

Arrancamos nuestro Kubernetes:

    minikube start
    eval $(minikube docker-env)
    kubectl config use-context minikube

Podemos verlo en el navegador con:

    minikube dashboard

Creamos la imagen de nuestros proyectos:

    cd oauth/
    docker build -t oauth-python:v1 .
    cd ../template/
    docker build -t colors-python:v1 .

## Metodo 1 (yaml)

    kubectl create -f backend.yaml
    kubectl create -f frontend.yaml
    minikube service colors

## Método 2 (manual)

Creamos los pods en kubernetes

    kubectl run colors --image=colors-python:v4 --port=5000
    
    kubectl run oauth --image=oauth-python:v1 --port=5000

Exponemos los pods

    $ kubectl expose deployment colors --type=LoadBalancer
    $ kubectl expose deployment oauth

    $ kubectl get services
    
    NAME            TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
    colors-python   LoadBalancer   10.100.83.27   <pending>     5000:32283/TCP   7s
    kubernetes      ClusterIP      10.96.0.1      <none>        443/TCP          30m


    minikube service colors


# Update project

Update the image of your Deployment:

    kubectl set image deployment/colors colors-python=colors-python:v4
    kubectl set image deployment/oauth oauth-python=oauth-python:v4
    
    
# Clean up
Now you can clean up the resources you created in your cluster:

    kubectl delete service colors
    kubectl delete service oauth
    kubectl delete deployment colors
    kubectl delete deployment oauth
  
Optionally, force removal of the Docker images created:

    docker rmi colors-python:v1 oauth-python:v1 -f
    
Optionally, stop the Minikube VM:

    minikube stop
    eval $(minikube docker-env -u)
    
Optionally, delete the Minikube VM:

    minikube delete