# GetResourceImageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** |  | 
**image_id** | **str** |  | 

## Example

```python
from talos_aclient.models.get_resource_image_request import GetResourceImageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetResourceImageRequest from a JSON string
get_resource_image_request_instance = GetResourceImageRequest.from_json(json)
# print the JSON string representation of the object
print(GetResourceImageRequest.to_json())

# convert the object into a dict
get_resource_image_request_dict = get_resource_image_request_instance.to_dict()
# create an instance of GetResourceImageRequest from a dict
get_resource_image_request_from_dict = GetResourceImageRequest.from_dict(get_resource_image_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


