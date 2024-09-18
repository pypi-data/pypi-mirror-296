# RetrieveSegmentsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** |  | 
**dataset_id** | **str** |  | [optional] [default to 'default']
**search_type** | [**RetrieveSearchType**](RetrieveSearchType.md) |  | [optional] 
**limit** | **int** |  | [optional] [default to 10]
**resource_id** | **str** |  | [optional] [default to '']

## Example

```python
from talos_aclient.models.retrieve_segments_request import RetrieveSegmentsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RetrieveSegmentsRequest from a JSON string
retrieve_segments_request_instance = RetrieveSegmentsRequest.from_json(json)
# print the JSON string representation of the object
print(RetrieveSegmentsRequest.to_json())

# convert the object into a dict
retrieve_segments_request_dict = retrieve_segments_request_instance.to_dict()
# create an instance of RetrieveSegmentsRequest from a dict
retrieve_segments_request_from_dict = RetrieveSegmentsRequest.from_dict(retrieve_segments_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


