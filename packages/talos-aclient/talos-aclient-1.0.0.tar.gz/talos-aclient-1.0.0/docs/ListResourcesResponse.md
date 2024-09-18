# ListResourcesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**List[Resource]**](Resource.md) |  | 

## Example

```python
from talos_aclient.models.list_resources_response import ListResourcesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListResourcesResponse from a JSON string
list_resources_response_instance = ListResourcesResponse.from_json(json)
# print the JSON string representation of the object
print(ListResourcesResponse.to_json())

# convert the object into a dict
list_resources_response_dict = list_resources_response_instance.to_dict()
# create an instance of ListResourcesResponse from a dict
list_resources_response_from_dict = ListResourcesResponse.from_dict(list_resources_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


