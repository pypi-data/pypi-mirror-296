# ListResourcesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_ids** | **List[str]** |  | 
**dataset_id** | **str** |  | [optional] [default to 'default']
**page** | **int** |  | [optional] [default to 1]
**size** | **int** |  | [optional] [default to 10]
**table_name** | **str** |  | [optional] 

## Example

```python
from talos_aclient.models.list_resources_request import ListResourcesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListResourcesRequest from a JSON string
list_resources_request_instance = ListResourcesRequest.from_json(json)
# print the JSON string representation of the object
print(ListResourcesRequest.to_json())

# convert the object into a dict
list_resources_request_dict = list_resources_request_instance.to_dict()
# create an instance of ListResourcesRequest from a dict
list_resources_request_from_dict = ListResourcesRequest.from_dict(list_resources_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


