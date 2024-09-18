# talos_aclient.ResourceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_resource**](ResourceApi.md#create_resource) | **POST** /v1/talos/resource/create | Create Resource
[**delete_resource**](ResourceApi.md#delete_resource) | **POST** /v1/talos/resource/delete | Delete Resource
[**get_resource**](ResourceApi.md#get_resource) | **POST** /v1/talos/resource/get | Get Resource
[**get_resource_image**](ResourceApi.md#get_resource_image) | **POST** /v1/talos/resource/get_image | Get Resource Image
[**list_resource**](ResourceApi.md#list_resource) | **POST** /v1/talos/resource/list | List Resource


# **create_resource**
> CreateResourceResponse create_resource(create_resource_request)

Create Resource

### Example


```python
import talos_aclient
from talos_aclient.models.create_resource_request import CreateResourceRequest
from talos_aclient.models.create_resource_response import CreateResourceResponse
from talos_aclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = talos_aclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with talos_aclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = talos_aclient.ResourceApi(api_client)
    create_resource_request = talos_aclient.CreateResourceRequest() # CreateResourceRequest | 

    try:
        # Create Resource
        api_response = await api_instance.create_resource(create_resource_request)
        print("The response of ResourceApi->create_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResourceApi->create_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_resource_request** | [**CreateResourceRequest**](CreateResourceRequest.md)|  | 

### Return type

[**CreateResourceResponse**](CreateResourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_resource**
> ResponseModel delete_resource(delete_resource_request)

Delete Resource

### Example


```python
import talos_aclient
from talos_aclient.models.delete_resource_request import DeleteResourceRequest
from talos_aclient.models.response_model import ResponseModel
from talos_aclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = talos_aclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with talos_aclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = talos_aclient.ResourceApi(api_client)
    delete_resource_request = talos_aclient.DeleteResourceRequest() # DeleteResourceRequest | 

    try:
        # Delete Resource
        api_response = await api_instance.delete_resource(delete_resource_request)
        print("The response of ResourceApi->delete_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResourceApi->delete_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_resource_request** | [**DeleteResourceRequest**](DeleteResourceRequest.md)|  | 

### Return type

[**ResponseModel**](ResponseModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource**
> GetResourceResponse get_resource(get_resource_request, page=page, page_size=page_size)

Get Resource

### Example


```python
import talos_aclient
from talos_aclient.models.get_resource_request import GetResourceRequest
from talos_aclient.models.get_resource_response import GetResourceResponse
from talos_aclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = talos_aclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with talos_aclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = talos_aclient.ResourceApi(api_client)
    get_resource_request = talos_aclient.GetResourceRequest() # GetResourceRequest | 
    page = 1 # int |  (optional) (default to 1)
    page_size = 10 # int |  (optional) (default to 10)

    try:
        # Get Resource
        api_response = await api_instance.get_resource(get_resource_request, page=page, page_size=page_size)
        print("The response of ResourceApi->get_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResourceApi->get_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **get_resource_request** | [**GetResourceRequest**](GetResourceRequest.md)|  | 
 **page** | **int**|  | [optional] [default to 1]
 **page_size** | **int**|  | [optional] [default to 10]

### Return type

[**GetResourceResponse**](GetResourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource_image**
> GetResourceImageResponse get_resource_image(get_resource_image_request)

Get Resource Image

### Example


```python
import talos_aclient
from talos_aclient.models.get_resource_image_request import GetResourceImageRequest
from talos_aclient.models.get_resource_image_response import GetResourceImageResponse
from talos_aclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = talos_aclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with talos_aclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = talos_aclient.ResourceApi(api_client)
    get_resource_image_request = talos_aclient.GetResourceImageRequest() # GetResourceImageRequest | 

    try:
        # Get Resource Image
        api_response = await api_instance.get_resource_image(get_resource_image_request)
        print("The response of ResourceApi->get_resource_image:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResourceApi->get_resource_image: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **get_resource_image_request** | [**GetResourceImageRequest**](GetResourceImageRequest.md)|  | 

### Return type

[**GetResourceImageResponse**](GetResourceImageResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_resource**
> ListResourcesResponse list_resource(list_resources_request, page=page, page_size=page_size)

List Resource

### Example


```python
import talos_aclient
from talos_aclient.models.list_resources_request import ListResourcesRequest
from talos_aclient.models.list_resources_response import ListResourcesResponse
from talos_aclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = talos_aclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with talos_aclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = talos_aclient.ResourceApi(api_client)
    list_resources_request = talos_aclient.ListResourcesRequest() # ListResourcesRequest | 
    page = 1 # int |  (optional) (default to 1)
    page_size = 10 # int |  (optional) (default to 10)

    try:
        # List Resource
        api_response = await api_instance.list_resource(list_resources_request, page=page, page_size=page_size)
        print("The response of ResourceApi->list_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResourceApi->list_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_resources_request** | [**ListResourcesRequest**](ListResourcesRequest.md)|  | 
 **page** | **int**|  | [optional] [default to 1]
 **page_size** | **int**|  | [optional] [default to 10]

### Return type

[**ListResourcesResponse**](ListResourcesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

