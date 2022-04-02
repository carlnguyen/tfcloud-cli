import requests

class TerraformCloudApi(object):
    def __init__(self, org, tf_cloud_token):
        self.org = org
        self.tf_cloud_token = tf_cloud_token
        self.headers = {
            "Authorization": f"Bearer {tf_cloud_token}",
            "Content-Type": "application/vnd.api+json"
        }
        self.base_url = "https://app.terraform.io/api/v2"

    def list_varsets(self):
        url = self.base_url + f"/organizations/{self.org}/varsets"
        req = requests.get(
                    url=url,
                    headers=self.headers,
                )
        return req.content.decode("utf-8")

    def get_varset_id(self, org, tf_cloud_token, varset_name):
        url = self.base_url + f"/organizations/{org}/varsets"
        headers = {
            "Authorization": f"Bearer {tf_cloud_token}",
            "Content-Type": "application/vnd.api+json"
        }
        req = requests.get(
                url=url,
                headers=headers,
            )
        if req.ok:
            for var in req.json()['data']:
                if var['attributes']['name'] == varset_name:
                    return var['id']
            print(req.content.decode("utf-8"))
            return None
        else:
            print(req.content.decode("utf-8"))
            return None

    @classmethod
    def create_workspace(cls, org, tf_cloud_token, branch_to_watch, working_directory, vcs_identifier, vcs_oauth_token_id, workspace_name):
        url = cls.base_url + f"/organizations/{org}/workspaces"
        headers = {
            "Authorization": f"Bearer {tf_cloud_token}",
            "Content-Type": "application/vnd.api+json"
        }
        payload = {
              "data": {
                "attributes": {
                  "name": workspace_name,
                  "resource-count": 0,
                  "terraform_version": "1.1.0",
                  "working-directory": working_directory,
                  "vcs-repo": {
                    "identifier": vcs_identifier,
                    "oauth-token-id": vcs_oauth_token_id,
                    "branch": branch_to_watch
                  },
                },
                "type": "workspaces"
              }
            }
        req = requests.post(
                url=url,
                headers=headers,
                json=payload
            )
        print(req.content.decode('utf-8'))

    #This not working
    @classmethod
    def search_workspace_by_name(cls, org, tf_cloud_token, workspace_name=""):
        url = cls.base_url + "/organizations/{org}/workspaces"
        headers = {
            "Authorization": f"Bearer {tf_cloud_token}",
            "Content-Type": "application/vnd.api+json"
        }
        params = "?search={workspace_name}" 
        req = requests.get(
                url=url,
                headers=headers,
            )
        return req.content.decode('utf-8')

    @classmethod
    def create_variable_sets(cls, org, tf_cloud_token, vars_set):
        url = cls.base_url + f"/organizations/{org}/varsets"
        headers = {
            "Authorization": f"Bearer {tf_cloud_token}",
            "Content-Type": "application/vnd.api+json"
        }
        for item in vars_set:
            payload = {
              "data": {
                  "type": "varsets",
                  "attributes": {
                    "name": item['name'],
                    "description": item['description'],
                    "global": False
                  },
                  "relationships": {
                    "workspaces": {
                        "data": item['workspaces']
                    },
                    "vars": {
                      "data": item['data']
                    }
                }
              }
            }
            req = requests.post(
                    url=url,
                    headers=headers,
                    json=payload
                )
            # Success status code is 201
            if req.ok:
                print(f"Succeeded inserting {item['name']}\n")
            else:
                print(f"Failed inserting {item['name']}")
                print(f"{req.content.decode('utf-8')}\n")

    def update_varset_workspaces(self, org, tf_cloud_token, vars_set):
        headers = {
            "Authorization": f"Bearer {tf_cloud_token}",
            "Content-Type": "application/vnd.api+json"
        }
        for item in vars_set:
            varset_id = self.get_varset_id(
                    org=org,
                    tf_cloud_token=tf_cloud_token,
                    varset_name=item['name']
                )
            if varset_id:
                url = self.base_url + f"/varsets/{varset_id}/relationships/workspaces"
                payload = {
                  "data": item['workspaces']
                }
                req = requests.post(
                        url=url,
                        headers=headers,
                        json=payload
                    )
                if req.ok:
                    print(f"Succeeded updating workspaces to {item['name']}")
                else:
                    print(f"Failed updating workspaces to {item['name']}")
                    print(req.content.decode(utf-8) + "\n")
            else:
                print(f"Varset {varset_name} is not found")

    def create_varsets(self):
        tmp = json.loads(open("varset.json"))
        varset_obj = Default
