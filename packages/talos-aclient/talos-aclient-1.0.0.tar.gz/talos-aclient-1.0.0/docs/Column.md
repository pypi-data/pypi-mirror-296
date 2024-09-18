# Column


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**header_idx** | **int** |  | 
**desc** | **str** |  | [optional] [default to '']
**db_column** | **str** |  | 
**data_type** | [**DataType**](DataType.md) |  | 

## Example

```python
from talos_aclient.models.column import Column

# TODO update the JSON string below
json = "{}"
# create an instance of Column from a JSON string
column_instance = Column.from_json(json)
# print the JSON string representation of the object
print(Column.to_json())

# convert the object into a dict
column_dict = column_instance.to_dict()
# create an instance of Column from a dict
column_from_dict = Column.from_dict(column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


