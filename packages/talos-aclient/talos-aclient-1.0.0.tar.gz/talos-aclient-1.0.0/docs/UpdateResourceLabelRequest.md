# UpdateResourceLabelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** |  | 
**resource_id** | **str** |  | 
**labels** | **object** |  | 

## Example

```python
from talos_aclient.models.update_resource_label_request import UpdateResourceLabelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateResourceLabelRequest from a JSON string
update_resource_label_request_instance = UpdateResourceLabelRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateResourceLabelRequest.to_json())

# convert the object into a dict
update_resource_label_request_dict = update_resource_label_request_instance.to_dict()
# create an instance of UpdateResourceLabelRequest from a dict
update_resource_label_request_from_dict = UpdateResourceLabelRequest.from_dict(update_resource_label_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


