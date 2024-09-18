# UpdateDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**AnyOf**](AnyOf.md) |  | [optional] 

## Example

```python
from talos_aclient.models.update_dataset_response import UpdateDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateDatasetResponse from a JSON string
update_dataset_response_instance = UpdateDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateDatasetResponse.to_json())

# convert the object into a dict
update_dataset_response_dict = update_dataset_response_instance.to_dict()
# create an instance of UpdateDatasetResponse from a dict
update_dataset_response_from_dict = UpdateDatasetResponse.from_dict(update_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


