#!/usr/bin/env python3
import subprocess
from pathlib import Path

envs_dir = Path("environments")
for file in envs_dir.iterdir():
    env_name = file.name
    subprocess.run(["docker", "build", "-t", f"ifc-env-check:{env_name}", "-f", file.as_posix(), "."])
