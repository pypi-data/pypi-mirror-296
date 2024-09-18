# talos_aclient.VectorApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**vector_retrieve**](VectorApi.md#vector_retrieve) | **POST** /v1/talos/vector/retrieve | Vector Retrieve


# **vector_retrieve**
> RetrieveSegmentsResponse vector_retrieve(retrieve_segments_request)

Vector Retrieve

### Example


```python
import talos_aclient
from talos_aclient.models.retrieve_segments_request import RetrieveSegmentsRequest
from talos_aclient.models.retrieve_segments_response import RetrieveSegmentsResponse
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
    api_instance = talos_aclient.VectorApi(api_client)
    retrieve_segments_request = talos_aclient.RetrieveSegmentsRequest() # RetrieveSegmentsRequest | 

    try:
        # Vector Retrieve
        api_response = await api_instance.vector_retrieve(retrieve_segments_request)
        print("The response of VectorApi->vector_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VectorApi->vector_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **retrieve_segments_request** | [**RetrieveSegmentsRequest**](RetrieveSegmentsRequest.md)|  | 

### Return type

[**RetrieveSegmentsResponse**](RetrieveSegmentsResponse.md)

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

