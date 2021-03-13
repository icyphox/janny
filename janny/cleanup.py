import time
import json
import datetime
from types import SimpleNamespace

from janny.utils import parse_delta, RUNNING
from janny.auth import SESSION as s
from janny.config import API_HOST, logger


def clean_up(
    url: str, resource_obj: SimpleNamespace, object_name: str, kill_time: str, namespace: str
):
    """
    Parse the kill_time and create call send_delete_request(); create an event after deletion.
    """
    delta = parse_delta(kill_time)
    secs = delta.total_seconds()
    time.sleep(secs)
    logger.info(f"Slept for {kill_time}, cleaning resource {object_name} now")
    send_delete_request(url, resource_obj.name, object_name, namespace)

    message = f"Successfully deleted {resource_obj.name}/{object_name}"
    now = datetime.datetime.utcnow().isoformat() + "Z"
    event = {
        "metadata": {
            "namespace": namespace,
            "generateName": "janny-",
        },
        "type": "Normal",
        "count": 1,
        "action": f"Deleted resource {object_name}",
        "eventTime": now,
        "firstTimestamp": now,
        "reason": "ResourceDeleted",
        "message": message,
        "involvedObject": {
            "apiVersion": "v1",
            "name": object_name,
            "namespace": namespace,
            "kind": resource_obj.kind,
        },
        "reportingComponent": "janny",
        "reportingInstance": "janny",
        "source": {
            "component": "janny",
        },
    }

    create_event(event, namespace)


def send_delete_request(
    url: str, kube_resource: str, resource_name: str, namespace: str
):
    """
    Sends a DELETE request to the resource.
    """
    api_url = f"{API_HOST}{url}/namespaces/{namespace}/{kube_resource}/{resource_name}"
    response = s.delete(api_url, params={"propagationPolicy": "Background"})
    logger.info(f"Sent delete request to {kube_resource}/{resource_name}")
    response_json = json.loads(response.content)
    if "Success" not in response_json.values():
        logger.error(f"Deletion failed! Recieved: {response_json}")

    RUNNING.remove(resource_name)


def create_event(event: dict, namespace: str):
    """
    Create an Event for resource deletion.
    FIXME: Maybe don't hardcode the group URL?
    """

    api_url = f"{API_HOST}/api/v1/namespaces/{namespace}/events"
    response = s.post(api_url, json=event)
    response_json = json.loads(response.content)
    if "Failure" not in response_json.values():
        logger.info(f"Created event")
    else:
        logger.error(f"Failed to create event! Recieved: {response_json}")
