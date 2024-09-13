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


class ParticipantLeaveBody(object):
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
        'user_id': 'str',
        'user_external_id': 'str',
        'participant_id': 'str'
    }

    attribute_map = {
        'user_id': 'userId',
        'user_external_id': 'userExternalId',
        'participant_id': 'participantId'
    }

    nulls = set()

    def __init__(self, user_id=None, user_external_id=None, participant_id=None, local_vars_configuration=None):  # noqa: E501
        """ParticipantLeaveBody - a model defined in OpenAPI"""  # noqa: E501
        
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._user_id = None
        self._user_external_id = None
        self._participant_id = None
        self.discriminator = None

        if user_id is not None:
            self.user_id = user_id
        if user_external_id is not None:
            self.user_external_id = user_external_id
        if participant_id is not None:
            self.participant_id = participant_id

    @property
    def user_id(self):
        """Gets the user_id of this ParticipantLeaveBody.  # noqa: E501

        The id of the user that will be removed from the conversation. It will return 404 if the user can’t be found.   # noqa: E501

        :return: The user_id of this ParticipantLeaveBody.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ParticipantLeaveBody.

        The id of the user that will be removed from the conversation. It will return 404 if the user can’t be found.   # noqa: E501

        :param user_id: The user_id of this ParticipantLeaveBody.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def user_external_id(self):
        """Gets the user_external_id of this ParticipantLeaveBody.  # noqa: E501

        The externalId of the user that will be removed from the conversation. It will return 404 if the user can’t be found.   # noqa: E501

        :return: The user_external_id of this ParticipantLeaveBody.  # noqa: E501
        :rtype: str
        """
        return self._user_external_id

    @user_external_id.setter
    def user_external_id(self, user_external_id):
        """Sets the user_external_id of this ParticipantLeaveBody.

        The externalId of the user that will be removed from the conversation. It will return 404 if the user can’t be found.   # noqa: E501

        :param user_external_id: The user_external_id of this ParticipantLeaveBody.  # noqa: E501
        :type: str
        """

        self._user_external_id = user_external_id

    @property
    def participant_id(self):
        """Gets the participant_id of this ParticipantLeaveBody.  # noqa: E501

        The participantId of the user that will be removed from the conversation. It will return 404 if the user can’t be found.   # noqa: E501

        :return: The participant_id of this ParticipantLeaveBody.  # noqa: E501
        :rtype: str
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        """Sets the participant_id of this ParticipantLeaveBody.

        The participantId of the user that will be removed from the conversation. It will return 404 if the user can’t be found.   # noqa: E501

        :param participant_id: The participant_id of this ParticipantLeaveBody.  # noqa: E501
        :type: str
        """

        self._participant_id = participant_id

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
        if not isinstance(other, ParticipantLeaveBody):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ParticipantLeaveBody):
            return True

        return self.to_dict() != other.to_dict()
