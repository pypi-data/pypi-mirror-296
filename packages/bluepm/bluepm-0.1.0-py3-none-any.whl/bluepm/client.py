import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class BlueAPIClient:
    def __init__(self, token_id=None, secret_id=None, company_id=None, project_id=None):
        self.base_url = "https://api.blue.cc/graphql"  # Replace with actual API endpoint

        # Try to get token_id and secret_id from environment variables first
        self.token_id = token_id or os.environ.get('BLUE_TOKEN_ID')
        self.secret_id = secret_id or os.environ.get('BLUE_SECRET_ID')

        if not self.token_id or not self.secret_id:
            raise ValueError("Token ID and Secret ID must be provided either as arguments or as environment variables (BLUE_TOKEN_ID and BLUE_SECRET_ID)")

        self.company_id = company_id or os.environ.get('BLUE_COMPANY_ID')
        self.project_id = project_id or os.environ.get('BLUE_PROJECT_ID')
        
        self.headers = {
            "x-bloo-token-id": self.token_id,
            "x-bloo-token-secret": self.secret_id,
        }
        
        if self.company_id:
            self.headers["x-bloo-company-id"] = self.company_id
        if self.project_id:
            self.headers["x-bloo-project-id"] = self.project_id
        
        self.transport = RequestsHTTPTransport(
            url=self.base_url,
            headers=self.headers,
            use_json=True,
        )
        
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    def execute_query(self, query, variables=None):
        try:
            result = self.client.execute(gql(query), variable_values=variables)
            return result  # Return the raw result without any processing
        except Exception as e:
            print(f"An error occurred while executing the query: {str(e)}")
            return None

  # Function to get the project list
    def get_project_list(self):
        query = """
        query ProjectListQuery($companyId: String!) {
          projectList(filter: { companyIds: [$companyId] }) {
            items {
              name
              id
              uid
            }
          }
        }
        """
        variables = {"companyId": self.company_id}
        return self.execute_query(query, variables)
    
    # Function to get the project list with full details
    def get_project_list_full_details(self):
        query = """
        query ProjectListQuery($companyId: String!) {
          projectList(filter: { companyIds: [$companyId] }) {
            items {
              id
              uid
              slug
              name
              description
              archived
              color
              icon
              createdAt
              updatedAt
              allowNotification
              position
              unseenActivityCount
              todoListsMaxPosition
              lastAccessedAt
              isTemplate
              automationsCount
              totalFileCount
              totalFileSize
              todoAlias
            }
            pageInfo {
              totalPages
              totalItems
              page
              perPage
              hasNextPage
              hasPreviousPage
            }
          }
        }
        """
        variables = {"companyId": self.company_id}
        return self.execute_query(query, variables)
    
    # Function to create a new project
    def create_project(self, name):
        mutation = """
        mutation CreateProject($input: CreateProjectInput!) {
          createProject(input: $input) {
            id
          }
        }
        """
        variables = {
            "input": {
                "name": name,
                "companyId": self.company_id
            }
        }
        return self.execute_query(mutation, variables)
    
    # Method to get list of records across a company
    def get_records_company(self):
      query = """
      query ListOfRecords($companyId: String!) {
        todoQueries {
          todos(
            filter: { companyIds: [$companyId] }
            sort: [position_ASC]
          ) {
            items {
              id
              uid
              position
              title
              text
              html
              startedAt
              duedAt
              timezone
              color
              cover
              done
            }
            pageInfo {
              totalPages
              totalItems
              page
              perPage
              hasNextPage
              hasPreviousPage
            }
          }
        }
      }
      """
      variables = {"companyId": self.company_id}
      return self.execute_query(query, variables)
