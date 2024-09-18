# ParseConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loader_method** | [**ParseMethod**](ParseMethod.md) |  | [optional] 
**chunk_size** | **int** |  | [optional] [default to 256]
**chunk_overlap** | **int** |  | [optional] [default to 0]
**embedding_model** | [**EmbeddingModel**](EmbeddingModel.md) |  | [optional] 
**steps** | [**List[TaskStep]**](TaskStep.md) |  | [optional] [default to [FileLoader, FileTransformer, FileIndexer]]
**transform_steps** | [**List[TransformStep]**](TransformStep.md) |  | [optional] [default to [clean, splitter]]

## Example

```python
from talos_aclient.models.parse_config import ParseConfig

# TODO update the JSON string below
json = "{}"
# create an instance of ParseConfig from a JSON string
parse_config_instance = ParseConfig.from_json(json)
# print the JSON string representation of the object
print(ParseConfig.to_json())

# convert the object into a dict
parse_config_dict = parse_config_instance.to_dict()
# create an instance of ParseConfig from a dict
parse_config_from_dict = ParseConfig.from_dict(parse_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


