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


class NameTransferTx(object):
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
        'name_hash': 'str',
        'recipient_pubkey': 'str',
        'fee': 'int',
        'account': 'EncodedHash',
        'nonce': 'int'
    }

    attribute_map = {
        'name_hash': 'name_hash',
        'recipient_pubkey': 'recipient_pubkey',
        'fee': 'fee',
        'account': 'account',
        'nonce': 'nonce'
    }

    def __init__(self, name_hash=None, recipient_pubkey=None, fee=None, account=None, nonce=None):  # noqa: E501
        """NameTransferTx - a model defined in Swagger"""  # noqa: E501

        self._name_hash = None
        self._recipient_pubkey = None
        self._fee = None
        self._account = None
        self._nonce = None
        self.discriminator = None

        self.name_hash = name_hash
        self.recipient_pubkey = recipient_pubkey
        self.fee = fee
        if account is not None:
            self.account = account
        if nonce is not None:
            self.nonce = nonce

    @property
    def name_hash(self):
        """Gets the name_hash of this NameTransferTx.  # noqa: E501


        :return: The name_hash of this NameTransferTx.  # noqa: E501
        :rtype: str
        """
        return self._name_hash

    @name_hash.setter
    def name_hash(self, name_hash):
        """Sets the name_hash of this NameTransferTx.


        :param name_hash: The name_hash of this NameTransferTx.  # noqa: E501
        :type: str
        """
        if name_hash is None:
            raise ValueError("Invalid value for `name_hash`, must not be `None`")  # noqa: E501

        self._name_hash = name_hash

    @property
    def recipient_pubkey(self):
        """Gets the recipient_pubkey of this NameTransferTx.  # noqa: E501


        :return: The recipient_pubkey of this NameTransferTx.  # noqa: E501
        :rtype: str
        """
        return self._recipient_pubkey

    @recipient_pubkey.setter
    def recipient_pubkey(self, recipient_pubkey):
        """Sets the recipient_pubkey of this NameTransferTx.


        :param recipient_pubkey: The recipient_pubkey of this NameTransferTx.  # noqa: E501
        :type: str
        """
        if recipient_pubkey is None:
            raise ValueError("Invalid value for `recipient_pubkey`, must not be `None`")  # noqa: E501

        self._recipient_pubkey = recipient_pubkey

    @property
    def fee(self):
        """Gets the fee of this NameTransferTx.  # noqa: E501


        :return: The fee of this NameTransferTx.  # noqa: E501
        :rtype: int
        """
        return self._fee

    @fee.setter
    def fee(self, fee):
        """Sets the fee of this NameTransferTx.


        :param fee: The fee of this NameTransferTx.  # noqa: E501
        :type: int
        """
        if fee is None:
            raise ValueError("Invalid value for `fee`, must not be `None`")  # noqa: E501

        self._fee = fee

    @property
    def account(self):
        """Gets the account of this NameTransferTx.  # noqa: E501


        :return: The account of this NameTransferTx.  # noqa: E501
        :rtype: EncodedHash
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this NameTransferTx.


        :param account: The account of this NameTransferTx.  # noqa: E501
        :type: EncodedHash
        """

        self._account = account

    @property
    def nonce(self):
        """Gets the nonce of this NameTransferTx.  # noqa: E501


        :return: The nonce of this NameTransferTx.  # noqa: E501
        :rtype: int
        """
        return self._nonce

    @nonce.setter
    def nonce(self, nonce):
        """Sets the nonce of this NameTransferTx.


        :param nonce: The nonce of this NameTransferTx.  # noqa: E501
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
        if not isinstance(other, NameTransferTx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
