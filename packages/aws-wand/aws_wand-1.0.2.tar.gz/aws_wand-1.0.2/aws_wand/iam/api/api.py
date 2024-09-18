import boto3

class API:
    def __init__(self, api_id: str, access_key: str, secret_key: str):
        setattr(self, api_id, boto3.client(api_id, aws_access_key_id=access_key, aws_secret_access_key=secret_key))