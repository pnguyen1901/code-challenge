# EQ - call center simulation

Example flask app for running a simulation of a call center with x number of consumers and agents.


## Getting started
This app was deployed and tested on **Python 3.7**. Using older and newer versions of Python might cause some issues.

It is recommended that you create a Python virtual env before installing the dependencies to maintain isolation between environments and avoiding dependency clashing.

```shell
cd ..\
python3.7 -m venv py3.7
source py3.7/bin/activate
```

You should now see that the virtual environment has been activated with the prefix `virtualenv` name on your terminal.
```shell
(py3.7)Phats-iMac:EQ-callcenter phatnguyen$
```

Run this app locally:

```shell
pip install -r requirements.txt
python run.py
```

Download [Postman](https://www.postman.com/downloads/).
```
Create a POST request to http://localhost:5000/api/v1/run_simulation with a body including the two parameters:
- noOfCustomers
- noOfAgents
```
![](assets/postman.png)

If you don't pass the parameters, the simulation will run with the default values of **1000** and **20** for the customers and agents respectively.

## Deploy to Kubernetes minikube

Install [docker desktop](https://www.docker.com/products/docker-desktop) and [kubernetes - minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) and run:

```shell
# Minikube is a VM so you need to build the Docker image in the VM not in your localhost.
# So first, you need to get an interactive shell in the VM by opening up terminal and run.
eval $(minikube docker-env)

# Now you can build and deploy as normal.
docker build -t everquote:1.0 .
kubectl apply -f resources.yaml
```
To access the service in the Kubernetes cluster, you need to forward a local port to a port on the Pod

```shell
# run this first to get the pod name
kubectl get pods -n everquote

# results should look something similar to this
NAME                          READY   STATUS    RESTARTS   AGE
callcenter-778fb94744-88qfr   1/1     Running   0          9s

kubectl port-forward podname localPort:podPort
# if you see this on the terminal, the service is now accessible and can be reached using Postman.
Forwarding from 127.0.0.1:5000 -> 5000
Forwarding from [::1]:5000 -> 5000
Handling connection for 5000
Handling connection for 5000
```

## Project Structure




Core files to run the program.

    ├── project
    │   ├── __init__.py
    │   ├── .env
    │   ├── .env.example
    │   ├── callcenter.py    
    │   └── dataModels.py

This file fires up the Flask server.


    ├── run.py

This file is responsile for Kubernetes deployment.

    ├── resources.yaml

All test-related files. 

    ├── tests
    │   └── fixtures
    │   │     ├── __init__.py
    │   │     ├── agent.py
    │   │     ├── callcenter.py
    │   │     └── customer.py
    │   ├── confest.py
    │   ├── test_callcenter.py
    │   ├── test_data_models.py
    │   └── test_flask_app.py

Asset files: list of all 50 stats and images used for README.md

    ├── assets
    │   ├── listOf50States.txt
    │   └── postman.png

## Tests

Test suites are set up using `pytest` framework. Read more about [`Pytest`](https://pytest.org/en/stable/index.html)

Current test suites cover the following items: 
- class Customer 
- class Agent
- The public interface createSimulation of class CallCenter
- route /api/v1/run_simulation of the Flask app

Standalone unit tests run with:

```shell
pytest --junitxml=tests/results/output
```

conftest.py is created to share fixture functions across test files. The nice thing about conftest.py is you don’t need to import the fixture you want to use in a test, it automatically gets discovered by pytest. Just simply pass the fixure function as a parameter in the test class.

    ├── tests
    │   └── confest.py


## Future Enhancements

- Improve the logic of the simulation by leveraging multi-threading to dynamically monitor each agent and return customer's voicemail once they are left.
- Employ StringIO and Response object from flask to allow download the xlsx report file on HTTP request instead of writing to the local directory.
- Add a CI/CD pipeline to be able to automate unit testing before deploying to Kubernetes cluster.

