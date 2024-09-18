# CloneDatasetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**queue** | [**EnumCeleryQueue**](EnumCeleryQueue.md) |  | [optional] 
**src_dataset_id** | **str** |  | 
**dst_dataset_id** | **str** |  | 

## Example

```python
from talos_aclient.models.clone_dataset_request import CloneDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CloneDatasetRequest from a JSON string
clone_dataset_request_instance = CloneDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(CloneDatasetRequest.to_json())

# convert the object into a dict
clone_dataset_request_dict = clone_dataset_request_instance.to_dict()
# create an instance of CloneDatasetRequest from a dict
clone_dataset_request_from_dict = CloneDatasetRequest.from_dict(clone_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


