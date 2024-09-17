# __init__.py

import importlib.resources as pkg_resources
import pandas as pd

def get_data_file(filename):
    """Access a file from the 'data' folder."""
    return pkg_resources.files('rarego_kge.data') / filename

from rarego_kge import get_data_file