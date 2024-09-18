import os
from sgqlc.operation import Operation
from sgqlc.endpoint.requests import RequestsEndpoint
from .schema import schema

class BlueAPIClient:
    def __init__(self, token_id=None, secret_id=None, company_id=None, project_id=None):
        self.token_id = token_id or os.environ.get('BLUE_TOKEN_ID')
        self.secret_id = secret_id or os.environ.get('BLUE_SECRET_ID')
        self.company_id = company_id or os.environ.get('BLUE_COMPANY_ID')
        self.project_id = project_id or os.environ.get('BLUE_PROJECT_ID')

        if not all([self.token_id, self.secret_id, self.company_id]):
            raise ValueError("Missing required credentials. Please provide token_id, secret_id, and company_id.")

        self.endpoint = RequestsEndpoint(
            "https://api.blue.cc/graphql",
            {
                "x-bloo-token-id": self.token_id,
                "x-bloo-token-secret": self.secret_id,
                "x-bloo-company-id": self.company_id,
                "x-bloo-project-id": self.project_id
            }
        )

    def execute(self, operation):
        data = self.endpoint(operation)
        return operation + data

    def query(self):
        return Operation(schema.Query)

    def mutation(self):
        return Operation(schema.Mutation)
    
    # Helper function to get project names
    def get_project_names(self, company_id):
        op = self.query()
        op.project_list(filter={'companyIds': [company_id]}).items.name()
        return self.execute(op)