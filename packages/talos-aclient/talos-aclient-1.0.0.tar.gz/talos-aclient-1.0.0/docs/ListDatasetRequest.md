# ListDatasetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_ids** | **List[str]** |  | 

## Example

```python
from talos_aclient.models.list_dataset_request import ListDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatasetRequest from a JSON string
list_dataset_request_instance = ListDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(ListDatasetRequest.to_json())

# convert the object into a dict
list_dataset_request_dict = list_dataset_request_instance.to_dict()
# create an instance of ListDatasetRequest from a dict
list_dataset_request_from_dict = ListDatasetRequest.from_dict(list_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


