import requests
import config
import json
import time


def login():
    headers = {'Accept': 'application/json'}
    r = requests.post('https://cloud.ravellosystems.com/api/v1/login',auth=(config.ravello_username,
     config.ravello_password), headers=headers)
    print(r.status_code)
    print(r.json())

def get_applications():
    headers = {'Accept': 'application/json'}
    r = requests.get('https://cloud.ravellosystems.com/api/v1/applications',auth=(config.ravello_username,
     config.ravello_password), headers=headers)
    print(r.status_code)
    print(r.json())

def get_blueprints(id=None):
    headers = {'Accept': 'application/json'}
    if not id:
        r = requests.get('https://cloud.ravellosystems.com/api/v1/blueprints',auth=(config.ravello_username,
        config.ravello_password), headers=headers)
    else:
        r = requests.get('https://cloud.ravellosystems.com/api/v1/blueprints/'+id,auth=(config.ravello_username,
        config.ravello_password), headers=headers)
    print(r.status_code)
    print(r.json())

def create_applications(name, bp_id, quantity):
    headers = {'Accept': 'application/json'}

    for i in range(quantity):
        milli_sec = int(round(time.time() * 1000))
        payload = {'name': 'VDI_'+str(milli_sec) ,'baseBlueprintId': bp_id}
        r = requests.post('https://cloud.ravellosystems.com/api/v1/applications/',auth=(config.ravello_username,
        config.ravello_password), headers=headers)
        print(r.status_code)
        print(r.json())
    
