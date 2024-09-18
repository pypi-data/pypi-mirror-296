# DeleteResourceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ids** | **List[str]** |  | 

## Example

```python
from talos_aclient.models.delete_resource_request import DeleteResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteResourceRequest from a JSON string
delete_resource_request_instance = DeleteResourceRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteResourceRequest.to_json())

# convert the object into a dict
delete_resource_request_dict = delete_resource_request_instance.to_dict()
# create an instance of DeleteResourceRequest from a dict
delete_resource_request_from_dict = DeleteResourceRequest.from_dict(delete_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


