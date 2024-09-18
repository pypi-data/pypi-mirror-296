# ListDatasetResourcesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** |  | 
**resource_ids** | **List[str]** |  | [optional] 
**keyword** | **str** |  | [optional] 
**status** | **int** |  | [optional] 

## Example

```python
from talos_aclient.models.list_dataset_resources_request import ListDatasetResourcesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatasetResourcesRequest from a JSON string
list_dataset_resources_request_instance = ListDatasetResourcesRequest.from_json(json)
# print the JSON string representation of the object
print(ListDatasetResourcesRequest.to_json())

# convert the object into a dict
list_dataset_resources_request_dict = list_dataset_resources_request_instance.to_dict()
# create an instance of ListDatasetResourcesRequest from a dict
list_dataset_resources_request_from_dict = ListDatasetResourcesRequest.from_dict(list_dataset_resources_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


