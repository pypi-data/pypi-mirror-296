# ListSegmentsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** |  | 
**dataset_id** | **str** |  | [optional] [default to 'default']

## Example

```python
from talos_aclient.models.list_segments_request import ListSegmentsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListSegmentsRequest from a JSON string
list_segments_request_instance = ListSegmentsRequest.from_json(json)
# print the JSON string representation of the object
print(ListSegmentsRequest.to_json())

# convert the object into a dict
list_segments_request_dict = list_segments_request_instance.to_dict()
# create an instance of ListSegmentsRequest from a dict
list_segments_request_from_dict = ListSegmentsRequest.from_dict(list_segments_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


