from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import TableManager
import google.auth.transport.requests
from google.oauth2 import service_account
import json
import requests

siemplify = SiemplifyAction()
table = siemplify.extract_action_param("Data Table Name", print_value=True)
data = siemplify.extract_action_param("Data to add (comma-separated)", print_value=True)
sa_json = siemplify.extract_configuration_param('Integration',"Service Account JSON")
sa_json = json.loads(sa_json)
project_name = siemplify.extract_configuration_param('Integration',"GCP Project ID")
region = siemplify.extract_configuration_param('Integration',"GCP Region")
tenant = siemplify.extract_configuration_param('Integration',"Google SecOps Tenant ID")


@output_handler
def main():
    
    # Create the endpoint url
    API_BASE = "https://" + region + "-chronicle.googleapis.com"
    PARENT = "/v1alpha/projects/" + project_name + "/locations/" + region + "/instances/" + tenant
    URL = API_BASE + PARENT + "/dataTables/" + table + "/dataTableRows"

    # Create a dict of the values that we'll insert
    data_dict = data.split(",")

    # Attempt to load the data
    credentials = service_account.Credentials.from_service_account_info(
        sa_json, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    hd = {
      "Authorization": "Bearer " + credentials.token,
      "Content-Type": "application/json"
    }
    payload = {
        "values": data_dict
    }

    req = requests.post(URL, headers=hd, timeout=30, json=payload)

    # If we get a create time, the row was added succesfully
    if 'createTime' in req.text:
        r_js = json.loads(req.text)
        id_split = r_js['name'].split("/")
        row_id = id_split[9]

        status = EXECUTION_STATE_COMPLETED
        output_message = "Successfully added row. ID: " + row_id
        result_value = True
        siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
        siemplify.end(output_message, result_value, status)
    else:
        output_message = req.text
        status = EXECUTION_STATE_FAILED
        siemplify.LOGGER.error(output_message)
        result_value = False
        siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))

if __name__ == "__main__":
    main()
