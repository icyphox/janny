import requests
import os

from janny.config import logger


def kube_auth():
    session = requests.Session()

    # We're in-cluster
    if not os.path.exists(os.path.expanduser("~/.kube/config")):
        with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as f:
            token = f.read()
        session.verify = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
        session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Authenticated with the API server")
    else:
        logger.info("Not in-cluster, continuing as is")

    return session


SESSION = kube_auth()
