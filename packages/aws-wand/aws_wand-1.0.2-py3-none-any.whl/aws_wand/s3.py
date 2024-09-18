from aws_wand.iam.iam_handling_api import IAMHandlingAPI


class S3(IAMHandlingAPI):
    USER_TYPE = 's3'
    OPERATING_POLICY = 's3_policy'
    PERMISSIONS_BOUNDARY = ['s3:*']

    @classmethod
    def create_policy_document(cls):
        return {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Action': [
                        's3:CreateBucket',
                        's3:DeleteBucket',
                        's3:PutBucketOwnershipControls'
                    ],
                    'Resource': 'arn:aws:s3:::*'
                }
            ]
        }

    def __init__(self, admin, user_name):
        super().__init__(admin, user_name, self.USER_TYPE, self.OPERATING_POLICY, self.create_policy_document(),
                         self.PERMISSIONS_BOUNDARY)
        self.automated_destroying_buckets = []

    def create_bucket(self, bucket_name, region='eu-central-1', destroy_flag=True):
        try:
            response = self.s3.create_bucket(
                ACL='private',
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': region,
                },
                ObjectOwnership='BucketOwnerEnforced'
            )
            if destroy_flag:
                self.automated_destroying_buckets.append(bucket_name)
            return response
        except Exception as e:
            print(f'{e}')
            return None

    def delete_bucket(self, bucket_name):
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            print(f'{e}')
            return None

    def __del__(self):
        if self.automated_destroying_buckets:
            for bucket_name in self.automated_destroying_buckets:
                self.delete_bucket(bucket_name)
        super().__del__()