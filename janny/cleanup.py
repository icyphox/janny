import time
import json

from janny.utils import parse_delta, RUNNING
from janny.auth import SESSION as s
from janny.config import API_HOST, logger


def clean_up(
    url: str, kube_resource: str, resource_name: str, kill_time: str, namespace: str
):
    """
    Parse the kill_time and create call send_delete_event().
    """
    delta = parse_delta(kill_time)
    secs = delta.total_seconds()
    time.sleep(secs)
    logger.info(f"Slept for {kill_time}. Cleaning resource {resource_name} now.")
    send_delete_event(url, kube_resource, resource_name, namespace)


def send_delete_event(url: str, kube_resource: str, resource_name: str, namespace: str):
    """
    Sends a DELETE request to the resource.
    """
    api_url = f"{API_HOST}{url}/namespaces/{namespace}/{kube_resource}/{resource_name}"
    response = s.delete(api_url, params={"propagationPolicy": "Background"})
    logger.info(f"Sent delete event to {kube_resource}/{resource_name}")
    response_json = json.loads(response.content)
    if "Success" not in response_json.values():
        logger.error(f"Deletion did not succeed. Recieved: {response_json}")

    RUNNING.remove(resource_name)
