from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

from google.cloud import storage 
from google.oauth2 import service_account
from google.resumable_media.requests import ResumableUpload
from google.auth.transport.requests import AuthorizedSession
from tqdm import tqdm

import pandas as pd
import io 
import os 


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class GCSDataConnector(BaseDataConnector):
    __REQUIRED_CONF__ = {"config": ["GOOGLE_PROJECT"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gcs_service_account_keyfile = self._get_config("GOOGLE_SERVICEACCOUNT_KEYFILE", None)
        self.gcs_project = self._get_config("GOOGLE_PROJECT")



    def get_data(self, path, *args, **kwargs):
        df = self._load_data(path, self.gcs_service_account_keyfile, self.gcs_project)
        return df

    def save_data(self, data, path, *args, **kwargs):
        self._save_data(data, path, self.gcs_service_account_keyfile, self.gcs_project)


     #load data into df
    @classmethod
    def _load_data(self, path, keyfile, project, **kwargs):
        client = self._get_client(keyfile, project)
        bucket = path.split("/")[0]
        file_path = "/".join(path.split("/")[1:])
        extension = path.split(".")[-1]
        source_data = client.get_bucket(bucket).blob(file_path).download_as_string()

        if extension == "csv":
            data = pd.read_csv(io.StringIO(source_data), encoding="utf-8", **kwargs)
        elif extension == "parquet" or extension == "pq":
            data = pd.read_parquet(io.BytesIO(source_data), **kwargs)
        elif extension == "orc":
            data = pd.read_orc(io.BytesIO(source_data), **kwargs)
        else:
            self.log("Unsupported file type provided: %s" % extension)
        self.log("Successfully loaded data from %s into DataFrame." %path)
        
        return data 

    def _save_data(self, data, path, keyfile, project, *args, **kwargs):
        # get client
        client = self._get_client(keyfile, project)

        #get blob based on path
        bucket = path.split("/")[0]
        file_path = "/".join(path.split("/")[1:])
        extension = path.split(".")[-1]
        blob = client.get_bucket(bucket).blob(file_path)

        format = self._get_format(extension)

        if extension == ".csv": 
            f = io.StringIO()
            data.to_csv(f, index=False)
        elif extension == ".pq" or extension == "parquet": 
            f = io.BytesIO()
            data.to_parquet(f, index=False)
        else:  
            raise Exception("Unsupported file type for path: %s" %
                            (file_path))
        f.seek(0)

        url = "https://www.googleapis.com/upload/storage/v1/b/%s/o?uploadType=resumable" % bucket
        chunksize = (1024 * 1024)  # 1MB
        upload = ResumableUpload(url, chunksize)
        transport = AuthorizedSession(credentials=client._credentials)
        upload.initiate(transport, f, {"name": blob.name}, format)

        with tqdm(total=upload.total_bytes, desc="Upload %s to %s bucket" %(file_path, bucket)) as pbar:
            while not upload.finished:
                upload.transmit_next_chunk(transport)
                pbar.update(chunksize)

        self.log("Successfully uploaded %s" %path)


    def _get_client(self, key_path, project): 
        if key_path is not None: 
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=[
                    "https://www.googleapis.com/auth/cloud-platform"],
            )

            client = storage.Client(credentials=credentials,project=credentials.project_id)
        elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None: 
            client = storage.Client(project=project)
        else: 
            raise Exception("Must either provide GOOGLE_KEYFILE in lolpop configuration or set environment variable GOOGLE_APPLICATION_CREDENTIALS.")

        return client
    
    def _get_format(self, extension): 
        if extension == ".csv": 
            return "text/csv"
        else: 
            return "application/octet-stream"