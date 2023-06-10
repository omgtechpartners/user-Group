from datetime import datetime
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
from requests.auth import HTTPBasicAuth
import json
import logging

    

class FilterUpdate:
    def __init__(self, serverUrl, serverUsername,serverPassword,cloudUrl,cloudUsername,cloudPassword):
        self.serverUrl= serverUrl
        self.serverUsername = serverUsername
        self.serverPassword = serverPassword

        self.cloudUrl = cloudUrl
        self.cloudUsername = cloudUsername
        self.cloudPassword = cloudPassword

    
    def readJiraGroupUser(self):
        auth = HTTPBasicAuth(self.serverUsername,self.serverPassword)
        headers={"Content-Type":"application/json","Accept":"application/json"}
        response = requests.get( self.serverUrl, headers=headers,auth=auth)
        if response.status_code != 200: 
                #logging.info()
                logging.info("Rest call failed while reading the JIRA ID"+str(response.text))

        

    def readJiraUser(self,owner,logging):

            auth = HTTPBasicAuth(self.serverUsername,self.serverPassword)
            if(owner!=''):
                owners = owner.replace(')','').split('(')
                if(len(owners)>1):
                    print(self.serverUrl+owners[1])
                    headers={"Content-Type":"application/json","Accept":"application/json"}
                    response = requests.get( self.serverUrl+owners[1], headers=headers,auth=auth)
                    if response.status_code != 200: 
                        #logging.info()
                        logging.info("Rest call failed while reading the JIRA ID"+str(response.text))
                    
                    else:
                        responsedata = json.loads(response.text)
                        if(len(responsedata)>0):
                             print(responsedata[0]['emailAddress'])
                             logging.info("emailAddress: "+responsedata[0]['emailAddress'])
                             return responsedata[0]['emailAddress']
                        else:
                            return None
                 

    def readJiraUserAccountId(self,emailaddress,logging):
         auth = HTTPBasicAuth(self.cloudUsername,self.cloudPassword)
         if emailaddress!=None:
            headers = {"Content-Type":"application/json","Accept":"application/json"}
            url = self.cloudUrl+'/user/search/?query={}'.format(emailaddress)
            response = requests.get(url, headers=headers,auth=auth)
            if response.status_code != 200: 
                #logging.info()
                logging.indo("Rest call failed while reading the ACCOUNT ID"+str(response.status_code))
                    
            else:
                responsedata = json.loads(response.text)
                if(len(responsedata)>0):
                    print(responsedata[0]['accountId'])
                    return responsedata[0]['accountId']
                else:
                    return None
    
    
             

def main():
    df = pd.read_excel('Filters.xlsx')
    print(df)
    now = datetime.now()
    logging.basicConfig(filename='/Users/manishkumar/Desktop/Sound United Project/filterlogs/filterLogs'+str(now)+'.log', level=logging.INFO)
    logging.info('Starting Processing of Change Rquest log')
    for index, row in df.iterrows():
       #print(row['Filter'], row['Owner'],row['SQL'])
        cloudUrl = "https://soundunited.atlassian.net/rest/api/3/"
        cloudUsername = "manish.kumar@omgtechpartners.com"
        cloudPassword = "yx2JimcUvFYCZKOY3msRE9A9"

        serverUrl= 'https://dm-atlassian.rickcloud.jp/jiraapi/2/group/member?groupname=A/V Solutions'
        serverUsername = "Manish.Kumar"
        serverPassword = ""

        cloudFIlter = FilterUpdate(serverUrl,serverUsername,serverPassword,cloudUrl,cloudUsername,cloudPassword)
        
        cloudFIlter.readJiraGroupUser()
       
        logging.info("Filter ID: "+str(filterid))
        logging.info('Filter Name:'+str(row['Filter']))
       
        Owner = str(row['Owner'])
        jirauser = cloudFIlter.readJiraUser(Owner,logging)
        accountid = cloudFIlter.readJiraUserAccountId(jirauser,logging)
        cloudFIlter.updateFilterPermission(filterid,logging)
        cloudFIlter.updateFilterOwener(accountid,filterid,logging)



if __name__ == '__main__':
    main()

