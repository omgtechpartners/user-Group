
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import *

class Jira:
    def __init__(self, username,password):
        
        self.username = username
        self.password = password
        self.base =  "https://soundunited.atlassian.net" #UPDATE THIS END POINT RESPECTIVE INSTANCE
        self.groups = ["external-access"]#UPDATE THE GROUP NAME RESPECTIVE TO THE INSTANCE
       


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
                "groupId": "b3d73a9e-395d-4bab-a7fe-b61ddf037130",#UPDATE GROUP ID
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
    df = pd.read_excel('export-users.xlsx',sheet_name='export-users')
    datetime = pd.to_datetime(df['Last seen in Jira Software - soundunited']).dt.date
    quarterDate = date(2023,7,1)
    for item in df['User id']:
        
        found = j.GetUseringroup(item)
        if found == True:
            print(datetime[0])
            if datetime[0] < quarterDate:
                print(item)
                res = j.removeUserFromGroup(item)
                print(res)

       



if __name__ == '__main__':
    main()

