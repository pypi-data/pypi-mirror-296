# TableRow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**values** | **List[str]** |  | 

## Example

```python
from talos_aclient.models.table_row import TableRow

# TODO update the JSON string below
json = "{}"
# create an instance of TableRow from a JSON string
table_row_instance = TableRow.from_json(json)
# print the JSON string representation of the object
print(TableRow.to_json())

# convert the object into a dict
table_row_dict = table_row_instance.to_dict()
# create an instance of TableRow from a dict
table_row_from_dict = TableRow.from_dict(table_row_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


