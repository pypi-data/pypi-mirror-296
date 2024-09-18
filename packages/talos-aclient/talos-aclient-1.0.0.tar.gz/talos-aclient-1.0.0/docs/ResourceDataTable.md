# ResourceDataTable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**storage_type** | [**StorageType**](StorageType.md) |  | 
**storage_url** | **str** |  | 
**sheet** | **str** |  | 
**header_row** | **int** |  | 
**value_starting_row** | **int** |  | 

## Example

```python
from talos_aclient.models.resource_data_table import ResourceDataTable

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceDataTable from a JSON string
resource_data_table_instance = ResourceDataTable.from_json(json)
# print the JSON string representation of the object
print(ResourceDataTable.to_json())

# convert the object into a dict
resource_data_table_dict = resource_data_table_instance.to_dict()
# create an instance of ResourceDataTable from a dict
resource_data_table_from_dict = ResourceDataTable.from_dict(resource_data_table_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


