# CreateDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**CreateDatasetResponseItem**](CreateDatasetResponseItem.md) |  | 

## Example

```python
from talos_aclient.models.create_dataset_response import CreateDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatasetResponse from a JSON string
create_dataset_response_instance = CreateDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(CreateDatasetResponse.to_json())

# convert the object into a dict
create_dataset_response_dict = create_dataset_response_instance.to_dict()
# create an instance of CreateDatasetResponse from a dict
create_dataset_response_from_dict = CreateDatasetResponse.from_dict(create_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


