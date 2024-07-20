# Unofficial Data Tables Integration for Google SecOps/Chronicle SOAR
Unofficial integration for Chronicle SOAR/Google SecOps to integrate with data tables/reference lists v2. These lists enable substantially more rows and mutli-columns.


## Available Actions
| SOAR Action | Description |
| ------------- | ------------- |
| Get Data Table as JSON | Returns a JSON object with the full data table. Useful for processing in later actions  |
| Find Matching Row(s) | Search a column for any matching rows. Seach operators include: `equals`,`contains`  |
| Add Row to Table | Insert a list (comma-separated) as a row to a table |
| Delete Row from Table | Given a row ID, delete it from the data table |
