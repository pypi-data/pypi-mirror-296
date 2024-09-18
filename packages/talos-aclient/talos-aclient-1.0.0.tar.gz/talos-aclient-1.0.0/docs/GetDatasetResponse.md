# GetDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**Dataset**](Dataset.md) |  | 

## Example

```python
from talos_aclient.models.get_dataset_response import GetDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDatasetResponse from a JSON string
get_dataset_response_instance = GetDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(GetDatasetResponse.to_json())

# convert the object into a dict
get_dataset_response_dict = get_dataset_response_instance.to_dict()
# create an instance of GetDatasetResponse from a dict
get_dataset_response_from_dict = GetDatasetResponse.from_dict(get_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


