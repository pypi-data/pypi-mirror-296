from botocore.exceptions import ClientError
import json
from aws_wand.iam.api.api import API

class IAMAdmin(API):
    USER_TYPE = 'iam'
    def __init__(self, access_key: str, secret_key: str):
        super().__init__(self.USER_TYPE, access_key, secret_key)

    def create_user(self, user_name: str, permission_boundaries: list):
        try:
            response = self.iam.create_user(UserName=user_name)
            return response
        except ClientError as e:
            print(f'Error: {e}')
            return None

    def delete_user(self, user_name: str):
        try:
            response = self.iam.delete_user(UserName=user_name)
            return response
        except Exception as e:
            print(f'{e}')
            return None

    def create_access_key(self, user_name: str):
        try:
            response = self.iam.create_access_key(UserName=user_name)
            access_key, secret_key = response['AccessKey']['AccessKeyId'], response['AccessKey']['SecretAccessKey']
            return access_key, secret_key
        except Exception as e:
            print(f'{e}')
            return None, None

    def delete_access_key(self, user_name: str, access_key: str):
        try:
            response = self.iam.delete_access_key(UserName=user_name, AccessKeyId=access_key)

            return response
        except Exception as e:
            print(f'{e}')
            return None

    def attach_policy_to_user(self, user_name: str, policy_arn: str):
        try:
            self.iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
        except Exception as e:
            print(f'{e}')
            return None

    def detach_policy_from_user(self, user_name: str, policy_arn: str):
        try:
            self.iam.detach_user_policy(UserName=user_name, PolicyArn=policy_arn)
        except Exception as e:
            print(f'{e}')
            return None

    def create_policy(self, policy_name: str, policy_document: dict):
        try:
            response = self.iam.create_policy(PolicyName=policy_name, PolicyDocument=json.dumps(policy_document))

            return response['Policy']['Arn']
        except Exception as e:
            print(f'{e}')
            return None

    def delete_policy(self, policy_arn: str):
        try:
            response = self.iam.delete_policy(PolicyArn=policy_arn)

            return response
        except Exception as e:
            print(f'{e}')
            return None