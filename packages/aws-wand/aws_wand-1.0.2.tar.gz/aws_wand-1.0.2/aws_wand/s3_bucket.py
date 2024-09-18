from aws_wand.iam.iam_handling_api import IAMHandlingAPI
from botocore.exceptions import ClientError
import os

class S3Bucket(IAMHandlingAPI):
    USER_TYPE = 's3'
    OPERATING_POLICY = 'ds_policy'
    PERMISSIONS_BOUNDARY = ['s3:*']

    @classmethod
    def create_policy_document(cls, bucket_name):
        return {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Action': [
                        's3:ListBucket'
                    ],
                    'Resource': f'arn:aws:s3:::{bucket_name}'
                },
                {
                    'Effect': 'Allow',
                    'Action': [
                        's3:GetObject',
                        's3:PutObject',
                        's3:DeleteObject'
                    ],
                    'Resource': f'arn:aws:s3:::{bucket_name}/*'
                }
            ]
        }

    def __init__(self, admin, bucket_name, user_name):
        self.bucket_name = bucket_name
        super().__init__(admin, user_name, self.USER_TYPE, self.OPERATING_POLICY,
                         self.create_policy_document(self.bucket_name), self.PERMISSIONS_BOUNDARY)

    def upload_file(self, filename: str, object_name: str = None):
        if object_name is None:
            object_name = os.path.basename(filename)
        try:
            self.s3.upload_file(filename, self.bucket_name, object_name)
        except Exception as e:
            print(f'{e}')

    def upload_files(self, directory: str, folder_name: str = None):
        for filename in os.listdir(directory):
            if folder_name is None:
                self.upload_file(os.path.join(directory, filename))
            else:
                self.upload_file(os.path.join(directory, filename),
                                 object_name=os.path.join(folder_name, os.path.basename(filename)))

    def delete_all_objects(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)

            if 'Contents' in response:
                for obj in response['Contents']:
                    self.s3.delete_object(Bucket=self.bucket_name, Key=obj['Key'])

        except ClientError as e:
            print(f'{e}')

    def __del__(self):
        self.delete_all_objects()
        super().__del__()