import importlib.util
from .utils import input_or_output, get_asset_property
import importlib
from fileioutilities import FileIO



def download(name, path):
    fileio = FileIO(name)
    fileio.download(local_path=path)
    return path

def auto_save(name, path):
    fileio = FileIO(name)
    fileio.upload(local_path=path)

