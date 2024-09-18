# CreateDatasetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parse_config** | [**ParseConfig**](ParseConfig.md) |  | [optional] 
**index_config** | [**IndexConfigInput**](IndexConfigInput.md) |  | [optional] 

## Example

```python
from talos_aclient.models.create_dataset_request import CreateDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatasetRequest from a JSON string
create_dataset_request_instance = CreateDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDatasetRequest.to_json())

# convert the object into a dict
create_dataset_request_dict = create_dataset_request_instance.to_dict()
# create an instance of CreateDatasetRequest from a dict
create_dataset_request_from_dict = CreateDatasetRequest.from_dict(create_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


