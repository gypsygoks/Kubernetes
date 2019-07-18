# Kubernetes - Python
# Deploying the Kubernetes in linux(ubuntu - 18.04) machine in a cluster of machines. 
- [Introduction](#Introduction)
- [Pre-requisites](#pre-requisites)
- [Installation and configuration](#Installation-and-configuration)

# Introduction
In this post, we will deploy a Kubernetes in linux(ubuntu - 18.04) in master and slave configuration and will deploy the prometheus and nginx docket using deployment.

# Pre-requisites
Before we get started installing the Prometheus stack on AWS. 
* Ensure you install the latest version of python package is installed.
* Get the respective node access, it support both key and password.

# Installation and configuration
Clone the project locally to your linux machine.

Make configuration changes by edit the on_premise.conf file.
Please find the reference below.
```
...
[master_kubernetes]
ip = 10.10.10.10
username = ubuntu
private_key = <path_to_private_key>
...
...
[slave_kubernetes]
ip = 10.10.10.11
username = ubuntu
private_key = <path_to_private_key>
....
```
The above configuration is where you want to install the kubernetes cluster.

In this project we used the following provision.
* Ubuntu - 18.04
* Kubenetes
* Docker
* Prometheus

You can any number of cluster node in this for kubernetes.

