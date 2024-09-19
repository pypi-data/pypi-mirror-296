import sys
import os
import tomli

def get_version():
    pyproject_path = os.path.join(os.path.dirname(__file__), '../pyproject.toml')
    with open(pyproject_path, 'rb') as f:
        pyproject_data = tomli.load(f)
    return pyproject_data['project']['version']

# Python APM SDK version
SDK_VERSION = get_version()  

# Define constants for Python version and SDK version
PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
