# coding: utf-8

"""
    Sunshine Conversations API

    The version of the OpenAPI document: 12.8.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


from sunshine_conversations_client.configuration import Configuration
from sunshine_conversations_client.undefined import Undefined


class AppListFilter(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'service_account_id': 'str'
    }

    attribute_map = {
        'service_account_id': 'serviceAccountId'
    }

    nulls = set()

    def __init__(self, service_account_id=None, local_vars_configuration=None):  # noqa: E501
        """AppListFilter - a model defined in OpenAPI"""  # noqa: E501
        
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._service_account_id = None
        self.discriminator = None

        if service_account_id is not None:
            self.service_account_id = service_account_id

    @property
    def service_account_id(self):
        """Gets the service_account_id of this AppListFilter.  # noqa: E501

        When specified, lists only the apps that the service account has access to.  # noqa: E501

        :return: The service_account_id of this AppListFilter.  # noqa: E501
        :rtype: str
        """
        return self._service_account_id

    @service_account_id.setter
    def service_account_id(self, service_account_id):
        """Sets the service_account_id of this AppListFilter.

        When specified, lists only the apps that the service account has access to.  # noqa: E501

        :param service_account_id: The service_account_id of this AppListFilter.  # noqa: E501
        :type: str
        """

        self._service_account_id = service_account_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AppListFilter):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AppListFilter):
            return True

        return self.to_dict() != other.to_dict()
