from janny.utils import get


def get_resource_urls():
    apis = get("/apis/")
    apiv1 = get("/api/v1")

    resource_urls = dict()
    resource_urls["/api/v1"] = apiv1.resources

    for g in apis.groups:
        version = g.preferredVersion.groupVersion
        resource_urls["/apis/" + version] = get(
            "/apis/" + g.preferredVersion.groupVersion
        ).resources

    return resource_urls


def main():
    get_resource_urls()
