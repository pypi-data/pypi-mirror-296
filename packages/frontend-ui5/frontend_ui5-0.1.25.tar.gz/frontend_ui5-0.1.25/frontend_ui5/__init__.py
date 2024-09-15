import json
import logging
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(Path(__file__).parent.name)  # the logger's name is the parent directory's name

frontend_version = "UNKNOWN"
compatible_versions = []

try:
    path = Path(__file__).parent / "static" / "resources" / "app.version.json"
    with open(path, "r") as file:
        frontend_version = json.load(file)["version"].split("-")[0]
except Exception as ex:
    logger.error(f"Error reading frontend version: {ex}")

versions_to_check = f"{frontend_version}/{settings.BACKEND_VERSION}"

with open(settings.BASE_DIR / "compatibility.txt", "r") as file:
    compatible_versions = file.readlines()

if versions_to_check not in compatible_versions:
    logger.critical(f"Version mismatch: {
        versions_to_check} is not in the compatibility list")
else:
    logger.info(f"Version check passed: {
        versions_to_check} is in the compatibility list")
