
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

class Jira:
    def __init__(self, username,password):
        
        self.username = username
        self.password = password
        self.base =  "https://soundunited.atlassian.net"
        self.groups = ["external-access"]


    def GetUseringroup(self, accountid):
        
        url = "{}/rest/api/3/user/groups?accountId={}".format(self.base,accountid)
        headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
        }
        auth = HTTPBasicAuth(self.username, self.password)
        response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    auth=auth
        )
        print(url)
        d = response.json()
        
        for item in d:
            
            group = item['name']
            if group in self.groups:
                return True
            else:
                False
    def removeUserFromGroup(self, accountid):
        url = "{}/rest/api/3/group/user".format(self.base)
        auth = HTTPBasicAuth(self.username, self.password)
        
        
        headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
        }
        query = {
                "groupId": "b3d73a9e-395d-4bab-a7fe-b61ddf037130",
                "accountId":accountid
                }
        
        response = requests.request(
            "DELETE",
            url,
            params=query,
            auth=auth,
            headers=headers
        )
        print(response)
        return response

        
def main():
    
    username = input("Enter your usename: ")
    token =    input("Enter your token: ")
    j = Jira(username,token)
    df = pd.read_excel('TestExternal.xlsx',sheet_name='JIRA')
  
    for item in df['User id']:
        
        found = j.GetUseringroup(item)
        if found == True:
                print(item)
                res = j.removeUserFromGroup(item)
                print(res)

       



if __name__ == '__main__':
    main()

