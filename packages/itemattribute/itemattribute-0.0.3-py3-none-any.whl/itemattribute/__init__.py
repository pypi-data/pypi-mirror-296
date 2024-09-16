from .item_attribute import ItemAttribute

import importlib.resources
import json
import  os


dir = os.path.dirname(os.path.abspath(__file__))

with importlib.resources.open_text("itemattribute", "version.json") as file:
    __version__ = json.load(file)['version']
