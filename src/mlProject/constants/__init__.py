from pathlib import Path
import os

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

CONFIG_FILE_PATH = PROJECT_ROOT / "config" / "config.yaml"
PARAMS_FILE_PATH = PROJECT_ROOT / "params.yaml"
SCHEMA_FILE_PATH = PROJECT_ROOT / "schema.yaml"