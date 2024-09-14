import sys
import time
import requests
import json
from ratelimit import limits, sleep_and_retry
from SeleniumLibrary.base import keyword

class RunVeevaJob:
    ###SECONDS = 30
    #@limits(calls=no_of_calls, period=period_in_secs)

    @keyword
    @sleep_and_retry
    @limits(calls=int("1"), period=int("10"))
    def startJob(self,sessionid, joburl):
        time.sleep(10)
        r = requests.post(joburl, headers={'Authorization': sessionid})
        response = r.json()
        print(response)
        if response['responseStatus'] == 'FAILURE':
            responseStatus="FAILURE"
        elif response['responseStatus'] == 'SUCCESS':
            responseStatus="SUCCESS"
        else:
            responseStatus=response['responseStatus']
        return responseStatus

    @keyword
    def getJobID(self, sessionid, jobname, jobmonitorurl):
        print(jobname)
        time.sleep(10)
        r = requests.get(jobmonitorurl, headers={'Authorization': sessionid})
        response = r.json()
        #print(response['jobs'])
        jobdict={}
        jobslist = response['jobs']
        jobid = 0
        for job in jobslist:
            jobdict=job
            if jobdict['title'] == jobname:
                jobid=jobdict['job_id']
                #print(jobid)
        return jobid
        
    @keyword
    # def get_session_start_job(self, json_file):
    #     with open(json_file) as json_file:
    #         json_data = json.load(json_file)
    def get_session_start_job(self, json_data):
            baseurl = json_data['base_url']
            username = json_data['username']
            password = json_data['password']
            #no_of_calls = json_data['no_of_calls']
            #period_in_secs = json_data['period_in_secs']
            authurl = baseurl + '/auth'
            credentials = {'username': username, 'password': password}
            authResponse = requests.post(authurl, data=None, params=credentials)
            authContent = authResponse.json()
            print(authContent)
            if authContent['responseStatus'] == 'FAILURE':
                sys.exit(authContent['responseMessage'])  
            else:
                pass
            sessionID = authContent['sessionId']
            print ("Logged on. Session ID is : "+sessionID)
            #jobids = json_data['jobids']
            jobnames= json_data['jobnames']
            print(jobnames)
            jobnamelist = jobnames.split(',')
            print(jobnamelist)
            jobStatus={}
            jobMonitorURL=baseurl+"/services/jobs/monitors"
            jobid = 0
            for jobname in jobnamelist:
                print("Inside for")
                #GET JOB ID - Call Job Monitor
                jobid=self.getJobID(sessionID, jobname, jobMonitorURL)
                joburl=baseurl+"/services/jobs/start_now/"+str(jobid)
                #CALL API
                status=self.startJob(sessionID, joburl)
                jobStatus[jobid]=status
            return status
