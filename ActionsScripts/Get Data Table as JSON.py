from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import TableManager
import google.auth.transport.requests
from google.oauth2 import service_account
import json
import requests

COLUMNS = []
JSON_RESULT = []

siemplify = SiemplifyAction()
table = siemplify.extract_action_param("Data Table Name", print_value=True)
sa_json = siemplify.extract_configuration_param('Integration',"Service Account JSON")
sa_json = json.loads(sa_json)
project_name = siemplify.extract_configuration_param('Integration',"GCP Project ID")
region = siemplify.extract_configuration_param('Integration',"GCP Region")
tenant = siemplify.extract_configuration_param('Integration',"Google SecOps Tenant ID")


@output_handler
def main():
    c = TableManager.secops.get_datatable_json(sa_json,
                                                project_name,
                                                region,
                                                tenant,
                                                table,
                                                siemplify)

    # Check if we got a valid response
    if 'error' in c:
        output_message = f"Unable to retrieve data table. Is the name correct?"
        status = EXECUTION_STATE_FAILED
        siemplify.LOGGER.error(output_message)
        result_value = False
        siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
        siemplify.end(output_message, result_value, status)
    else:
        siemplify.LOGGER.info('ok')
        siemplify.result.add_result_json(c)
        status = EXECUTION_STATE_COMPLETED
        output_message = "JSON results returned"
        result_value = True
        siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
        siemplify.end(output_message, result_value, status)

if __name__ == "__main__":
    main()
