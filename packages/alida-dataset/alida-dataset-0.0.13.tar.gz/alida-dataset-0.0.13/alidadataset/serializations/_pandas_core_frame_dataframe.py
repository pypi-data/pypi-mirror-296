from pandas import DataFrame
from pandas import read_csv
import pandas as pd
from ..utils import input_or_output, get_asset_property
from dsioutilities import Dataset
import os

def load_dataframe_from_minio(name):
    input_dataset = Dataset(name, dataset_type="tabular")
    if isinstance(input_dataset.get_path(), list):
        df = pd.concat([pd.read_csv(filename) for filename in input_dataset.get_path()])
    else:
        df = pd.read_csv(input_dataset.get_path())
    return df


def load(name)-> DataFrame:
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"
    
    if storage_type == "minio":
        return load_dataframe_from_minio(name)
    elif storage_type =="filesystem":
        if os.path.isdir(get_asset_property(asset_name=name)):
            list_of_files = next(os.walk(get_asset_property(asset_name=name)), (None, None, []))[2]
            return pd.concat([pd.read_csv(os.path.join(get_asset_property(asset_name=name), filename)) for filename in list_of_files if filename.endswith(".csv")])
        else:
            return read_csv(get_asset_property(asset_name=name))


def save(name, dataset):
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"
    
    if storage_type == "filesystem":
        path = get_asset_property(asset_name=name)
        dataset.to_csv(path, index=False)

    elif storage_type == "minio":
        # path = Dataset(name, dataset_type="tabular").get_path()
        # dataset.to_csv(path, index=False)
        dataset.to_csv(Dataset(name, dataset_type="tabular").get_path(), index=False)
