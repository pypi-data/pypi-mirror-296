# Data


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database** | **str** |  | 
**passwd** | **str** |  | 
**host** | **str** |  | 
**username** | **str** |  | 
**port** | **str** |  | [optional] [default to '3306']
**url** | **str** |  | 
**storage_type** | [**StorageType**](StorageType.md) |  | 
**storage_url** | **str** |  | 
**sheet** | **str** |  | 
**header_row** | **int** |  | 
**value_starting_row** | **int** |  | 

## Example

```python
from talos_aclient.models.data import Data

# TODO update the JSON string below
json = "{}"
# create an instance of Data from a JSON string
data_instance = Data.from_json(json)
# print the JSON string representation of the object
print(Data.to_json())

# convert the object into a dict
data_dict = data_instance.to_dict()
# create an instance of Data from a dict
data_from_dict = Data.from_dict(data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


