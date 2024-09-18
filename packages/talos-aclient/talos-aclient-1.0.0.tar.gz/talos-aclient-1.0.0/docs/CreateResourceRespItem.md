# CreateResourceRespItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**size** | **int** |  | [optional] [default to 0]
**dry_run** | **bool** |  | [optional] [default to False]

## Example

```python
from talos_aclient.models.create_resource_resp_item import CreateResourceRespItem

# TODO update the JSON string below
json = "{}"
# create an instance of CreateResourceRespItem from a JSON string
create_resource_resp_item_instance = CreateResourceRespItem.from_json(json)
# print the JSON string representation of the object
print(CreateResourceRespItem.to_json())

# convert the object into a dict
create_resource_resp_item_dict = create_resource_resp_item_instance.to_dict()
# create an instance of CreateResourceRespItem from a dict
create_resource_resp_item_from_dict = CreateResourceRespItem.from_dict(create_resource_resp_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


