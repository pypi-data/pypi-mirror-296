# AddResourceToDatasetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**ResourceType**](ResourceType.md) |  | 
**dry_run** | **bool** |  | [optional] [default to False]
**name** | **str** |  | 
**data** | [**Data**](Data.md) |  | 
**async_mode** | **bool** |  | [optional] [default to True]
**queue** | [**EnumCeleryQueue**](EnumCeleryQueue.md) |  | [optional] 
**dataset_id** | **str** |  | 

## Example

```python
from talos_aclient.models.add_resource_to_dataset_request import AddResourceToDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddResourceToDatasetRequest from a JSON string
add_resource_to_dataset_request_instance = AddResourceToDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(AddResourceToDatasetRequest.to_json())

# convert the object into a dict
add_resource_to_dataset_request_dict = add_resource_to_dataset_request_instance.to_dict()
# create an instance of AddResourceToDatasetRequest from a dict
add_resource_to_dataset_request_from_dict = AddResourceToDatasetRequest.from_dict(add_resource_to_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


