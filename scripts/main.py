import models
import config.settings
import requests
import os 

workspace_id = os.getenv('CLOCKIFY_WORKSPACE_ID')

base_api_url = 'https://api.clockify.me/api/'
headers = {'X-Api-Key': os.getenv('CLOCKIFY_API_KEY')}

def test():
    for page in range(200):
        url = "{}/workspaces/{}/timeEntries/?page=${}".format(base_api_url, workspace_id, page)
        response = requests.get(url, headers)
        print(response)


if __name__ == "__main__":
    test()