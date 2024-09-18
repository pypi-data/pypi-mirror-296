# DeleteDatasetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queue** | [**EnumCeleryQueue**](EnumCeleryQueue.md) |  | [optional] 
**dataset_id** | **str** |  | 

## Example

```python
from talos_aclient.models.delete_dataset_request import DeleteDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteDatasetRequest from a JSON string
delete_dataset_request_instance = DeleteDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteDatasetRequest.to_json())

# convert the object into a dict
delete_dataset_request_dict = delete_dataset_request_instance.to_dict()
# create an instance of DeleteDatasetRequest from a dict
delete_dataset_request_from_dict = DeleteDatasetRequest.from_dict(delete_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


