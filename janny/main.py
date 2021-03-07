from janny.utils import get

def get_resources():
    apis = get("/apis/")
    apiv1 = get("/api/v1")

    resource_objs = list()
    resource_objs.append(apiv1.resources)

    for g in apis.groups:
        resource_objs.append(get("/apis/" + g.preferredVersion.groupVersion).resources)

    for resources in resource_objs:
        for r in resources:
            if "/" not in r.name and r.namespaced:
                yield r.name

def main():
    for r in get_resources():
        print(r)
