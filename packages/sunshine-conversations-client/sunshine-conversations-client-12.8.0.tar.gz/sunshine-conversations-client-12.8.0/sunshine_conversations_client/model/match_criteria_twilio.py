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


class MatchCriteriaTwilio(object):
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
        'integration_id': 'str',
        'primary': 'bool',
        'phone_number': 'str'
    }

    attribute_map = {
        'type': 'type',
        'integration_id': 'integrationId',
        'primary': 'primary',
        'phone_number': 'phoneNumber'
    }

    nulls = set()

    def __init__(self, type='twilio', integration_id=None, primary=True, phone_number=None, local_vars_configuration=None):  # noqa: E501
        """MatchCriteriaTwilio - a model defined in OpenAPI"""  # noqa: E501
        
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._integration_id = None
        self._primary = None
        self._phone_number = None
        self.discriminator = None

        self.type = type
        self.integration_id = integration_id
        if primary is not None:
            self.primary = primary
        self.phone_number = phone_number

    @property
    def type(self):
        """Gets the type of this MatchCriteriaTwilio.  # noqa: E501

        The channel type.  # noqa: E501

        :return: The type of this MatchCriteriaTwilio.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this MatchCriteriaTwilio.

        The channel type.  # noqa: E501

        :param type: The type of this MatchCriteriaTwilio.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def integration_id(self):
        """Gets the integration_id of this MatchCriteriaTwilio.  # noqa: E501

        The ID of the integration to link. Must match the provided type.  # noqa: E501

        :return: The integration_id of this MatchCriteriaTwilio.  # noqa: E501
        :rtype: str
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """Sets the integration_id of this MatchCriteriaTwilio.

        The ID of the integration to link. Must match the provided type.  # noqa: E501

        :param integration_id: The integration_id of this MatchCriteriaTwilio.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and integration_id is None:  # noqa: E501
            raise ValueError("Invalid value for `integration_id`, must not be `None`")  # noqa: E501

        self._integration_id = integration_id

    @property
    def primary(self):
        """Gets the primary of this MatchCriteriaTwilio.  # noqa: E501

        Flag indicating whether the client will become the primary for the target conversation once linking is complete.  # noqa: E501

        :return: The primary of this MatchCriteriaTwilio.  # noqa: E501
        :rtype: bool
        """
        return self._primary

    @primary.setter
    def primary(self, primary):
        """Sets the primary of this MatchCriteriaTwilio.

        Flag indicating whether the client will become the primary for the target conversation once linking is complete.  # noqa: E501

        :param primary: The primary of this MatchCriteriaTwilio.  # noqa: E501
        :type: bool
        """

        self._primary = primary

    @property
    def phone_number(self):
        """Gets the phone_number of this MatchCriteriaTwilio.  # noqa: E501

        The user’s phone number. It must contain the + prefix and the country code. Examples of valid phone numbers: +1 212-555-2368, +12125552368, +1 212 555 2368. Examples of invalid phone numbers: 212 555 2368, 1 212 555 2368.   # noqa: E501

        :return: The phone_number of this MatchCriteriaTwilio.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this MatchCriteriaTwilio.

        The user’s phone number. It must contain the + prefix and the country code. Examples of valid phone numbers: +1 212-555-2368, +12125552368, +1 212 555 2368. Examples of invalid phone numbers: 212 555 2368, 1 212 555 2368.   # noqa: E501

        :param phone_number: The phone_number of this MatchCriteriaTwilio.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and phone_number is None:  # noqa: E501
            raise ValueError("Invalid value for `phone_number`, must not be `None`")  # noqa: E501

        self._phone_number = phone_number

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
        if not isinstance(other, MatchCriteriaTwilio):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MatchCriteriaTwilio):
            return True

        return self.to_dict() != other.to_dict()
