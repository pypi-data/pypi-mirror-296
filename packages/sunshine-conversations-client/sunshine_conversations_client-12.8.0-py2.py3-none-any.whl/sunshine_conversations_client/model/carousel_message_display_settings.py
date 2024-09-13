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


class CarouselMessageDisplaySettings(object):
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
        'image_aspect_ratio': 'str'
    }

    attribute_map = {
        'image_aspect_ratio': 'imageAspectRatio'
    }

    nulls = set()

    def __init__(self, image_aspect_ratio=None, local_vars_configuration=None):  # noqa: E501
        """CarouselMessageDisplaySettings - a model defined in OpenAPI"""  # noqa: E501
        
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._image_aspect_ratio = None
        self.discriminator = None

        if image_aspect_ratio is not None:
            self.image_aspect_ratio = image_aspect_ratio

    @property
    def image_aspect_ratio(self):
        """Gets the image_aspect_ratio of this CarouselMessageDisplaySettings.  # noqa: E501

        Specifies how to display all carousel images. Valid values are horizontal (default) and square. Only supported in Facebook Messenger, Web Messenger, Android SDK and iOS SDK carousels.  # noqa: E501

        :return: The image_aspect_ratio of this CarouselMessageDisplaySettings.  # noqa: E501
        :rtype: str
        """
        return self._image_aspect_ratio

    @image_aspect_ratio.setter
    def image_aspect_ratio(self, image_aspect_ratio):
        """Sets the image_aspect_ratio of this CarouselMessageDisplaySettings.

        Specifies how to display all carousel images. Valid values are horizontal (default) and square. Only supported in Facebook Messenger, Web Messenger, Android SDK and iOS SDK carousels.  # noqa: E501

        :param image_aspect_ratio: The image_aspect_ratio of this CarouselMessageDisplaySettings.  # noqa: E501
        :type: str
        """
        allowed_values = ["horizontal", "square"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and image_aspect_ratio not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `image_aspect_ratio` ({0}), must be one of {1}"  # noqa: E501
                .format(image_aspect_ratio, allowed_values)
            )

        self._image_aspect_ratio = image_aspect_ratio

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
        if not isinstance(other, CarouselMessageDisplaySettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CarouselMessageDisplaySettings):
            return True

        return self.to_dict() != other.to_dict()
