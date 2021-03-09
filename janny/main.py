import threading
import itertools

from janny.utils import get
from janny.cleanup import clean_up
from janny.config import logger


RUNNING = []


def get_resource_urls() -> list:
    """
    Returns a list of tuples of all namespaced resources.
    """
    apis = get("/apis/")
    apiv1 = get("/api/v1")

    resource_urls = list()
    for r in apiv1.resources:
        if r.namespaced and "/" not in r.name:
            resource_urls.append(("/api/v1", r))

    for g in apis.groups:
        version = g.preferredVersion.groupVersion
        for r in get("/apis/" + version).resources:
            if r.namespaced and "/" not in r.name:
                resource_urls.append(("/apis/" + version, r))

    return resource_urls


def filter_included_resources(include_list: list, resource_tuple_list: list) -> list:
    """
    Filters the list returned by get_resource_urls() according to
    a list of included resources.
    """
    filtered_resource_list = list()
    for k, v in resource_tuple_list:
        if v.name in include_list:
            filtered_resource_list.append((k, v))

    return filtered_resource_list


def spawn_clean_up_job(resource_tuple: tuple, namespace: str):
    """
    Spawns a clean up job -- runs on a new thread.
    """
    url, resource = resource_tuple
    resource_list = get(f"{url}/namespaces/{namespace}/{resource.name}")
    for r in resource_list.items:
        try:
            if (
                "janny.ttl" in vars(r.metadata.annotations)
                and r.metadata.name not in RUNNING
            ):
                logger.info(
                    f"New resource to clean up: {resource.name}/{r.metadata.name}: {vars(r.metadata.annotations)}"
                )
                kill_time = vars(r.metadata.annotations)["janny.ttl"]
                t = threading.Thread(
                    target=clean_up,
                    args=[url, resource.name, r.metadata.name, kill_time, namespace],
                )
                logger.info(f"Starting cleaner thread for {r.metadata.name}")
                RUNNING.append(r.metadata.name)
                t.start()
        except AttributeError:
            pass


def main(include_list, namespace_list):
    filtered = filter_included_resources(include_list, get_resource_urls())
    for f, n in itertools.product(filtered, namespace_list):
        spawn_clean_up_job(f, n)
