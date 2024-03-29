from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import boto3
from tqdm import tqdm

import pandas as pd
import io
import os


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class S3DataConnector(BaseDataConnector):
    __REQUIRED_CONF__ = {"config": ["AWS_S3_BUCKET",
                                    "AWS_ACCESS_KEY_ID",
                                    "AWS_SECRET_KEY_ID",
                                    "AWS_SESSION_TOKEN", ]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_config = utils.load_config(
            [
                "AWS_S3_BUCKET", 
                "AWS_ACCESS_KEY_ID", 
                "AWS_SECRET_KEY_ID", 
                "AWS_SESSION_TOKEN",
            ]
        )

    def get_data(self, path, *args, **kwargs):
        """
        Reads data from the AWS S3 Bucket.

        Args:
            path: a string representing the location of the file in the bucket

        Returns:
            DataFrame containing data from the bucket.
        """
        df = self._load_data(path, self.aws_config)
        return df

    def save_data(self, data, path, *args, **kwargs):
        """
        Saves data into the S3 Bucket.

        Args:
            data: Data to be written into the bucket
            path: a string representing the location of the file in the bucket

        Returns:
            None
        """
        self._save_data(data, path, self.aws_config)


    @classmethod
    def _load_data(self, path, config, *args, **kwargs):
        """
        Reads files within the AWS S3 Bucket.

        Args:
            path: a string representing the location of the file in the bucket
            config: a dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.


        Returns:
            Data on file.
        """
        client = self._get_client(config)
        bucket = config.get("AWS_S3_BUCKET")
        extension = path.split(".")[-1]

        response = client.get_object(Bucket=bucket, Key=path)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            self.log(f"Successful S3 get_object response. Status - {status}")
            source_data = response.get("Body").read()
            if extension == "csv":
                data = pd.read_csv(io.StringIO(source_data),
                                encoding="utf-8", **kwargs)
            elif extension == "parquet" or extension == "pq":
                data = pd.read_parquet(io.BytesIO(source_data), **kwargs)
            elif extension == "orc":
                data = pd.read_orc(io.BytesIO(source_data), **kwargs)
            else:
                self.log("Unsupported file type provided: %s" % extension)
            self.log("Successfully loaded data from %s into DataFrame." % path)

        else:
            self.log(f"Unsuccessful S3 get_object response. Status - {status}")

        return data

    def _save_data(self, data, path, config, *args, **kwargs):
        """
        Saves Data into AWS S3 Bucket

        Args:
            data: Data to be written into the bucket
            path: a string representing the location of the file in the bucket
            config: a dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

        Returns:
            None
        """
        # get client
        client = self._get_client(config)
        bucket = config.get("AWS_S3_BUCKET")
        extension = path.split(".")[-1]

        if extension == ".csv":
            f = io.StringIO()
            data.to_csv(f, index=False)
        elif extension == ".pq" or extension == "parquet":
            f = io.BytesIO()
            data.to_parquet(f, index=False)
        else:
            raise Exception("Unsupported file type for path: %s" %(path))
        f.seek(0)

        response = client.put_object(
            Bucket=bucket, Key=path, Body=f.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            self.log(f"Successful S3 put_object response. Status - {status}")
        else:
            self.log(f"Unsuccessful S3 put_object response. Status - {status}")


    def _get_client(self, config):
        """
        Returns the AWS S3 client.

        Args:
            config: a dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

        Returns:
            An AWS S3 client.
        """
        client = boto3.client(
            "s3",
            aws_access_key_id=config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=config.get("AWS_SESSION_TOKEN"),
        )
 
        return client
