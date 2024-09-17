print("This version of 'noises' is not designed for use. Consider it Pre-Alpha")

import importlib.metadata
import requests

try:
    installed_version = importlib.metadata.version("noises")
except importlib.metadata.PackageNotFoundError:
    print("The 'noises' package is not installed.")
    exit(1)

url = "https://pypi.org/pypi/noises/json"
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Failed to fetch version info from PyPI: {e}")
    exit(1)

try:
    latest_version = response.json()["info"]["version"]
except KeyError:
    print("Failed to parse version info from PyPI response.")
    exit(1)

if installed_version != latest_version:
    print(f"A new version of 'noises' is available! Installed: {installed_version}, Latest: {latest_version}. Update with: 'pip install --upgrade noises'")
else:
    print(f"'noises' is up to date (version {installed_version}).")