# VectorStoreArgs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analyzer** | [**ElasticsearchAnalyzer**](ElasticsearchAnalyzer.md) |  | [optional] 

## Example

```python
from talos_aclient.models.vector_store_args import VectorStoreArgs

# TODO update the JSON string below
json = "{}"
# create an instance of VectorStoreArgs from a JSON string
vector_store_args_instance = VectorStoreArgs.from_json(json)
# print the JSON string representation of the object
print(VectorStoreArgs.to_json())

# convert the object into a dict
vector_store_args_dict = vector_store_args_instance.to_dict()
# create an instance of VectorStoreArgs from a dict
vector_store_args_from_dict = VectorStoreArgs.from_dict(vector_store_args_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


