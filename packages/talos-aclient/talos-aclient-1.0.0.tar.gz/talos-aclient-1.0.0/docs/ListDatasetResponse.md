# ListDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**List[Dataset]**](Dataset.md) |  | 

## Example

```python
from talos_aclient.models.list_dataset_response import ListDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatasetResponse from a JSON string
list_dataset_response_instance = ListDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(ListDatasetResponse.to_json())

# convert the object into a dict
list_dataset_response_dict = list_dataset_response_instance.to_dict()
# create an instance of ListDatasetResponse from a dict
list_dataset_response_from_dict = ListDatasetResponse.from_dict(list_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


