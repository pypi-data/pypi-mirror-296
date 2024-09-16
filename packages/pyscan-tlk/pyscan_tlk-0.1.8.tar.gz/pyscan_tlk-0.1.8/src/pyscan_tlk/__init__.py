import importlib.resources
import json
import os


dir = os.path.dirname(os.path.abspath(__file__))

with importlib.resources.open_text("pyscan_tlk", "version.json") as file:
    __version__ = json.load(file)['version']
