# coding: utf-8

"""
    Aeternity Epoch

    This is the [Aeternity](https://www.aeternity.com/) Epoch API.  # noqa: E501

    OpenAPI spec version: 0.6.0
    Contact: apiteam@aeternity.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.models.ttl import TTL  # noqa: F401,E501


class OracleRegisterTx(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'query_format': 'str',
        'response_format': 'str',
        'query_fee': 'int',
        'fee': 'int',
        'ttl': 'TTL'
    }

    attribute_map = {
        'query_format': 'query_format',
        'response_format': 'response_format',
        'query_fee': 'query_fee',
        'fee': 'fee',
        'ttl': 'ttl'
    }

    def __init__(self, query_format=None, response_format=None, query_fee=None, fee=None, ttl=None):  # noqa: E501
        """OracleRegisterTx - a model defined in Swagger"""  # noqa: E501

        self._query_format = None
        self._response_format = None
        self._query_fee = None
        self._fee = None
        self._ttl = None
        self.discriminator = None

        if query_format is not None:
            self.query_format = query_format
        if response_format is not None:
            self.response_format = response_format
        if query_fee is not None:
            self.query_fee = query_fee
        if fee is not None:
            self.fee = fee
        if ttl is not None:
            self.ttl = ttl

    @property
    def query_format(self):
        """Gets the query_format of this OracleRegisterTx.  # noqa: E501


        :return: The query_format of this OracleRegisterTx.  # noqa: E501
        :rtype: str
        """
        return self._query_format

    @query_format.setter
    def query_format(self, query_format):
        """Sets the query_format of this OracleRegisterTx.


        :param query_format: The query_format of this OracleRegisterTx.  # noqa: E501
        :type: str
        """

        self._query_format = query_format

    @property
    def response_format(self):
        """Gets the response_format of this OracleRegisterTx.  # noqa: E501


        :return: The response_format of this OracleRegisterTx.  # noqa: E501
        :rtype: str
        """
        return self._response_format

    @response_format.setter
    def response_format(self, response_format):
        """Sets the response_format of this OracleRegisterTx.


        :param response_format: The response_format of this OracleRegisterTx.  # noqa: E501
        :type: str
        """

        self._response_format = response_format

    @property
    def query_fee(self):
        """Gets the query_fee of this OracleRegisterTx.  # noqa: E501


        :return: The query_fee of this OracleRegisterTx.  # noqa: E501
        :rtype: int
        """
        return self._query_fee

    @query_fee.setter
    def query_fee(self, query_fee):
        """Sets the query_fee of this OracleRegisterTx.


        :param query_fee: The query_fee of this OracleRegisterTx.  # noqa: E501
        :type: int
        """

        self._query_fee = query_fee

    @property
    def fee(self):
        """Gets the fee of this OracleRegisterTx.  # noqa: E501


        :return: The fee of this OracleRegisterTx.  # noqa: E501
        :rtype: int
        """
        return self._fee

    @fee.setter
    def fee(self, fee):
        """Sets the fee of this OracleRegisterTx.


        :param fee: The fee of this OracleRegisterTx.  # noqa: E501
        :type: int
        """

        self._fee = fee

    @property
    def ttl(self):
        """Gets the ttl of this OracleRegisterTx.  # noqa: E501


        :return: The ttl of this OracleRegisterTx.  # noqa: E501
        :rtype: TTL
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this OracleRegisterTx.


        :param ttl: The ttl of this OracleRegisterTx.  # noqa: E501
        :type: TTL
        """

        self._ttl = ttl

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if not isinstance(other, OracleRegisterTx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
