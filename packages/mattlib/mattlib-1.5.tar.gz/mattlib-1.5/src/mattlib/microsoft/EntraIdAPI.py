from .BaseMicrosoftAPI import BaseMicrosoftAPI

class EntraIdAPI(BaseMicrosoftAPI):
    def connect(self, tenant_ID, app_ID, secret_key):
       super().connect(tenant_ID, app_ID, secret_key,
                        'https://graph.microsoft.com/.default')
       self.subscriptions = None
       self.resource_groups = None
       self.servers = None

    def list_auditLogs_signIn(self):
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url)
        return response

    def methods(self):
        methods = [
            {
                'method_name': 'list_auditLogs_signIn',
                'method': self.list_auditLogs_signIn,
                'format': 'json'
            }
        ]
        return methods
