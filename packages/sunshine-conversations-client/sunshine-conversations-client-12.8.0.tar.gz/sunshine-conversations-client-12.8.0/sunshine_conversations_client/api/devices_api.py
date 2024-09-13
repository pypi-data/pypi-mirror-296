# coding: utf-8

"""
    Sunshine Conversations API

    The version of the OpenAPI document: 12.8.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from sunshine_conversations_client.api_client import ApiClient
from sunshine_conversations_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class DevicesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_device(self, app_id, user_id_or_external_id, device_id, **kwargs):  # noqa: E501
        """Get Device  # noqa: E501

        Fetches a specific Device.  ```shell /v2/apps/:appId/users/:userId ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_device(app_id, user_id_or_external_id, device_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str app_id: Identifies the app. (required)
        :param str user_id_or_external_id: The user's id or externalId. (required)
        :param str device_id: The device's id. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DeviceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_device_with_http_info(app_id, user_id_or_external_id, device_id, **kwargs)  # noqa: E501

    def get_device_with_http_info(self, app_id, user_id_or_external_id, device_id, **kwargs):  # noqa: E501
        """Get Device  # noqa: E501

        Fetches a specific Device.  ```shell /v2/apps/:appId/users/:userId ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_device_with_http_info(app_id, user_id_or_external_id, device_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str app_id: Identifies the app. (required)
        :param str user_id_or_external_id: The user's id or externalId. (required)
        :param str device_id: The device's id. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DeviceResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'app_id',
            'user_id_or_external_id',
            'device_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_device" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ('app_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['app_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `get_device`")  # noqa: E501
        # verify the required parameter 'user_id_or_external_id' is set
        if self.api_client.client_side_validation and ('user_id_or_external_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['user_id_or_external_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `user_id_or_external_id` when calling `get_device`")  # noqa: E501
        # verify the required parameter 'device_id' is set
        if self.api_client.client_side_validation and ('device_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['device_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `device_id` when calling `get_device`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'app_id' in local_var_params:
            path_params['appId'] = local_var_params['app_id']  # noqa: E501
        if 'user_id_or_external_id' in local_var_params:
            path_params['userIdOrExternalId'] = local_var_params['user_id_or_external_id']  # noqa: E501
        if 'device_id' in local_var_params:
            path_params['deviceId'] = local_var_params['device_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/apps/{appId}/users/{userIdOrExternalId}/devices/{deviceId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeviceResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_devices(self, app_id, user_id_or_external_id, **kwargs):  # noqa: E501
        """List Devices  # noqa: E501

        Get all the devices for a particular user. The Devices are sorted based on last seen time.  ```shell /v2/apps/:appId/users/:userId/devices ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_devices(app_id, user_id_or_external_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str app_id: Identifies the app. (required)
        :param str user_id_or_external_id: The user's id or externalId. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ClientListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_devices_with_http_info(app_id, user_id_or_external_id, **kwargs)  # noqa: E501

    def list_devices_with_http_info(self, app_id, user_id_or_external_id, **kwargs):  # noqa: E501
        """List Devices  # noqa: E501

        Get all the devices for a particular user. The Devices are sorted based on last seen time.  ```shell /v2/apps/:appId/users/:userId/devices ```   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_devices_with_http_info(app_id, user_id_or_external_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str app_id: Identifies the app. (required)
        :param str user_id_or_external_id: The user's id or externalId. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ClientListResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'app_id',
            'user_id_or_external_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_devices" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ('app_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['app_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `list_devices`")  # noqa: E501
        # verify the required parameter 'user_id_or_external_id' is set
        if self.api_client.client_side_validation and ('user_id_or_external_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['user_id_or_external_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `user_id_or_external_id` when calling `list_devices`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'app_id' in local_var_params:
            path_params['appId'] = local_var_params['app_id']  # noqa: E501
        if 'user_id_or_external_id' in local_var_params:
            path_params['userIdOrExternalId'] = local_var_params['user_id_or_external_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/apps/{appId}/users/{userIdOrExternalId}/devices', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ClientListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
