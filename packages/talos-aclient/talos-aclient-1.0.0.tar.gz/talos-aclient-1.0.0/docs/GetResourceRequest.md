# GetResourceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** |  | 
**dataset_id** | **str** |  | [optional] [default to 'default']
**table_name** | **str** |  | [optional] 

## Example

```python
from talos_aclient.models.get_resource_request import GetResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetResourceRequest from a JSON string
get_resource_request_instance = GetResourceRequest.from_json(json)
# print the JSON string representation of the object
print(GetResourceRequest.to_json())

# convert the object into a dict
get_resource_request_dict = get_resource_request_instance.to_dict()
# create an instance of GetResourceRequest from a dict
get_resource_request_from_dict = GetResourceRequest.from_dict(get_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


