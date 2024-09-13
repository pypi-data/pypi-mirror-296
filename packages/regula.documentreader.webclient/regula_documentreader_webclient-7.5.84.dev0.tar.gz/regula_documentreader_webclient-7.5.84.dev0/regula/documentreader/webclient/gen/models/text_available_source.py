# coding: utf-8

"""
    Generated by: https://openapi-generator.tech
"""

import pprint
import re  # noqa: F401

import six

from regula.documentreader.webclient.gen.configuration import Configuration
# this line was added to enable pycharm type hinting
from regula.documentreader.webclient.gen.models import *


"""

"""
class TextAvailableSource(object):
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
        'source': 'Source',
        'validity_status': 'CheckResult',
        'container_type': 'int'
    }

    attribute_map = {
        'source': 'source',
        'validity_status': 'validityStatus',
        'container_type': 'containerType'
    }

    def __init__(self, source=None, validity_status=None, container_type=0, local_vars_configuration=None):  # noqa: E501
        """TextAvailableSource - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._source = None
        self._validity_status = None
        self._container_type = None
        self.discriminator = None

        self.source = source
        self.validity_status = validity_status
        if container_type is not None:
            self.container_type = container_type

    @property
    def source(self):
        """Gets the source of this TextAvailableSource.  # noqa: E501


        :return: The source of this TextAvailableSource.  # noqa: E501
        :rtype: Source
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this TextAvailableSource.


        :param source: The source of this TextAvailableSource.  # noqa: E501
        :type source: Source
        """
        if self.local_vars_configuration.client_side_validation and source is None:  # noqa: E501
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source

    @property
    def validity_status(self):
        """Gets the validity_status of this TextAvailableSource.  # noqa: E501


        :return: The validity_status of this TextAvailableSource.  # noqa: E501
        :rtype: CheckResult
        """
        return self._validity_status

    @validity_status.setter
    def validity_status(self, validity_status):
        """Sets the validity_status of this TextAvailableSource.


        :param validity_status: The validity_status of this TextAvailableSource.  # noqa: E501
        :type validity_status: CheckResult
        """
        if self.local_vars_configuration.client_side_validation and validity_status is None:  # noqa: E501
            raise ValueError("Invalid value for `validity_status`, must not be `None`")  # noqa: E501

        self._validity_status = validity_status

    @property
    def container_type(self):
        """Gets the container_type of this TextAvailableSource.  # noqa: E501

        Same as Result type, but used for safe parsing of not-described values. See Result type.  # noqa: E501

        :return: The container_type of this TextAvailableSource.  # noqa: E501
        :rtype: int
        """
        return self._container_type

    @container_type.setter
    def container_type(self, container_type):
        """Sets the container_type of this TextAvailableSource.

        Same as Result type, but used for safe parsing of not-described values. See Result type.  # noqa: E501

        :param container_type: The container_type of this TextAvailableSource.  # noqa: E501
        :type container_type: int
        """

        self._container_type = container_type

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
        if not isinstance(other, TextAvailableSource):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TextAvailableSource):
            return True

        return self.to_dict() != other.to_dict()
