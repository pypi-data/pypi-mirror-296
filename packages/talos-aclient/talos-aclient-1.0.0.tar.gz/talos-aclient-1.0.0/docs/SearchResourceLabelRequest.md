# SearchResourceLabelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_ids** | **List[str]** |  | 
**keyword** | **str** |  | 

## Example

```python
from talos_aclient.models.search_resource_label_request import SearchResourceLabelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResourceLabelRequest from a JSON string
search_resource_label_request_instance = SearchResourceLabelRequest.from_json(json)
# print the JSON string representation of the object
print(SearchResourceLabelRequest.to_json())

# convert the object into a dict
search_resource_label_request_dict = search_resource_label_request_instance.to_dict()
# create an instance of SearchResourceLabelRequest from a dict
search_resource_label_request_from_dict = SearchResourceLabelRequest.from_dict(search_resource_label_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


