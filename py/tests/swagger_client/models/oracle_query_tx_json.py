# coding: utf-8

"""
    Aeternity Epoch

    This is the [Aeternity](https://www.aeternity.com/) Epoch API.  # noqa: E501

    OpenAPI spec version: 0.7.0
    Contact: apiteam@aeternity.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.models.json_tx import JSONTx  # noqa: F401,E501
from swagger_client.models.ttl import TTL  # noqa: F401,E501


class OracleQueryTxJSON(object):
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
        'query_ttl': 'TTL',
        'response_ttl': 'TTL'
    }

    attribute_map = {
        'query_ttl': 'query_ttl',
        'response_ttl': 'response_ttl'
    }

    def __init__(self, query_ttl=None, response_ttl=None):  # noqa: E501
        """OracleQueryTxJSON - a model defined in Swagger"""  # noqa: E501

        self._query_ttl = None
        self._response_ttl = None
        self.discriminator = None

        self.query_ttl = query_ttl
        self.response_ttl = response_ttl

    @property
    def query_ttl(self):
        """Gets the query_ttl of this OracleQueryTxJSON.  # noqa: E501


        :return: The query_ttl of this OracleQueryTxJSON.  # noqa: E501
        :rtype: TTL
        """
        return self._query_ttl

    @query_ttl.setter
    def query_ttl(self, query_ttl):
        """Sets the query_ttl of this OracleQueryTxJSON.


        :param query_ttl: The query_ttl of this OracleQueryTxJSON.  # noqa: E501
        :type: TTL
        """
        if query_ttl is None:
            raise ValueError("Invalid value for `query_ttl`, must not be `None`")  # noqa: E501

        self._query_ttl = query_ttl

    @property
    def response_ttl(self):
        """Gets the response_ttl of this OracleQueryTxJSON.  # noqa: E501


        :return: The response_ttl of this OracleQueryTxJSON.  # noqa: E501
        :rtype: TTL
        """
        return self._response_ttl

    @response_ttl.setter
    def response_ttl(self, response_ttl):
        """Sets the response_ttl of this OracleQueryTxJSON.


        :param response_ttl: The response_ttl of this OracleQueryTxJSON.  # noqa: E501
        :type: TTL
        """
        if response_ttl is None:
            raise ValueError("Invalid value for `response_ttl`, must not be `None`")  # noqa: E501

        self._response_ttl = response_ttl

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
        if not isinstance(other, OracleQueryTxJSON):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
