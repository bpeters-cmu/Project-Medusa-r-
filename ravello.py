import requests
import config
import json
import time

class Ravello:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):

        headers = {'Accept': 'application/json'}
        r = requests.post('https://cloud.ravellosystems.com/api/v1/login',auth=(self.username,
         self.password), headers=headers)
        print(r.status_code)
        print(r.json())

    def get_applications(self):
        headers = {'Accept': 'application/json'}
        r = requests.get('https://cloud.ravellosystems.com/api/v1/applications',auth=(self.username,
         self.password), headers=headers)
        print(r.status_code)
        print(r.json())

    def get_blueprints(self, id=None):
        headers = {'Accept': 'application/json'}
        if not id:
            r = requests.get('https://cloud.ravellosystems.com/api/v1/blueprints',auth=(self.username,
            self.password), headers=headers)
        else:
            r = requests.get('https://cloud.ravellosystems.com/api/v1/blueprints/'+id,auth=(self.username,
            self.password), headers=headers)
        return r.json()

    def create_applications(self, quantity, bp_id=None):
        if not bp_id:
            bp_id = self.get_gold_image()
            if not bp_id:
                return None
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        print(headers)
        apps = []
        app_ids = []
        for i in range(quantity):
            milli_sec = int(round(time.time() * 1000))
            payload = {'name': 'VDI_' + str(milli_sec) ,'baseBlueprintId': bp_id, 'description': 'VDI instance'}
            r = requests.post('https://cloud.ravellosystems.com/api/v1/applications/',auth=(self.username,
            self.password), headers=headers, data=json.dumps(payload))
            print(r.status_code)
            body = r.json()
            app_ids.append(str(body['id']))
            apps.append([body['id'], body['name'], body['design']['vms'][0]['id']])
            print('test')
        self.publish_all(app_ids)
        return apps

    def get_ip(self, app_id, vm_id):
        headers = {'Accept': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/'+ app_id +'/vms/'+ vm_id +'/publicIps;deployment'
        r = requests.get(url, auth=(self.username, self.password), headers=headers)
        print(r.status_code)
        body = r.json()
        print(body)
        print(body['ips'])
        ip = body['ips'][0]
        print(ip)
        return ip

    def get_gold_image(self):
        blueprints = self.get_blueprints()
        for i in range(len(blueprints)):
            if blueprints[i]['name'].lower() == 'GoldImage'.lower():
                return blueprints[i]['id'], blueprints[i]['description']
        return None

    def publish_app(self, id):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/' + id + '/publish'
        payload = {'preferredRegion': 'us-central-1','optimizationLevel': 'PERFORMANCE_OPTIMIZED'}
        r = requests.post(url, auth=(self.username, self.password),
         headers=headers, data=json.dumps(payload))

    def publish_all(self, apps):
        print('apps', apps)
        for app in apps:
            print('test')
            self.publish_app(app)

    def stop_app(self, app_id):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/' + app_id + '/stop'
        r = requests.post(url, auth=(self.username, self.password), headers=headers)
        body = r.json()
        return body['completedSuccessfuly']

    def start_app(self, app_id):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/' + app_id + '/start'
        r = requests.post(url, auth=(self.username, self.password), headers=headers)
        body = r.json()
        return body['completedSuccessfuly']

    def delete_app(self, app_id):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/' + app_id
        print(url)
        print(self.username, self.password)
        r = requests.delete(url, auth=(self.username, self.password), headers=headers)
        print(r.text)
        return r.status_code

    def get_vm_state(self, app_id, vm_id):
        headers = {'Accept': 'application/json'}
        url = 'https://cloud.ravellosystems.com/api/v1/applications/'+ app_id +'/vms/'+ vm_id +'/state;deployment'
        r = requests.get(url, auth=(self.username, self.password), headers=headers)
        print(r.status_code)
        print(r.text)
        body = r.json()
        return r.text
