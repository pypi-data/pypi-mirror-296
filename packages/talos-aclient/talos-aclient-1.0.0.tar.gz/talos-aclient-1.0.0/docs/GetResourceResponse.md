# GetResourceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**Resource**](Resource.md) |  | 

## Example

```python
from talos_aclient.models.get_resource_response import GetResourceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetResourceResponse from a JSON string
get_resource_response_instance = GetResourceResponse.from_json(json)
# print the JSON string representation of the object
print(GetResourceResponse.to_json())

# convert the object into a dict
get_resource_response_dict = get_resource_response_instance.to_dict()
# create an instance of GetResourceResponse from a dict
get_resource_response_from_dict = GetResourceResponse.from_dict(get_resource_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


