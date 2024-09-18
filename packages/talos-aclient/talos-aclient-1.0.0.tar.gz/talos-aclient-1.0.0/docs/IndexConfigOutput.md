# IndexConfigOutput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**embedding_model** | [**EmbeddingModel**](EmbeddingModel.md) |  | [optional] 
**vector_store** | [**VectorStoreType**](VectorStoreType.md) |  | [optional] 
**vector_store_args** | [**VectorStoreArgs**](VectorStoreArgs.md) |  | [optional] 
**relational_db** | [**RelationalDBConfigOutput**](RelationalDBConfigOutput.md) |  | [optional] 

## Example

```python
from talos_aclient.models.index_config_output import IndexConfigOutput

# TODO update the JSON string below
json = "{}"
# create an instance of IndexConfigOutput from a JSON string
index_config_output_instance = IndexConfigOutput.from_json(json)
# print the JSON string representation of the object
print(IndexConfigOutput.to_json())

# convert the object into a dict
index_config_output_dict = index_config_output_instance.to_dict()
# create an instance of IndexConfigOutput from a dict
index_config_output_from_dict = IndexConfigOutput.from_dict(index_config_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


