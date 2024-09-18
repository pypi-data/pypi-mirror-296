# RelationalDBConfigInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**table_name** | **str** |  | 
**table_desc** | **str** |  | 
**columns** | [**List[Column]**](Column.md) |  | 

## Example

```python
from talos_aclient.models.relational_db_config_input import RelationalDBConfigInput

# TODO update the JSON string below
json = "{}"
# create an instance of RelationalDBConfigInput from a JSON string
relational_db_config_input_instance = RelationalDBConfigInput.from_json(json)
# print the JSON string representation of the object
print(RelationalDBConfigInput.to_json())

# convert the object into a dict
relational_db_config_input_dict = relational_db_config_input_instance.to_dict()
# create an instance of RelationalDBConfigInput from a dict
relational_db_config_input_from_dict = RelationalDBConfigInput.from_dict(relational_db_config_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


