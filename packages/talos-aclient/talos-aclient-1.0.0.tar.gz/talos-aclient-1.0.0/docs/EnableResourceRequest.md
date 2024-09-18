# EnableResourceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** |  | 
**resource_id** | **str** |  | 
**enabled** | **bool** |  | 

## Example

```python
from talos_aclient.models.enable_resource_request import EnableResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EnableResourceRequest from a JSON string
enable_resource_request_instance = EnableResourceRequest.from_json(json)
# print the JSON string representation of the object
print(EnableResourceRequest.to_json())

# convert the object into a dict
enable_resource_request_dict = enable_resource_request_instance.to_dict()
# create an instance of EnableResourceRequest from a dict
enable_resource_request_from_dict = EnableResourceRequest.from_dict(enable_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


