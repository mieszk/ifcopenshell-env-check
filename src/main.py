import os

from models_generator.models_generator import create_models

env_name = os.getenv("ENV_NAME")
ifcs_dir = "/var/ifc-files"
models_dir = "/var/models"

create_models(ifcs_dir, models_dir, env_name)
