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


class ContractCallData(object):
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
        'caller': 'str',
        'nonce': 'int',
        'contract': 'str',
        'vm_version': 'int',
        'fee': 'int',
        'amount': 'int',
        'gas': 'int',
        'gas_price': 'int',
        'call_data': 'str'
    }

    attribute_map = {
        'caller': 'caller',
        'nonce': 'nonce',
        'contract': 'contract',
        'vm_version': 'vm_version',
        'fee': 'fee',
        'amount': 'amount',
        'gas': 'gas',
        'gas_price': 'gas_price',
        'call_data': 'call_data'
    }

    def __init__(self, caller=None, nonce=None, contract=None, vm_version=None, fee=None, amount=None, gas=None, gas_price=None, call_data=None):  # noqa: E501
        """ContractCallData - a model defined in Swagger"""  # noqa: E501

        self._caller = None
        self._nonce = None
        self._contract = None
        self._vm_version = None
        self._fee = None
        self._amount = None
        self._gas = None
        self._gas_price = None
        self._call_data = None
        self.discriminator = None

        self.caller = caller
        if nonce is not None:
            self.nonce = nonce
        self.contract = contract
        self.vm_version = vm_version
        self.fee = fee
        self.amount = amount
        self.gas = gas
        self.gas_price = gas_price
        self.call_data = call_data

    @property
    def caller(self):
        """Gets the caller of this ContractCallData.  # noqa: E501

        Contract caller pub_key  # noqa: E501

        :return: The caller of this ContractCallData.  # noqa: E501
        :rtype: str
        """
        return self._caller

    @caller.setter
    def caller(self, caller):
        """Sets the caller of this ContractCallData.

        Contract caller pub_key  # noqa: E501

        :param caller: The caller of this ContractCallData.  # noqa: E501
        :type: str
        """
        if caller is None:
            raise ValueError("Invalid value for `caller`, must not be `None`")  # noqa: E501

        self._caller = caller

    @property
    def nonce(self):
        """Gets the nonce of this ContractCallData.  # noqa: E501

        Caller's nonce  # noqa: E501

        :return: The nonce of this ContractCallData.  # noqa: E501
        :rtype: int
        """
        return self._nonce

    @nonce.setter
    def nonce(self, nonce):
        """Sets the nonce of this ContractCallData.

        Caller's nonce  # noqa: E501

        :param nonce: The nonce of this ContractCallData.  # noqa: E501
        :type: int
        """

        self._nonce = nonce

    @property
    def contract(self):
        """Gets the contract of this ContractCallData.  # noqa: E501

        Contract's pub_key  # noqa: E501

        :return: The contract of this ContractCallData.  # noqa: E501
        :rtype: str
        """
        return self._contract

    @contract.setter
    def contract(self, contract):
        """Sets the contract of this ContractCallData.

        Contract's pub_key  # noqa: E501

        :param contract: The contract of this ContractCallData.  # noqa: E501
        :type: str
        """
        if contract is None:
            raise ValueError("Invalid value for `contract`, must not be `None`")  # noqa: E501

        self._contract = contract

    @property
    def vm_version(self):
        """Gets the vm_version of this ContractCallData.  # noqa: E501

        Virtual machine's version  # noqa: E501

        :return: The vm_version of this ContractCallData.  # noqa: E501
        :rtype: int
        """
        return self._vm_version

    @vm_version.setter
    def vm_version(self, vm_version):
        """Sets the vm_version of this ContractCallData.

        Virtual machine's version  # noqa: E501

        :param vm_version: The vm_version of this ContractCallData.  # noqa: E501
        :type: int
        """
        if vm_version is None:
            raise ValueError("Invalid value for `vm_version`, must not be `None`")  # noqa: E501
        if vm_version is not None and vm_version > 255:  # noqa: E501
            raise ValueError("Invalid value for `vm_version`, must be a value less than or equal to `255`")  # noqa: E501
        if vm_version is not None and vm_version < 0:  # noqa: E501
            raise ValueError("Invalid value for `vm_version`, must be a value greater than or equal to `0`")  # noqa: E501

        self._vm_version = vm_version

    @property
    def fee(self):
        """Gets the fee of this ContractCallData.  # noqa: E501

        Transaction fee  # noqa: E501

        :return: The fee of this ContractCallData.  # noqa: E501
        :rtype: int
        """
        return self._fee

    @fee.setter
    def fee(self, fee):
        """Sets the fee of this ContractCallData.

        Transaction fee  # noqa: E501

        :param fee: The fee of this ContractCallData.  # noqa: E501
        :type: int
        """
        if fee is None:
            raise ValueError("Invalid value for `fee`, must not be `None`")  # noqa: E501
        if fee is not None and fee < 0:  # noqa: E501
            raise ValueError("Invalid value for `fee`, must be a value greater than or equal to `0`")  # noqa: E501

        self._fee = fee

    @property
    def amount(self):
        """Gets the amount of this ContractCallData.  # noqa: E501

        Amount  # noqa: E501

        :return: The amount of this ContractCallData.  # noqa: E501
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this ContractCallData.

        Amount  # noqa: E501

        :param amount: The amount of this ContractCallData.  # noqa: E501
        :type: int
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501
        if amount is not None and amount < 0:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must be a value greater than or equal to `0`")  # noqa: E501

        self._amount = amount

    @property
    def gas(self):
        """Gets the gas of this ContractCallData.  # noqa: E501

        Contract gas  # noqa: E501

        :return: The gas of this ContractCallData.  # noqa: E501
        :rtype: int
        """
        return self._gas

    @gas.setter
    def gas(self, gas):
        """Sets the gas of this ContractCallData.

        Contract gas  # noqa: E501

        :param gas: The gas of this ContractCallData.  # noqa: E501
        :type: int
        """
        if gas is None:
            raise ValueError("Invalid value for `gas`, must not be `None`")  # noqa: E501
        if gas is not None and gas < 0:  # noqa: E501
            raise ValueError("Invalid value for `gas`, must be a value greater than or equal to `0`")  # noqa: E501

        self._gas = gas

    @property
    def gas_price(self):
        """Gets the gas_price of this ContractCallData.  # noqa: E501

        Gas price  # noqa: E501

        :return: The gas_price of this ContractCallData.  # noqa: E501
        :rtype: int
        """
        return self._gas_price

    @gas_price.setter
    def gas_price(self, gas_price):
        """Sets the gas_price of this ContractCallData.

        Gas price  # noqa: E501

        :param gas_price: The gas_price of this ContractCallData.  # noqa: E501
        :type: int
        """
        if gas_price is None:
            raise ValueError("Invalid value for `gas_price`, must not be `None`")  # noqa: E501
        if gas_price is not None and gas_price < 0:  # noqa: E501
            raise ValueError("Invalid value for `gas_price`, must be a value greater than or equal to `0`")  # noqa: E501

        self._gas_price = gas_price

    @property
    def call_data(self):
        """Gets the call_data of this ContractCallData.  # noqa: E501

        Contract call data  # noqa: E501

        :return: The call_data of this ContractCallData.  # noqa: E501
        :rtype: str
        """
        return self._call_data

    @call_data.setter
    def call_data(self, call_data):
        """Sets the call_data of this ContractCallData.

        Contract call data  # noqa: E501

        :param call_data: The call_data of this ContractCallData.  # noqa: E501
        :type: str
        """
        if call_data is None:
            raise ValueError("Invalid value for `call_data`, must not be `None`")  # noqa: E501

        self._call_data = call_data

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
        if not isinstance(other, ContractCallData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
