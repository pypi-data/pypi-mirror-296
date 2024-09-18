# ResourceContent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | **object** |  | 
**page_content** | **str** |  | 

## Example

```python
from talos_aclient.models.resource_content import ResourceContent

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceContent from a JSON string
resource_content_instance = ResourceContent.from_json(json)
# print the JSON string representation of the object
print(ResourceContent.to_json())

# convert the object into a dict
resource_content_dict = resource_content_instance.to_dict()
# create an instance of ResourceContent from a dict
resource_content_from_dict = ResourceContent.from_dict(resource_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


