# lqlpath

`lqlpath` is a Python package designed to search for paths in JSON files based on either keys or values.
it can be used for log query language like GCP LQL  
## Features

- **Search by Key**: Retrieve a list of field paths in the JSON where a specific key is found.
- **Search by Value**: Retrieve a list of field paths in the JSON where a specific value is found.
--**Search for bq logs by key
#EXAMPLE


from lqlpath import get_byKey,get_byValue
##
print(get_byKey('bq.json','reservation'))
##
print(get_byValue('bq.json',"us-central1"))

output:
['protoPayload.serviceData.jobInsertResponse.resource.jobStatistics.reservation']
['protoPayload.serviceData.jobInsertResponse.resource.jobName.location']


##the below function search the json fieldpath  for bigquery json logs by key
 
#The following bigquery resouese type supported
#BIGQUERY_RESOURCE
#BIGQUERY_PROJECT
#BIGQUERY_DATASET
#BIGQUERY_TABLE

bq_get_byKey("BIGQUERY_TABLE","table_id")

output:
['resource.labels.table_id']


