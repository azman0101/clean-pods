"""Clean Pods - Kubernetes pod cleanup utility."""

import json
import os

# Determine the path to the manifest file (assumes project root is one level up)
manifest_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".release-please-manifest.json")
try:
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    # Use the key matching the package name, or fallback to the first value
    if "app" in manifest:
        __version__ = manifest["app"]
    else:
        __version__ = next(iter(manifest.values()))
except Exception:
    __version__ = "0.0.0"  # fallback or raise an error as appropriate