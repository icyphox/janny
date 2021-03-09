import os
import logging

# Logging setup
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

API_HOST = os.getenv("JANNY_API_HOST") or "https://kubernetes.default"
