# talos_aclient.DatasetApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_resource**](DatasetApi.md#add_resource) | **POST** /v1/talos/dataset/add_resource | Add Resource
[**clone_dataset**](DatasetApi.md#clone_dataset) | **POST** /v1/talos/dataset/clone | Clone Dataset
[**create_dataset**](DatasetApi.md#create_dataset) | **POST** /v1/talos/dataset/create | Create Dataset
[**delete_dataset**](DatasetApi.md#delete_dataset) | **POST** /v1/talos/dataset/delete | Delete Dataset
[**delete_dataset_resource**](DatasetApi.md#delete_dataset_resource) | **POST** /v1/talos/dataset/delete_resource | Delete Dataset Resource
[**enable_dataset_resource**](DatasetApi.md#enable_dataset_resource) | **POST** /v1/talos/dataset/enable_resource | Enable Dataset Resource
[**get_dataset**](DatasetApi.md#get_dataset) | **POST** /v1/talos/dataset/get | Get Dataset
[**list_dataset**](DatasetApi.md#list_dataset) | **POST** /v1/talos/dataset/list | List Dataset
[**list_resources**](DatasetApi.md#list_resources) | **POST** /v1/talos/dataset/list_resources | List Resources
[**list_rows**](DatasetApi.md#list_rows) | **POST** /v1/talos/dataset/list_rows | List Rows
[**refresh_dataset**](DatasetApi.md#refresh_dataset) | **POST** /v1/talos/dataset/refresh | Refresh Dataset
[**refresh_resource**](DatasetApi.md#refresh_resource) | **POST** /v1/talos/dataset/refresh_resource | Refresh Resource
[**update_dataset**](DatasetApi.md#update_dataset) | **POST** /v1/talos/dataset/update | Update Dataset


# **add_resource**
> CreateResourceResponse add_resource(add_resource_to_dataset_request)

Add Resource

### Example


```python
import talos_aclient
from talos_aclient.models.add_resource_to_dataset_request import AddResourceToDatasetRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    add_resource_to_dataset_request = talos_aclient.AddResourceToDatasetRequest() # AddResourceToDatasetRequest | 

    try:
        # Add Resource
        api_response = await api_instance.add_resource(add_resource_to_dataset_request)
        print("The response of DatasetApi->add_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->add_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **add_resource_to_dataset_request** | [**AddResourceToDatasetRequest**](AddResourceToDatasetRequest.md)|  | 

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

# **clone_dataset**
> object clone_dataset(clone_dataset_request)

Clone Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.clone_dataset_request import CloneDatasetRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    clone_dataset_request = talos_aclient.CloneDatasetRequest() # CloneDatasetRequest | 

    try:
        # Clone Dataset
        api_response = await api_instance.clone_dataset(clone_dataset_request)
        print("The response of DatasetApi->clone_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->clone_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **clone_dataset_request** | [**CloneDatasetRequest**](CloneDatasetRequest.md)|  | 

### Return type

**object**

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

# **create_dataset**
> CreateDatasetResponse create_dataset(create_dataset_request)

Create Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.create_dataset_request import CreateDatasetRequest
from talos_aclient.models.create_dataset_response import CreateDatasetResponse
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
    api_instance = talos_aclient.DatasetApi(api_client)
    create_dataset_request = talos_aclient.CreateDatasetRequest() # CreateDatasetRequest | 

    try:
        # Create Dataset
        api_response = await api_instance.create_dataset(create_dataset_request)
        print("The response of DatasetApi->create_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->create_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_dataset_request** | [**CreateDatasetRequest**](CreateDatasetRequest.md)|  | 

### Return type

[**CreateDatasetResponse**](CreateDatasetResponse.md)

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

# **delete_dataset**
> ResponseModel delete_dataset(delete_dataset_request)

Delete Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.delete_dataset_request import DeleteDatasetRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    delete_dataset_request = talos_aclient.DeleteDatasetRequest() # DeleteDatasetRequest | 

    try:
        # Delete Dataset
        api_response = await api_instance.delete_dataset(delete_dataset_request)
        print("The response of DatasetApi->delete_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->delete_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_dataset_request** | [**DeleteDatasetRequest**](DeleteDatasetRequest.md)|  | 

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

# **delete_dataset_resource**
> ResponseModel delete_dataset_resource(delete_dataset_resource_request)

Delete Dataset Resource

### Example


```python
import talos_aclient
from talos_aclient.models.delete_dataset_resource_request import DeleteDatasetResourceRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    delete_dataset_resource_request = talos_aclient.DeleteDatasetResourceRequest() # DeleteDatasetResourceRequest | 

    try:
        # Delete Dataset Resource
        api_response = await api_instance.delete_dataset_resource(delete_dataset_resource_request)
        print("The response of DatasetApi->delete_dataset_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->delete_dataset_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_dataset_resource_request** | [**DeleteDatasetResourceRequest**](DeleteDatasetResourceRequest.md)|  | 

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

# **enable_dataset_resource**
> ResponseModel enable_dataset_resource(enable_resource_request)

Enable Dataset Resource

### Example


```python
import talos_aclient
from talos_aclient.models.enable_resource_request import EnableResourceRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    enable_resource_request = talos_aclient.EnableResourceRequest() # EnableResourceRequest | 

    try:
        # Enable Dataset Resource
        api_response = await api_instance.enable_dataset_resource(enable_resource_request)
        print("The response of DatasetApi->enable_dataset_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->enable_dataset_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **enable_resource_request** | [**EnableResourceRequest**](EnableResourceRequest.md)|  | 

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

# **get_dataset**
> GetDatasetResponse get_dataset(get_dataset_request)

Get Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.get_dataset_request import GetDatasetRequest
from talos_aclient.models.get_dataset_response import GetDatasetResponse
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
    api_instance = talos_aclient.DatasetApi(api_client)
    get_dataset_request = talos_aclient.GetDatasetRequest() # GetDatasetRequest | 

    try:
        # Get Dataset
        api_response = await api_instance.get_dataset(get_dataset_request)
        print("The response of DatasetApi->get_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->get_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **get_dataset_request** | [**GetDatasetRequest**](GetDatasetRequest.md)|  | 

### Return type

[**GetDatasetResponse**](GetDatasetResponse.md)

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

# **list_dataset**
> ListDatasetResponse list_dataset(list_dataset_request)

List Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.list_dataset_request import ListDatasetRequest
from talos_aclient.models.list_dataset_response import ListDatasetResponse
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
    api_instance = talos_aclient.DatasetApi(api_client)
    list_dataset_request = talos_aclient.ListDatasetRequest() # ListDatasetRequest | 

    try:
        # List Dataset
        api_response = await api_instance.list_dataset(list_dataset_request)
        print("The response of DatasetApi->list_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->list_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_dataset_request** | [**ListDatasetRequest**](ListDatasetRequest.md)|  | 

### Return type

[**ListDatasetResponse**](ListDatasetResponse.md)

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

# **list_resources**
> ListDatasetResourcesResponse list_resources(list_dataset_resources_request, page=page, page_size=page_size)

List Resources

### Example


```python
import talos_aclient
from talos_aclient.models.list_dataset_resources_request import ListDatasetResourcesRequest
from talos_aclient.models.list_dataset_resources_response import ListDatasetResourcesResponse
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
    api_instance = talos_aclient.DatasetApi(api_client)
    list_dataset_resources_request = talos_aclient.ListDatasetResourcesRequest() # ListDatasetResourcesRequest | 
    page = 1 # int | Page number (optional) (default to 1)
    page_size = 10 # int | Page size (optional) (default to 10)

    try:
        # List Resources
        api_response = await api_instance.list_resources(list_dataset_resources_request, page=page, page_size=page_size)
        print("The response of DatasetApi->list_resources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->list_resources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_dataset_resources_request** | [**ListDatasetResourcesRequest**](ListDatasetResourcesRequest.md)|  | 
 **page** | **int**| Page number | [optional] [default to 1]
 **page_size** | **int**| Page size | [optional] [default to 10]

### Return type

[**ListDatasetResourcesResponse**](ListDatasetResourcesResponse.md)

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

# **list_rows**
> ListRowsResponse list_rows(list_rows_request, page=page, page_size=page_size)

List Rows

### Example


```python
import talos_aclient
from talos_aclient.models.list_rows_request import ListRowsRequest
from talos_aclient.models.list_rows_response import ListRowsResponse
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
    api_instance = talos_aclient.DatasetApi(api_client)
    list_rows_request = talos_aclient.ListRowsRequest() # ListRowsRequest | 
    page = 1 # int |  (optional) (default to 1)
    page_size = 10 # int |  (optional) (default to 10)

    try:
        # List Rows
        api_response = await api_instance.list_rows(list_rows_request, page=page, page_size=page_size)
        print("The response of DatasetApi->list_rows:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->list_rows: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_rows_request** | [**ListRowsRequest**](ListRowsRequest.md)|  | 
 **page** | **int**|  | [optional] [default to 1]
 **page_size** | **int**|  | [optional] [default to 10]

### Return type

[**ListRowsResponse**](ListRowsResponse.md)

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

# **refresh_dataset**
> object refresh_dataset(refresh_dataset_request)

Refresh Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.refresh_dataset_request import RefreshDatasetRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    refresh_dataset_request = talos_aclient.RefreshDatasetRequest() # RefreshDatasetRequest | 

    try:
        # Refresh Dataset
        api_response = await api_instance.refresh_dataset(refresh_dataset_request)
        print("The response of DatasetApi->refresh_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->refresh_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **refresh_dataset_request** | [**RefreshDatasetRequest**](RefreshDatasetRequest.md)|  | 

### Return type

**object**

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

# **refresh_resource**
> ResponseModel refresh_resource(refresh_dataset_resource_request)

Refresh Resource

### Example


```python
import talos_aclient
from talos_aclient.models.refresh_dataset_resource_request import RefreshDatasetResourceRequest
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
    api_instance = talos_aclient.DatasetApi(api_client)
    refresh_dataset_resource_request = talos_aclient.RefreshDatasetResourceRequest() # RefreshDatasetResourceRequest | 

    try:
        # Refresh Resource
        api_response = await api_instance.refresh_resource(refresh_dataset_resource_request)
        print("The response of DatasetApi->refresh_resource:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->refresh_resource: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **refresh_dataset_resource_request** | [**RefreshDatasetResourceRequest**](RefreshDatasetResourceRequest.md)|  | 

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

# **update_dataset**
> UpdateDatasetResponse update_dataset(update_dataset_request)

Update Dataset

### Example


```python
import talos_aclient
from talos_aclient.models.update_dataset_request import UpdateDatasetRequest
from talos_aclient.models.update_dataset_response import UpdateDatasetResponse
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
    api_instance = talos_aclient.DatasetApi(api_client)
    update_dataset_request = talos_aclient.UpdateDatasetRequest() # UpdateDatasetRequest | 

    try:
        # Update Dataset
        api_response = await api_instance.update_dataset(update_dataset_request)
        print("The response of DatasetApi->update_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->update_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_dataset_request** | [**UpdateDatasetRequest**](UpdateDatasetRequest.md)|  | 

### Return type

[**UpdateDatasetResponse**](UpdateDatasetResponse.md)

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

