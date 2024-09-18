# RetrieveSegment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page_content** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 

## Example

```python
from talos_aclient.models.retrieve_segment import RetrieveSegment

# TODO update the JSON string below
json = "{}"
# create an instance of RetrieveSegment from a JSON string
retrieve_segment_instance = RetrieveSegment.from_json(json)
# print the JSON string representation of the object
print(RetrieveSegment.to_json())

# convert the object into a dict
retrieve_segment_dict = retrieve_segment_instance.to_dict()
# create an instance of RetrieveSegment from a dict
retrieve_segment_from_dict = RetrieveSegment.from_dict(retrieve_segment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


