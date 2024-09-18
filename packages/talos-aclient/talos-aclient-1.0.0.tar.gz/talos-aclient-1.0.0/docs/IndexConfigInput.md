# IndexConfigInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**embedding_model** | [**EmbeddingModel**](EmbeddingModel.md) |  | [optional] 
**vector_store** | [**VectorStoreType**](VectorStoreType.md) |  | [optional] 
**vector_store_args** | [**VectorStoreArgs**](VectorStoreArgs.md) |  | [optional] 
**relational_db** | [**RelationalDBConfigInput**](RelationalDBConfigInput.md) |  | [optional] 

## Example

```python
from talos_aclient.models.index_config_input import IndexConfigInput

# TODO update the JSON string below
json = "{}"
# create an instance of IndexConfigInput from a JSON string
index_config_input_instance = IndexConfigInput.from_json(json)
# print the JSON string representation of the object
print(IndexConfigInput.to_json())

# convert the object into a dict
index_config_input_dict = index_config_input_instance.to_dict()
# create an instance of IndexConfigInput from a dict
index_config_input_from_dict = IndexConfigInput.from_dict(index_config_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


