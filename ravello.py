import requests
import config
import json
import time

class Ravello:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login():

        headers = {'Accept': 'application/json'}
        r = requests.post('https://cloud.ravellosystems.com/api/v1/login',auth=(self.username,
         self.password), headers=headers)
        print(r.status_code)
        print(r.json())

    def get_applications():
        headers = {'Accept': 'application/json'}
        r = requests.get('https://cloud.ravellosystems.com/api/v1/applications',auth=(self.username,
         self.password), headers=headers)
        print(r.status_code)
        print(r.json())

    def get_blueprints(id=None):
        headers = {'Accept': 'application/json'}
        if not id:
            r = requests.get('https://cloud.ravellosystems.com/api/v1/blueprints',auth=(self.username,
            self.password), headers=headers)
        else:
            r = requests.get('https://cloud.ravellosystems.com/api/v1/blueprints/'+id,auth=(self.username,
            self.password), headers=headers)
        return r.json()

    def create_applications(bp_id, quantity):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        print(headers)

        for i in range(quantity):
            milli_sec = int(round(time.time() * 1000))
            payload = {'name': 'VDI_' + str(milli_sec) ,'baseBlueprintId': bp_id, 'description': 'VDI instance'}
            print(payload)
            r = requests.post('https://cloud.ravellosystems.com/api/v1/applications/',auth=(self.username,
            self.password), headers=headers, data=json.dumps(payload))
            print(r.status_code)
            print(r.text)

    def get_ip(app_id, vm_id):
        headers = {'Accept': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/'+ app_id +'/vms/'+ vm_id +'/publicIps;deployment'
        r = requests.get(url, auth=(self.username, self.password), headers=headers)
        print(r.status_code)
        print(r.json())

    def get_gold_image():
        blueprints = get_blueprints()
        for i in range(len(blueprints)):
            if blueprints[i]['name'] == 'GoldImage':
                return blueprints[i]['id']
        return None

    def publish_app(id):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/' + id + '/publish'
        payload = {'preferredRegion': 'us-central-1','optimizationLevel': 'PERFORMANCE_OPTIMIZED'}
        r = requests.post(url, auth=(self.username, self.password),
         headers=headers, data=json.dumps(payload))

    def publish_all(apps):
        for app in apps:
            publish_app(app)
