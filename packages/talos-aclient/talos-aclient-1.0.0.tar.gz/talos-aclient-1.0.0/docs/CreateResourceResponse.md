# CreateResourceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**CreateResourceRespItem**](CreateResourceRespItem.md) |  | 

## Example

```python
from talos_aclient.models.create_resource_response import CreateResourceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateResourceResponse from a JSON string
create_resource_response_instance = CreateResourceResponse.from_json(json)
# print the JSON string representation of the object
print(CreateResourceResponse.to_json())

# convert the object into a dict
create_resource_response_dict = create_resource_response_instance.to_dict()
# create an instance of CreateResourceResponse from a dict
create_resource_response_from_dict = CreateResourceResponse.from_dict(create_resource_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


