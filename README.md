# Unofficial Data Tables Integration for Google SecOps/Chronicle SOAR
Unofficial integration for Chronicle SOAR/Google SecOps to integrate with data tables/reference lists v2. These lists enable substantially more rows and multi-columns.

**NOTE**: The native Chronicle integration to SecOps SOAR now support Data Tables. You should migrate to this as this repo will no longer be updated: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/google-chronicle#google-chronicle-actions-get-data-tables

## Service Account Requirement
You'll need to create a service account in your Google SecOps project (sometimes called Bring-your-own-project). You should give it full rights to permssions under `chronicle.dataTable*`. Once created, generate a JSON key for that service account and that's what you'll use for the integration.

## Available Actions
| SOAR Action | Description |
| ------------- | ------------- |
| Get Data Table as JSON | Returns a JSON object with the full data table. Useful for processing in later actions  |
| Find Matching Row(s) | Search a column for any matching rows. Seach operators include: `equals`,`contains`  |
| Add Row to Table | Insert a list (comma-separated) as a row to a table |
| Delete Row from Table | Given a row ID, delete it from the data table |
