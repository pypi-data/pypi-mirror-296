# BodyGetResourceV1TalosResourceGetPost


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_id** | **str** |  | 
**dataset_id** | **str** |  | [optional] [default to 'default']
**table_name** | **str** |  | [optional] 

## Example

```python
from talos_aclient.models.body_get_resource_v1_talos_resource_get_post import BodyGetResourceV1TalosResourceGetPost

# TODO update the JSON string below
json = "{}"
# create an instance of BodyGetResourceV1TalosResourceGetPost from a JSON string
body_get_resource_v1_talos_resource_get_post_instance = BodyGetResourceV1TalosResourceGetPost.from_json(json)
# print the JSON string representation of the object
print(BodyGetResourceV1TalosResourceGetPost.to_json())

# convert the object into a dict
body_get_resource_v1_talos_resource_get_post_dict = body_get_resource_v1_talos_resource_get_post_instance.to_dict()
# create an instance of BodyGetResourceV1TalosResourceGetPost from a dict
body_get_resource_v1_talos_resource_get_post_from_dict = BodyGetResourceV1TalosResourceGetPost.from_dict(body_get_resource_v1_talos_resource_get_post_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


