from janny.utils import get


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


def check_annotations(resource_tuple: tuple, namespace: str) -> list:
    """
    Returns a list of resource tuples which have the 'janny.ttl'
    annotation.
    """
    url, resource = resource_tuple
    resource_list = get(f"{url}/namespaces/{namespace}/{resource.name}")
    annotated_list = list()
    for r in resource_list.items:
        if "janny.ttl" in vars(r.metadata.annotations):
            annotated_list.append(r)

    return annotated_list


def main():
    filtered = filter_included_resources(["deployments"], get_resource_urls())
    for f in filtered:
        print(check_annotations(f, "default"))
