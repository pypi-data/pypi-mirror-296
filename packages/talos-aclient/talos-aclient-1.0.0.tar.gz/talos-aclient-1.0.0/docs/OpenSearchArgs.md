# OpenSearchArgs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analyzer** | [**ElasticsearchAnalyzer**](ElasticsearchAnalyzer.md) |  | [optional] 

## Example

```python
from talos_aclient.models.open_search_args import OpenSearchArgs

# TODO update the JSON string below
json = "{}"
# create an instance of OpenSearchArgs from a JSON string
open_search_args_instance = OpenSearchArgs.from_json(json)
# print the JSON string representation of the object
print(OpenSearchArgs.to_json())

# convert the object into a dict
open_search_args_dict = open_search_args_instance.to_dict()
# create an instance of OpenSearchArgs from a dict
open_search_args_from_dict = OpenSearchArgs.from_dict(open_search_args_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


