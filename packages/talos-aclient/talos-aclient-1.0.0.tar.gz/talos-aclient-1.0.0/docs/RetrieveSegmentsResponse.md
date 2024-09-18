# RetrieveSegmentsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**List[RetrieveSegment]**](RetrieveSegment.md) |  | 

## Example

```python
from talos_aclient.models.retrieve_segments_response import RetrieveSegmentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RetrieveSegmentsResponse from a JSON string
retrieve_segments_response_instance = RetrieveSegmentsResponse.from_json(json)
# print the JSON string representation of the object
print(RetrieveSegmentsResponse.to_json())

# convert the object into a dict
retrieve_segments_response_dict = retrieve_segments_response_instance.to_dict()
# create an instance of RetrieveSegmentsResponse from a dict
retrieve_segments_response_from_dict = RetrieveSegmentsResponse.from_dict(retrieve_segments_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


