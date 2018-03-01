# coding: utf-8

"""
    Aeternity Epoch

    This is the [Aeternity](https://www.aeternity.com/) Epoch API.  # noqa: E501

    OpenAPI spec version: 0.8.0
    Contact: apiteam@aeternity.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.models.encoded_hash import EncodedHash  # noqa: F401,E501


class NameClaimTx(object):
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
        'name': 'str',
        'name_salt': 'int',
        'fee': 'int',
        'account': 'EncodedHash',
        'nonce': 'int'
    }

    attribute_map = {
        'name': 'name',
        'name_salt': 'name_salt',
        'fee': 'fee',
        'account': 'account',
        'nonce': 'nonce'
    }

    def __init__(self, name=None, name_salt=None, fee=None, account=None, nonce=None):  # noqa: E501
        """NameClaimTx - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._name_salt = None
        self._fee = None
        self._account = None
        self._nonce = None
        self.discriminator = None

        self.name = name
        self.name_salt = name_salt
        self.fee = fee
        if account is not None:
            self.account = account
        if nonce is not None:
            self.nonce = nonce

    @property
    def name(self):
        """Gets the name of this NameClaimTx.  # noqa: E501


        :return: The name of this NameClaimTx.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NameClaimTx.


        :param name: The name of this NameClaimTx.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def name_salt(self):
        """Gets the name_salt of this NameClaimTx.  # noqa: E501


        :return: The name_salt of this NameClaimTx.  # noqa: E501
        :rtype: int
        """
        return self._name_salt

    @name_salt.setter
    def name_salt(self, name_salt):
        """Sets the name_salt of this NameClaimTx.


        :param name_salt: The name_salt of this NameClaimTx.  # noqa: E501
        :type: int
        """
        if name_salt is None:
            raise ValueError("Invalid value for `name_salt`, must not be `None`")  # noqa: E501

        self._name_salt = name_salt

    @property
    def fee(self):
        """Gets the fee of this NameClaimTx.  # noqa: E501


        :return: The fee of this NameClaimTx.  # noqa: E501
        :rtype: int
        """
        return self._fee

    @fee.setter
    def fee(self, fee):
        """Sets the fee of this NameClaimTx.


        :param fee: The fee of this NameClaimTx.  # noqa: E501
        :type: int
        """
        if fee is None:
            raise ValueError("Invalid value for `fee`, must not be `None`")  # noqa: E501

        self._fee = fee

    @property
    def account(self):
        """Gets the account of this NameClaimTx.  # noqa: E501


        :return: The account of this NameClaimTx.  # noqa: E501
        :rtype: EncodedHash
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this NameClaimTx.


        :param account: The account of this NameClaimTx.  # noqa: E501
        :type: EncodedHash
        """

        self._account = account

    @property
    def nonce(self):
        """Gets the nonce of this NameClaimTx.  # noqa: E501


        :return: The nonce of this NameClaimTx.  # noqa: E501
        :rtype: int
        """
        return self._nonce

    @nonce.setter
    def nonce(self, nonce):
        """Sets the nonce of this NameClaimTx.


        :param nonce: The nonce of this NameClaimTx.  # noqa: E501
        :type: int
        """

        self._nonce = nonce

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
        if not isinstance(other, NameClaimTx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
