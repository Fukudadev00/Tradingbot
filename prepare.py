from web3 import Web3
import yaml
import json
import time
import solcx
with open('info.yaml') as fh:
    conf = yaml.load(fh, Loader=yaml.FullLoader)

private_key = conf['key']

BSC_url = 'https://bsc-dataseed.binance.org/'
Auro_url = 'https://mainnet.aurora.dev'
Poly_url = 'https://polygon-rpc.com'

web3 = Web3(Web3.HTTPProvider(BSC_url))
account = web3.eth.account.from_key(private_key).address
temp_file = solcx.compile_files('bsc.sol')
bsc_abi = temp_file['bsc.sol:trade']['abi']
bsc_bytecode = temp_file['bsc.sol:trade']['bin']
BSC_contract = web3.eth.contract(abi=bsc_abi, bytecode=bsc_bytecode)
construct_txn = BSC_contract.constructor().buildTransaction()
tx_create = web3.eth.account.sign_transaction(construct_txn, private_key)
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
BSC = web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress
print("BSC contract address: ", BSC)
web3 = Web3(Web3.HTTPProvider(Poly_url))
temp_file = solcx.compile_files('./contract/poly.sol')
poly_abi = temp_file['poly.sol:trade']['abi']
poly_bytecode = temp_file['poly.sol:trade']['bin']
Poly_contract = web3.eth.contract(abi=poly_abi, bytecode=poly_bytecode)
construct_txn = Poly_contract.constructor().buildTransaction()
tx_create = web3.eth.account.sign_transaction(construct_txn, private_key)
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
Poly = web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress
print("Polygon contract address: ", Poly)

web3 = Web3(Web3.HTTPProvider(Auro_url))
temp_file = solcx.compile_files('./contract/auro.sol')
auro_abi = temp_file['auro.sol:trade']['abi']
auro_bytecode = temp_file['auro.sol:trade']['bin']
Auro_contract = web3.eth.contract(abi=auro_abi, bytecode=auro_bytecode)
construct_txn = Auro_contract.constructor().buildTransaction()
tx_create = web3.eth.account.sign_transaction(construct_txn, private_key)
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
Auro = web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress
print("Aurora contract address: ", Auro)