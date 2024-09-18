# ResourceDataFile


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**storage_type** | [**StorageType**](StorageType.md) |  | 
**storage_url** | **str** |  | 

## Example

```python
from talos_aclient.models.resource_data_file import ResourceDataFile

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceDataFile from a JSON string
resource_data_file_instance = ResourceDataFile.from_json(json)
# print the JSON string representation of the object
print(ResourceDataFile.to_json())

# convert the object into a dict
resource_data_file_dict = resource_data_file_instance.to_dict()
# create an instance of ResourceDataFile from a dict
resource_data_file_from_dict = ResourceDataFile.from_dict(resource_data_file_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


