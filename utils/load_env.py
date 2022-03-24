import os
import sys


def get_env_secrets(key):
    """retrive specific environment secret"""
    try:
        return os.environ[key]
    except KeyError:
        print(f"Environment variable {key} missing")
        sys.exit(1)
