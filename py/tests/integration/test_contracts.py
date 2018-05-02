# coding: utf-8

import tempfile
import os
import shutil
import time
from nose.tools import assert_equals, assert_not_equals, assert_regexp_matches, with_setup
import common
from waiting import wait
from swagger_client.models.contract import Contract
from swagger_client.models.contract_call_input import ContractCallInput
from swagger_client.rest import ApiException

settings = common.test_settings(__name__.split(".")[-1])

def test_compile_and_call_id():
    # Alice should be able to compile a sophia contract with an identity
    # function into bytecode and call it.
    test_settings = settings["test_compile_and_call_id"]
    (root_dir, node, api) = setup_node(test_settings, "alice")

    # Read a contract
    currentFile = __file__
    dirPath = os.path.dirname(currentFile)
    contract_file = open(dirPath + "/identity.aes", "r")
    contract_string = contract_file.read()

    # Compile contract to bytecode
    contract = Contract( contract_string, "")
    compilation_result = api.compile_contract(contract)
    assert_regexp_matches(compilation_result.bytecode, '0x.*')

    # Call contract bytecode
    call_input = ContractCallInput("sophia", compilation_result.bytecode, "main", "42")
    call_result = api.call_contract(call_input)
    assert_regexp_matches(call_result.out, '0x.*')

    # stop node
    common.stop_node(node)
    shutil.rmtree(root_dir)

def test_encode_id_call():
    # Alice should be able to encode a call to a function in
    # a sophia contract.
    
    test_settings = settings["test_encode_id_call"]
    (root_dir, node, api) = setup_node(test_settings, "alice")

    bytecode = '0x36600080376200002160005180805180516004146200002d57505b5060011951005b80590390f35b80905090565b602001517f6d61696e00000000000000000000000000000000000000000000000000000000146200005e576200001a565b60200151806200006e9062000027565b5960008152818162000081918091505090565b8152915050905090565b825180599081525060208401602084038393509350935050600082136200008b5780925050509056'
    call_input = ContractCallInput("sophia", bytecode, "main", "42")
    result = api.encode_calldata(call_input)

    calldata = '0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000002a00000000000000000000000000000000000000000000000000000000000000046d61696e00000000000000000000000000000000000000000000000000000000'
    assert_equals(result.calldata, calldata)
    
    # stop node
    common.stop_node(node)
    shutil.rmtree(root_dir)

def test_id_call():
    # Alice should be able to call the id function in
    # an Id contract.
    
    test_settings = settings["test_id_call"]
    (root_dir, node, api) = setup_node(test_settings, "alice")

    bytecode = '0x36600080376200002160005180805180516004146200002d57505b5060011951005b80590390f35b80905090565b602001517f6d61696e00000000000000000000000000000000000000000000000000000000146200005e576200001a565b60200151806200006e9062000027565b5960008152818162000081918091505090565b8152915050905090565b825180599081525060208401602084038393509350935050600082136200008b5780925050509056'

    call_input = ContractCallInput("sophia", bytecode, "main", "42")
    result = api.call_contract(call_input)
    print(result)

    retval = '0x000000000000000000000000000000000000000000000000000000000000002a'
    assert_equals(result.out, retval)
    # stop node
    common.stop_node(node)
    shutil.rmtree(root_dir)
    

def test_solidity_greeter():
    # Alice should be able to initialize
    # the gretee Solidity contract.
    
    test_settings = settings["test_id_call"]
    (root_dir, node, api) = setup_node(test_settings, "alice")

    bytecode = greeter_code()


    call_input = ContractCallInput("evm", bytecode, "", "0x00")
    result = api.call_contract(call_input)
    print(result)

    generatedcode = greeter_generated_code()

    assert_equals(result.out, generatedcode)
    # stop node
    common.stop_node(node)
    shutil.rmtree(root_dir)

def test_call_solidity_greeter():
    # Alice should be able to call the greet function in
    # an greete Solidity contract.
    
    test_settings = settings["test_id_call"]
    (root_dir, node, api) = setup_node(test_settings, "alice")

    bytecode = greeter_generated_code()

    setGreeting = "0xa4136862"
    HelloWorld = "0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000d48656c6c6c6f20576f726c642100000000000000000000000000000000000000"
    call_input = ContractCallInput("evm", bytecode, "", setGreeting + HelloWorld)
    result = api.call_contract(call_input)
    print(result)

    generatedcode = greeter_generated_code()

    # assert_equals(result.out, generatedcode)
    # stop node
    common.stop_node(node)
    shutil.rmtree(root_dir)

    
def greeter_code():

    return "0x6060604052341561000f57600080fd5b60405161050c38038061050c83398101604052808051820191905050336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508060019080519060200190610081929190610088565b505061012d565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100c957805160ff19168380011785556100f7565b828001600101855582156100f7579182015b828111156100f65782518255916020019190600101906100db565b5b5090506101049190610108565b5090565b61012a91905b8082111561012657600081600090555060010161010e565b5090565b90565b6103d08061013c6000396000f300606060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806341c0e1b51461006757806342cbb15c1461007c578063a4136862146100a5578063cfae321714610102575b600080fd5b341561007257600080fd5b61007a610190565b005b341561008757600080fd5b61008f610221565b6040518082815260200191505060405180910390f35b34156100b057600080fd5b610100600480803590602001908201803590602001908080601f01602080910402602001604051908101604052809392919081815260200183838082843782019150505050505091905050610229565b005b341561010d57600080fd5b610115610243565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561015557808201518184015260208101905061013a565b50505050905090810190601f1680156101825780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561021f576000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b565b600043905090565b806001908051906020019061023f9291906102eb565b5050565b61024b61036b565b60018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102e15780601f106102b6576101008083540402835291602001916102e1565b820191906000526020600020905b8154815290600101906020018083116102c457829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061032c57805160ff191683800117855561035a565b8280016001018555821561035a579182015b8281111561035957825182559160200191906001019061033e565b5b509050610367919061037f565b5090565b602060405190810160405280600081525090565b6103a191905b8082111561039d576000816000905550600101610385565b5090565b905600a165627a7a7230582044f3995b80d8c9db924a58848a42198252c1f6e73a6a4423329b9641955a02dc0029"


def greeter_generated_code():
    return "0x606060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806341c0e1b51461006757806342cbb15c1461007c578063a4136862146100a5578063cfae321714610102575b600080fd5b341561007257600080fd5b61007a610190565b005b341561008757600080fd5b61008f610221565b6040518082815260200191505060405180910390f35b34156100b057600080fd5b610100600480803590602001908201803590602001908080601f01602080910402602001604051908101604052809392919081815260200183838082843782019150505050505091905050610229565b005b341561010d57600080fd5b610115610243565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561015557808201518184015260208101905061013a565b50505050905090810190601f1680156101825780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561021f576000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b565b600043905090565b806001908051906020019061023f9291906102eb565b5050565b61024b61036b565b60018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102e15780601f106102b6576101008083540402835291602001916102e1565b820191906000526020600020905b8154815290600101906020018083116102c457829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061032c57805160ff191683800117855561035a565b8280016001018555821561035a579182015b8281111561035957825182559160200191906001019061033e565b5b509050610367919061037f565b5090565b602060405190810160405280600081525090565b6103a191905b8082111561039d576000816000905550600101610385565b5090565b905600a165627a7a7230582044f3995b80d8c9db924a58848a42198252c1f6e73a6a4423329b9641955a02dc0029"

def setup_node(test_settings, node_name):
    return common.setup_node(test_settings["nodes"][node_name])
