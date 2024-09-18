# DeleteSegmentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**segment_id** | **str** |  | 
**dataset_id** | **str** |  | [optional] [default to 'default']

## Example

```python
from talos_aclient.models.delete_segment_request import DeleteSegmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteSegmentRequest from a JSON string
delete_segment_request_instance = DeleteSegmentRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteSegmentRequest.to_json())

# convert the object into a dict
delete_segment_request_dict = delete_segment_request_instance.to_dict()
# create an instance of DeleteSegmentRequest from a dict
delete_segment_request_from_dict = DeleteSegmentRequest.from_dict(delete_segment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


