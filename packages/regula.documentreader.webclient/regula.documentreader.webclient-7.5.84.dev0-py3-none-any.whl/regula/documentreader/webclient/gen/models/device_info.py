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
class DeviceInfo(object):
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
        'app_name': 'str',
        'version': 'str',
        'license_id': 'str',
        'license_serial': 'str',
        'valid_until': 'datetime',
        'server_time': 'datetime'
    }

    attribute_map = {
        'app_name': 'app-name',
        'version': 'version',
        'license_id': 'license-id',
        'license_serial': 'license-serial',
        'valid_until': 'valid-until',
        'server_time': 'server-time'
    }

    def __init__(self, app_name=None, version=None, license_id=None, license_serial=None, valid_until=None, server_time=None, local_vars_configuration=None):  # noqa: E501
        """DeviceInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._app_name = None
        self._version = None
        self._license_id = None
        self._license_serial = None
        self._valid_until = None
        self._server_time = None
        self.discriminator = None

        if app_name is not None:
            self.app_name = app_name
        if version is not None:
            self.version = version
        if license_id is not None:
            self.license_id = license_id
        if license_serial is not None:
            self.license_serial = license_serial
        if valid_until is not None:
            self.valid_until = valid_until
        if server_time is not None:
            self.server_time = server_time

    @property
    def app_name(self):
        """Gets the app_name of this DeviceInfo.  # noqa: E501


        :return: The app_name of this DeviceInfo.  # noqa: E501
        :rtype: str
        """
        return self._app_name

    @app_name.setter
    def app_name(self, app_name):
        """Sets the app_name of this DeviceInfo.


        :param app_name: The app_name of this DeviceInfo.  # noqa: E501
        :type app_name: str
        """

        self._app_name = app_name

    @property
    def version(self):
        """Gets the version of this DeviceInfo.  # noqa: E501


        :return: The version of this DeviceInfo.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DeviceInfo.


        :param version: The version of this DeviceInfo.  # noqa: E501
        :type version: str
        """

        self._version = version

    @property
    def license_id(self):
        """Gets the license_id of this DeviceInfo.  # noqa: E501


        :return: The license_id of this DeviceInfo.  # noqa: E501
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this DeviceInfo.


        :param license_id: The license_id of this DeviceInfo.  # noqa: E501
        :type license_id: str
        """

        self._license_id = license_id

    @property
    def license_serial(self):
        """Gets the license_serial of this DeviceInfo.  # noqa: E501


        :return: The license_serial of this DeviceInfo.  # noqa: E501
        :rtype: str
        """
        return self._license_serial

    @license_serial.setter
    def license_serial(self, license_serial):
        """Sets the license_serial of this DeviceInfo.


        :param license_serial: The license_serial of this DeviceInfo.  # noqa: E501
        :type license_serial: str
        """

        self._license_serial = license_serial

    @property
    def valid_until(self):
        """Gets the valid_until of this DeviceInfo.  # noqa: E501


        :return: The valid_until of this DeviceInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._valid_until

    @valid_until.setter
    def valid_until(self, valid_until):
        """Sets the valid_until of this DeviceInfo.


        :param valid_until: The valid_until of this DeviceInfo.  # noqa: E501
        :type valid_until: datetime
        """

        self._valid_until = valid_until

    @property
    def server_time(self):
        """Gets the server_time of this DeviceInfo.  # noqa: E501


        :return: The server_time of this DeviceInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._server_time

    @server_time.setter
    def server_time(self, server_time):
        """Sets the server_time of this DeviceInfo.


        :param server_time: The server_time of this DeviceInfo.  # noqa: E501
        :type server_time: datetime
        """

        self._server_time = server_time

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
        if not isinstance(other, DeviceInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeviceInfo):
            return True

        return self.to_dict() != other.to_dict()
