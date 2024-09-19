from datasets import Dataset
from .pandas_dataframe import load as load_df
import pyarrow as pa
from pyarrow import fs, csv, parquet
from minio import Minio as mn
from ..utils import input_or_output, get_asset_property

# def load(name)-> Dataset:
#     df = load_df(name=name)
#     return Dataset(arrow.Table.from_pandas(df))

def load_from_minio(name)-> Dataset:
    minio_url = get_asset_property(asset_name=name, property="minIO_URL")
    access_key = get_asset_property(asset_name=name, property="minIO_ACCESS_KEY")
    secret_key = get_asset_property(asset_name=name, property="minIO_SECRET_KEY")
    bucket_name = get_asset_property(asset_name=name, property="minio_bucket")
    

    use_ssl = get_asset_property(asset_name=name, property="use_ssl") if get_asset_property(asset_name=name, property="use_ssl") is not None else False
    use_ssl = True if use_ssl=="True" or use_ssl=="true" or use_ssl=="1" else False

    minio_client = mn(
        endpoint=minio_url if not ":" in minio_url else minio_url.split(":")[1][2:],
        access_key=access_key,
        secret_key=secret_key,
        secure=use_ssl 
    )

    minio = pa.fs.S3FileSystem(
        endpoint_override=minio_url,
        access_key=access_key,
        secret_key=secret_key,
        scheme="https" if use_ssl else "http")

    table = None

    folder_name = get_asset_property(asset_name=name) + "/"
    for obj in minio_client.list_objects(bucket_name, prefix=folder_name):
        csvFile = minio.open_input_file(bucket_name + "/" + obj.object_name)
        
        if table is None:
            table = pa.csv.read_csv(csvFile)
        else:
            table = pa.concat_tables([table, pa.csv.read_csv(csvFile)])

    return Dataset(table)


def load_from_disk(name)-> Dataset:
    df = load_df(name=name)
    return Dataset(pa.Table.from_pandas(df, preserve_index=False))


def load(name)-> Dataset:
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"

    if storage_type == "minio":
        return load_from_minio(name)
    elif storage_type =="filesystem":
        return load_from_disk(name)
