import json
from pathlib import Path

import setuptools

PARENT_FOLDER = Path(__file__).parent

is_test = False

package_name = "frontend_ui5"
resources = "static/resources"

# check if sap.ui.core.js is present in the static folder:
if (PARENT_FOLDER / package_name / resources / "sap-ui-core.js").exists():
    print("sap-ui-core.js found - deploying as test package")
    is_test = True

with open(PARENT_FOLDER / package_name / resources / "app.version.json", "r") as f:
    version_json = f.read()
    version = json.loads(version_json)["version"].split("-")[0]
    VERSION = f"{version}.dev1" if is_test else version


print(f"Version: {VERSION}")

setuptools.setup(
    name="frontend-ui5",
    version=VERSION,
    license="Apache License 2.0",
    packages=['frontend_ui5'],
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=["Django>=5.1"],
)
