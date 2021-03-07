import requests
import logging
import os

logging.basicConfig(level=logging.INFO)


def kube_auth():
    session = requests.Session()

    # We're in-cluster
    if not os.path.exists(os.path.expanduser("~/.kube/config")):
        with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as f:
            token = f.read()
        session.verify = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
        session.headers.update({"Authorization": f"Bearer {token}"})
        logging.info("Authenticated with the API server")
    else:
        logging.info("Not in-cluster, continuing as is")

    return session

SESSION = kube_auth()
