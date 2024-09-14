from SeleniumLibrary.base import keyword
import requests
import json
import sys
import time
import os

class VeevaPreRequisite:

    @keyword
    def create_prerequisite_document(self, credentials,attributes,filepath):
        print("Inside CreateDocuments")
        #Get User Session
        baseurl = credentials.get("base_url")
        username = credentials.get("username")
        password = credentials.get("password")
        authurl = baseurl + '/auth'
        print("Logging into Vault...")
        logininfo = {'username': username, 'password': password}
        authResponse = requests.post(authurl, data=None, params=logininfo)
        authContent = authResponse.json()
        if authContent['responseStatus'] == 'FAILURE':
            sys.exit(authContent['responseMessage'])
        else:
            pass
        
        sessionID = authContent['sessionId']
        # print ("Logged on. Session ID is : "+sessionID)

        #Create Document
        createdocumenturl=baseurl+'/objects/documents'
        if os.path.isfile(filepath):
            files = {'file':open(filepath,'rb')}
            r=requests.post(createdocumenturl, headers={'Authorization': sessionID,'X-VaultAPI-MigrationMode':'true','Accept':'application/json'}, data=attributes, files=files)
            jsonResponse = r.json()
            # print(jsonResponse)
            return jsonResponse['id']
        else:
            # print('File doesnot exists')
            return "File doesnot exists"

    #  @keyword
    #  def create_prerequisite_document(self, credentials,attributes,filepath):
    #     print("Inside CreateDocuments")
    #     #Get User Session
    #     baseurl = credentials["base_url"]
    #     username = credentials["username"]
    #     password = credentials["password"]
    #     authurl = baseurl + '/auth'
    #     print("Logging into Vault...")
    #     logininfo = {'username': username, 'password': password}
    #     authResponse = requests.post(authurl, data=None, params=logininfo)
    #     authContent = authResponse.json()
    #     if authContent['responseStatus'] == 'FAILURE':
    #         sys.exit(authContent['responseMessage'])
    #     else:
    #         pass
        
    #     sessionID = authContent['sessionId']
    #     # print ("Logged on. Session ID is : "+sessionID)

    #     #Create Document
    #     createdocumenturl=baseurl+'/objects/documents'
    #     if os.path.isfile(filepath):
    #         files = {'file':open(filepath,'rb')}
    #         r=requests.post(createdocumenturl, headers={'Authorization': sessionID,'X-VaultAPI-MigrationMode':'true','Accept':'application/json'}, data=attributes, files=files)
    #         jsonResponse = r.json()
    #         # print(jsonResponse)
    #         return jsonResponse['id']
    #     else:
    #         # print('File doesnot exists')
    #         return "File doesnot exists"
        
    @keyword    
    def load_config_and_execute(createDocument):
        with open("create_document_config.json") as json_file:
            json_data = json.load(json_file)
            credentials = json_data['credentials']
            attributes = json_data['attributes']
            filepath = json_data['filepath']
            status = createDocument(credentials, attributes, filepath)
            print(status)
    
    

