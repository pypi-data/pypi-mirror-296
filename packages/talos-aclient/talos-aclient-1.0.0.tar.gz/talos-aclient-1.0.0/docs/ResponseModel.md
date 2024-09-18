# ResponseModel

统一返回模型  E.g. ::      @router.get('/test', response_model=ResponseModel)     def test():         return ResponseModel(data={'test': 'test'})       @router.get('/test')     def test() -> ResponseModel:         return ResponseModel(data={'test': 'test'})       @router.get('/test')     def test() -> ResponseModel:         res = CustomResponseCode.HTTP_200         return ResponseModel(code=res.code, detail=res.detail, data={'test': 'test'})

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] [default to 200]
**detail** | **str** |  | [optional] [default to '请求成功']
**data** | [**AnyOf**](AnyOf.md) |  | [optional] 

## Example

```python
from talos_aclient.models.response_model import ResponseModel

# TODO update the JSON string below
json = "{}"
# create an instance of ResponseModel from a JSON string
response_model_instance = ResponseModel.from_json(json)
# print the JSON string representation of the object
print(ResponseModel.to_json())

# convert the object into a dict
response_model_dict = response_model_instance.to_dict()
# create an instance of ResponseModel from a dict
response_model_from_dict = ResponseModel.from_dict(response_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


