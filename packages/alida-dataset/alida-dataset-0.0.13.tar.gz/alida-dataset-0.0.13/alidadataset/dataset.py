import importlib.util
from .utils import input_or_output, get_asset_property
import importlib
import pandas as pd

def load(name, load_as="path"):
    
    module = importlib.import_module("alidadataset.serializations." + load_as)
    loading_func = getattr(module, "load")

    return loading_func(name)

def save(name, dataset, save_as="path"):
    
    module = importlib.import_module("alidadataset.serializations." + save_as)
    loading_func = getattr(module, "save")

    return loading_func(name, dataset)

#TODO make it better
def infer_module(name):
    storage = get_asset_property(name, "storage_type")

    if storage == "filesystem":
        return "pandas_dataframe"
    elif storage == "minio":
        return "pandas_dataframe"
    elif storage == "kafka":
        if input_or_output(name) == "input":
            return "streaming_input"
        elif input_or_output(name) == "output":
            return "streaming_output"

def auto_load(name):
    return load(name=name, load_as=infer_module(name))

def infer_saving_module(name, dataset):
    # if isinstance(dataset, pd.DataFrame):
    #     return "_" + str(type(dataset)).split("'")[1].replace(".", "_").lower()
    # else:
    #     raise Exception(str(type(dataset)) + " type of dataset is currently not supported for saving!")
    
    # Infer type and check if it is supported
    found = importlib.util.find_spec("alidadataset.serializations." + "_" + str(type(dataset)).split("'")[1].replace(".", "_").lower())
    if found is not None:
        return "_" + str(type(dataset)).split("'")[1].replace(".", "_").lower()
    else:
        #print("Checked for "+ "alidadataset.serializations." + "_" + str(type(dataset)).split("'")[1].replace(".", "_").lower())
        raise Exception(str(type(dataset)) + " type of dataset is currently not supported for saving!")


def auto_save(name, dataset):
    return save(
        dataset=dataset, 
        name=name, 
        save_as=infer_saving_module(name=name, dataset=dataset))


