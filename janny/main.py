import threading
import logging

from janny.utils import get
from janny.cleanup import clean_up

logging.basicConfig(level=logging.INFO)


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
        if "janny.ttl" in vars(r.metadata.annotations):
            print(r.metadata.annotations)
            kill_time = vars(r.metadata.annotations)["janny.ttl"]
            t = threading.Thread(
                target=clean_up,
                args=[url, resource.name, r.metadata.name, kill_time, namespace],
            )
            logging.info(f"Starting cleaner thread for {r.metadata.name}")
            t.start()


def main():
    filtered = filter_included_resources(["deployments"], get_resource_urls())
    for f in filtered:
        spawn_clean_up_job(f, "default")
