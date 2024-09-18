# CreateDatasetResponseItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**AnyOf**](AnyOf.md) |  | [optional] 
**id** | **str** |  | 

## Example

```python
from talos_aclient.models.create_dataset_response_item import CreateDatasetResponseItem

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatasetResponseItem from a JSON string
create_dataset_response_item_instance = CreateDatasetResponseItem.from_json(json)
# print the JSON string representation of the object
print(CreateDatasetResponseItem.to_json())

# convert the object into a dict
create_dataset_response_item_dict = create_dataset_response_item_instance.to_dict()
# create an instance of CreateDatasetResponseItem from a dict
create_dataset_response_item_from_dict = CreateDatasetResponseItem.from_dict(create_dataset_response_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


