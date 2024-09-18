# Resource


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**size** | **int** |  | [optional] [default to 0]
**metadata** | **object** |  | [optional] 
**page_contents** | [**List[ResourceContent]**](ResourceContent.md) |  | [optional] 
**progress** | **int** |  | [optional] 
**status** | **int** |  | [optional] 
**total** | **int** |  | [optional] [default to 0]
**storage_url** | **str** |  | [optional] 
**extension** | **str** |  | [optional] [default to '']
**document_meta** | **object** |  | [optional] 
**error_message** | **str** |  | [optional] [default to '']
**segment_count** | **int** |  | [optional] [default to 0]

## Example

```python
from talos_aclient.models.resource import Resource

# TODO update the JSON string below
json = "{}"
# create an instance of Resource from a JSON string
resource_instance = Resource.from_json(json)
# print the JSON string representation of the object
print(Resource.to_json())

# convert the object into a dict
resource_dict = resource_instance.to_dict()
# create an instance of Resource from a dict
resource_from_dict = Resource.from_dict(resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


