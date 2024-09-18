# talos_aclient.SegmentApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_segments**](SegmentApi.md#delete_segments) | **POST** /v1/talos/segment/delete | Delete Segments
[**list_segments**](SegmentApi.md#list_segments) | **POST** /v1/talos/segment/list | List Segments
[**update_segment**](SegmentApi.md#update_segment) | **POST** /v1/talos/segment/update | Update Segment


# **delete_segments**
> ResponseModel delete_segments(delete_segment_request)

Delete Segments

### Example


```python
import talos_aclient
from talos_aclient.models.delete_segment_request import DeleteSegmentRequest
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
    api_instance = talos_aclient.SegmentApi(api_client)
    delete_segment_request = talos_aclient.DeleteSegmentRequest() # DeleteSegmentRequest | 

    try:
        # Delete Segments
        api_response = await api_instance.delete_segments(delete_segment_request)
        print("The response of SegmentApi->delete_segments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SegmentApi->delete_segments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_segment_request** | [**DeleteSegmentRequest**](DeleteSegmentRequest.md)|  | 

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

# **list_segments**
> ListSegmentsResponse list_segments(list_segments_request, page=page, page_size=page_size)

List Segments

### Example


```python
import talos_aclient
from talos_aclient.models.list_segments_request import ListSegmentsRequest
from talos_aclient.models.list_segments_response import ListSegmentsResponse
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
    api_instance = talos_aclient.SegmentApi(api_client)
    list_segments_request = talos_aclient.ListSegmentsRequest() # ListSegmentsRequest | 
    page = 1 # int |  (optional) (default to 1)
    page_size = 10 # int |  (optional) (default to 10)

    try:
        # List Segments
        api_response = await api_instance.list_segments(list_segments_request, page=page, page_size=page_size)
        print("The response of SegmentApi->list_segments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SegmentApi->list_segments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_segments_request** | [**ListSegmentsRequest**](ListSegmentsRequest.md)|  | 
 **page** | **int**|  | [optional] [default to 1]
 **page_size** | **int**|  | [optional] [default to 10]

### Return type

[**ListSegmentsResponse**](ListSegmentsResponse.md)

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

# **update_segment**
> UpdateSegmentResponse update_segment(update_segment_request)

Update Segment

### Example


```python
import talos_aclient
from talos_aclient.models.update_segment_request import UpdateSegmentRequest
from talos_aclient.models.update_segment_response import UpdateSegmentResponse
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
    api_instance = talos_aclient.SegmentApi(api_client)
    update_segment_request = talos_aclient.UpdateSegmentRequest() # UpdateSegmentRequest | 

    try:
        # Update Segment
        api_response = await api_instance.update_segment(update_segment_request)
        print("The response of SegmentApi->update_segment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SegmentApi->update_segment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_segment_request** | [**UpdateSegmentRequest**](UpdateSegmentRequest.md)|  | 

### Return type

[**UpdateSegmentResponse**](UpdateSegmentResponse.md)

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

