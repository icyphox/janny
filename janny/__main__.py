import argparse
import sys

from .main import main
from janny.config import logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--included-resources",
        help="Comma separated list of Kubernetes resources for janny to clean up.",
        type=str,
    )
    parser.add_argument(
        "--namespaces",
        help="Comma separated list of namespaces for janny to scan.",
        type=str,
        default="default",
    )
    args = parser.parse_args()

    namespace_list = list()
    if not args.included_resources:
        parser.print_help()
        sys.exit(1)
    elif not args.namespaces:
        logger.info("No namspaces provided, using 'default'")
    elif args.namespaces:
        namespace_list = args.namespaces.replace(" ", "").split(",")

    include_list = args.included_resources.replace(" ", "").split(",")

    while True:
        main(include_list, namespace_list)
