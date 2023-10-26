
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
class Jira:
    def __init__(self, username, token):
        
        self.username = username
        self.password = token
        self.base =  "https://omg-test.atlassian.net"
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
    def addUsertoGroup(self, accountid):
        url = "{}/rest/api/3/group/user".format(self.base)
        auth = HTTPBasicAuth(self.username, self.password)
        
        
        headers={
                "Accept": "application/json",
                
                "Content-Type": "application/json"
        }
        query = {
                "groupId": "ebb28936-e7dc-4fd3-95ad-b67995895fdd",
                
                }
        payload = json.dumps( {
                "accountId": accountid
                } )
        print(payload)
        response = requests.request(
            "POST",
            url,
            params=query,
            data=payload,
            auth=auth,
            headers=headers
        )
        print(response)
        return response

        
def main():
    path = 'External.xlsx'
    username = input("Enter your usename: ")
    token =  input("Enter your token: ")
    j = Jira(username,token)
    df = pd.read_excel('TestExternal.xlsx',sheet_name='JIRA')
    
    for item in df['User id']:
        
        
        res = j.addUsertoGroup(item)
        print(res.text)
  
       



if __name__ == '__main__':
    main()

