from api.iam.api.api import API

class IAMHandlingAPI(API):
    def __init__(self, admin, user_name, user_type, operating_policy, policy_document, permissions_boundary):
        self.user_name = user_name
        self.admin = admin
        self.admin.create_user(self.user_name, permissions_boundary)
        self.access_key, self.private_key = self.admin.create_access_key(self.user_name)
        super().__init__(user_type, self.access_key, self.private_key)
        self.policy_arn = self.admin.create_policy(operating_policy, policy_document)
        self.admin.attach_policy_to_user(self.user_name, self.policy_arn)

    def __del__(self):
        self.admin.detach_policy_from_user(self.user_name, self.policy_arn)
        self.admin.delete_policy(self.policy_arn)
        self.admin.delete_access_key(self.user_name, self.access_key)
        self.admin.delete_user(self.user_name)