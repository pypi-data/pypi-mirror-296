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


class CustomAllOf(object):
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
        'type': 'str',
        'webhooks': 'list[Webhook]'
    }

    attribute_map = {
        'type': 'type',
        'webhooks': 'webhooks'
    }

    nulls = set()

    def __init__(self, type='custom', webhooks=None, local_vars_configuration=None):  # noqa: E501
        """CustomAllOf - a model defined in OpenAPI"""  # noqa: E501
        
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._webhooks = None
        self.discriminator = None

        if type is not None:
            self.type = type
        self.webhooks = webhooks

    @property
    def type(self):
        """Gets the type of this CustomAllOf.  # noqa: E501

        To configure a custom integration you need to setup a webhook with a set of triggers and target.   # noqa: E501

        :return: The type of this CustomAllOf.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CustomAllOf.

        To configure a custom integration you need to setup a webhook with a set of triggers and target.   # noqa: E501

        :param type: The type of this CustomAllOf.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def webhooks(self):
        """Gets the webhooks of this CustomAllOf.  # noqa: E501

        An array of webhooks associated with the custom integration.  # noqa: E501

        :return: The webhooks of this CustomAllOf.  # noqa: E501
        :rtype: list[Webhook]
        """
        return self._webhooks

    @webhooks.setter
    def webhooks(self, webhooks):
        """Sets the webhooks of this CustomAllOf.

        An array of webhooks associated with the custom integration.  # noqa: E501

        :param webhooks: The webhooks of this CustomAllOf.  # noqa: E501
        :type: list[Webhook]
        """
        if self.local_vars_configuration.client_side_validation and webhooks is None:  # noqa: E501
            raise ValueError("Invalid value for `webhooks`, must not be `None`")  # noqa: E501

        self._webhooks = webhooks

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
        if not isinstance(other, CustomAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomAllOf):
            return True

        return self.to_dict() != other.to_dict()
