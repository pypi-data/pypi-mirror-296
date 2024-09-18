# RelationalDBConfigOutput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**table_name** | **str** |  | 
**table_desc** | **str** |  | 
**columns** | [**List[Column]**](Column.md) |  | 

## Example

```python
from talos_aclient.models.relational_db_config_output import RelationalDBConfigOutput

# TODO update the JSON string below
json = "{}"
# create an instance of RelationalDBConfigOutput from a JSON string
relational_db_config_output_instance = RelationalDBConfigOutput.from_json(json)
# print the JSON string representation of the object
print(RelationalDBConfigOutput.to_json())

# convert the object into a dict
relational_db_config_output_dict = relational_db_config_output_instance.to_dict()
# create an instance of RelationalDBConfigOutput from a dict
relational_db_config_output_from_dict = RelationalDBConfigOutput.from_dict(relational_db_config_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


