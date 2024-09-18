# RefreshDatasetResourceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queue** | [**EnumCeleryQueue**](EnumCeleryQueue.md) |  | [optional] 
**dataset_id** | **str** |  | 
**resource_id** | **str** |  | 

## Example

```python
from talos_aclient.models.refresh_dataset_resource_request import RefreshDatasetResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshDatasetResourceRequest from a JSON string
refresh_dataset_resource_request_instance = RefreshDatasetResourceRequest.from_json(json)
# print the JSON string representation of the object
print(RefreshDatasetResourceRequest.to_json())

# convert the object into a dict
refresh_dataset_resource_request_dict = refresh_dataset_resource_request_instance.to_dict()
# create an instance of RefreshDatasetResourceRequest from a dict
refresh_dataset_resource_request_from_dict = RefreshDatasetResourceRequest.from_dict(refresh_dataset_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


