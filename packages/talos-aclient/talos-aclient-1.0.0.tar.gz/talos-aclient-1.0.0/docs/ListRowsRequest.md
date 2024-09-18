# ListRowsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** |  | 

## Example

```python
from talos_aclient.models.list_rows_request import ListRowsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListRowsRequest from a JSON string
list_rows_request_instance = ListRowsRequest.from_json(json)
# print the JSON string representation of the object
print(ListRowsRequest.to_json())

# convert the object into a dict
list_rows_request_dict = list_rows_request_instance.to_dict()
# create an instance of ListRowsRequest from a dict
list_rows_request_from_dict = ListRowsRequest.from_dict(list_rows_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


