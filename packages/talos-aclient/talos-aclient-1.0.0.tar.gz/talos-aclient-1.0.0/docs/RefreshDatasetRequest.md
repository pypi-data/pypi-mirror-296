# RefreshDatasetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queue** | [**EnumCeleryQueue**](EnumCeleryQueue.md) |  | [optional] 
**dataset_id** | **str** |  | 

## Example

```python
from talos_aclient.models.refresh_dataset_request import RefreshDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshDatasetRequest from a JSON string
refresh_dataset_request_instance = RefreshDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(RefreshDatasetRequest.to_json())

# convert the object into a dict
refresh_dataset_request_dict = refresh_dataset_request_instance.to_dict()
# create an instance of RefreshDatasetRequest from a dict
refresh_dataset_request_from_dict = RefreshDatasetRequest.from_dict(refresh_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


