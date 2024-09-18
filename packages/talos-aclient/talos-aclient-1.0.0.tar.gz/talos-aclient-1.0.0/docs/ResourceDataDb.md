# ResourceDataDb


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database** | **str** |  | 
**passwd** | **str** |  | 
**host** | **str** |  | 
**username** | **str** |  | 
**port** | **str** |  | [optional] [default to '3306']

## Example

```python
from talos_aclient.models.resource_data_db import ResourceDataDb

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceDataDb from a JSON string
resource_data_db_instance = ResourceDataDb.from_json(json)
# print the JSON string representation of the object
print(ResourceDataDb.to_json())

# convert the object into a dict
resource_data_db_dict = resource_data_db_instance.to_dict()
# create an instance of ResourceDataDb from a dict
resource_data_db_from_dict = ResourceDataDb.from_dict(resource_data_db_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


