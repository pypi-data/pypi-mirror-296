# CreateResourceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**ResourceType**](ResourceType.md) |  | 
**dry_run** | **bool** |  | [optional] [default to False]
**name** | **str** |  | 
**data** | [**Data**](Data.md) |  | 
**async_mode** | **bool** |  | [optional] [default to True]
**queue** | [**EnumCeleryQueue**](EnumCeleryQueue.md) |  | [optional] 

## Example

```python
from talos_aclient.models.create_resource_request import CreateResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateResourceRequest from a JSON string
create_resource_request_instance = CreateResourceRequest.from_json(json)
# print the JSON string representation of the object
print(CreateResourceRequest.to_json())

# convert the object into a dict
create_resource_request_dict = create_resource_request_instance.to_dict()
# create an instance of CreateResourceRequest from a dict
create_resource_request_from_dict = CreateResourceRequest.from_dict(create_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


