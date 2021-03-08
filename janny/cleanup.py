import time
import logging
import datetime

from janny.utils import parse_delta, get
from janny.auth import SESSION as s
from janny.config import API_HOST

logging.basicConfig(level=logging.INFO)


def clean_up(
    url: str, kube_resource: str, resource_name: str, kill_time: str, namespace: str
):
    delta = parse_delta(kill_time)
    secs = delta.total_seconds()
    time.sleep(secs)
    logging.info(f"Slept for {kill_time}. Cleaning resource {resource_name} now.")
    send_delete_event(url, kube_resource, resource_name, namespace)
    logging.info(f"Sent delete event to {kube_resource}/{resource_name}")


def send_delete_event(url: str, kube_resource: str, resource_name: str, namespace: str):
    api_url = f"{API_HOST}/{url}/namespaces/{namespace}/{kube_resource}/{resource_name}"
    s.delete(api_url, params={"propagationPolicy": "Background"})