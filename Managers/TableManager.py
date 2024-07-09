import google.auth.transport.requests
from google.oauth2 import service_account
import requests
import json

class secops():
    def __init__(self):
        pass
        
    def get_datatable_json(CREDS, PROJECT_ID, REGION, SECOPS_ID, TABLE_NAME, siemplify):
        # This class will assemble and return a dict object of a Google SecOps data table. If there's any errors
        #  the class will still return a dict with the error.
        COLUMNS = []
        JSON_RESULT = []

        # First we'll retrieve the columns
        API_BASE = "https://" + REGION + "-chronicle.googleapis.com"
        PARENT = "/v1alpha/projects/" + PROJECT_ID + "/locations/us/instances/" + SECOPS_ID
        URL = API_BASE + PARENT + "/dataTables/" + TABLE_NAME
        credentials = service_account.Credentials.from_service_account_info(
            CREDS, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        hd = {
            "Authorization": "Bearer " + credentials.token,
            "Content-Type": "application/json"
        }
        siemplify.LOGGER.info('Get columns endpoint: ' + URL)
        req = requests.get(URL, headers=hd, timeout=10)
        if 'Result not found' in req.text:
            return(json.loads(req.text))
        js = json.loads(req.text)
        for c in js['columnInfo']:
            COLUMNS.append(c['originalColumn'])

        # Now let's get the rows of data
        URL = API_BASE + PARENT + "/dataTables/" + TABLE_NAME + '/dataTableRows'
        siemplify.LOGGER.info("Get rows endpoint: " + URL)

        req = requests.get(URL, headers=hd, timeout=10)
        js = json.loads(req.text)
        for r in js['dataTableRows']:
            rinline = {}
            n = r['name'].split("/")
            id = {
                "id" : n[9]
            }
            rinline.update(id)
            for i in r['values']:
                row = {
                    COLUMNS[r['values'].index(i)] : i
                }
                rinline.update(row)
            JSON_RESULT.append(rinline)  
            rinline = {}
        return(JSON_RESULT)