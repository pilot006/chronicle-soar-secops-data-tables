from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import requests
import google.auth.transport.requests
from google.oauth2 import service_account
import json


@output_handler
def main():
    siemplify = SiemplifyAction()

    sa_json = siemplify.extract_configuration_param('Integration',"Service Account JSON")
    sa_json = json.loads(sa_json)
    project_name = siemplify.extract_configuration_param('Integration',"GCP Project ID")
    region = siemplify.extract_configuration_param('Integration',"GCP Region")
    tenant = siemplify.extract_configuration_param('Integration',"Google SecOps Tenant ID")

    # Get auth token
    credentials = service_account.Credentials.from_service_account_info(
        sa_json, scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    # Create URL using region & project config
    # https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini#http_request
    endpoint = 'https://' + region + "-chronicle.googleapis.com"
    endpoint = endpoint + '/v1alpha/projects/' 
    endpoint = endpoint + project_name + "/locations/" + region
    endpoint = endpoint + '/instances/' + tenant
    endpoint = endpoint + '/dataTables/secops_integration_test'
    siemplify.LOGGER.info("endpoint: " + endpoint)

    hd = {
        "Authorization": "Bearer " + credentials.token,
        "Content-Type": "application/json"
    }
    req = requests.get(endpoint, headers=hd)
    if 'Data Table Name' in req.text:
        status = EXECUTION_STATE_COMPLETED  # used to flag back to siemplify system, the action final status
        output_message = "output message :"  # human readable message, showed in UI as the action result
        result_value = True  # Set a simple result value, used for playbook if\else and placeholders.
    else:
        output_message = f"Unable to connect to SecOps Data Tables API"
        status = EXECUTION_STATE_FAILED
        siemplify.LOGGER.error(output_message)
        #siemplify.LOGGER.exception(e)
        result_value = False

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
    siemplify.end(output_message, result_value, status)

if __name__ == "__main__":
    main()
