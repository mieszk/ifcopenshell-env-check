#!/usr/bin/env python3
import subprocess
from pathlib import Path

env_names = [file.name for file in sorted(Path("environments").iterdir())]

for env in env_names:
    print(f"Running env {env}")
    subprocess.call([
        "podman", "run",
        "-v", "./ifc-files:/var/ifc-files:Z",
        "-v", "./models:/var/models:Z",
        f"ifc-env-check:{env}"
    ])
