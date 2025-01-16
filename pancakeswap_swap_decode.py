import asyncio

from asyncio import sleep
from dataclasses import dataclass

import aiohttp


from web3 import Web3


from decimal import Decimal
from typing import Optional
import requests
from web3 import AsyncWeb3
from web3.exceptions import Web3RPCError
import json


import time
import datetime
import requests
from decimal import Decimal, getcontext

from eth_utils import keccak
from eth_abi import decode
from colorama import Fore, Style

decimals = 18
from datetime import datetime


import sys
# Устанавливаем точность для вычислений Decimal
getcontext().prec = 50
class style():  # Class of different text colours - default is white
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'



def getTimestamp():
    while True:
        timeStampData = datetime.datetime.now()
        currentTimeStamp = "[" + timeStampData.strftime("%H:%M:%S.%f")[:-3] + "]"
        return currentTimeStamp


class style():  # Class of different text colours - default is white
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# ABI Factory контракта PancakeSwap
factory_abi = [
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "tokenA", "type": "address"},
            {"internalType": "address", "name": "tokenB", "type": "address"},
        ],
        "name": "getPair",
        "outputs": [{"internalType": "address", "name": "pair", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

panabi = json.loads("""
[
    {
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [{"name": "amounts", "type": "uint256[]"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
""")  # Replace with the full ABI

def getTimestamp():
    while True:
        timeStampData = datetime.now()
        currentTimeStamp = "[" + timeStampData.strftime("%H:%M:%S.%f")[:-3] + "]"
        return currentTimeStamp


web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed2.binance.org/"))
if web3.is_connected():
    print(getTimestamp()," BSC Node successfully connected")





# ABI контракта пула (Pair)
pair_abi_reserve = [
    {
        "constant": True,
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
            {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
            {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]


# pancakeswap factory
factory_address = "0xca143ce32fe78f1f7019d7d551a6402fc5350c73"

# Преобразование Factory-адреса в checksum формат
factory_address = Web3.to_checksum_address(factory_address)


# Connect to BSC via Web3
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed2.binance.org/"))

# Check if connected to BSC
if web3.is_connected():
    print("BSC Node successfully connected")

# Define the ABI for Transfer events (ERC-20 standard)
token_abi = json.loads(
    '[{"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "from", "type": "address"}, {"indexed": true, "internalType": "address", "name": "to", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"}]'
)

# Replace with your token's contract address (e.g., WBNB)
token_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"  # WBNB contract address
token_contract = web3.eth.contract(address=token_address, abi=token_abi)

# Event handler
transaction_hashes = []


# Define PancakeSwap Router contract address
panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

# Instantiate contract
contractbuy = web3.eth.contract(address=panRouterContractAddress, abi=panabi)



# Множество для хранения уже обработанных хэшей транзакций
processed_hashes = set()
event_filter = token_contract.events.Transfer.create_filter(from_block="latest")




@dataclass
class TokenData:
    token_name_0: str
    token_address_0: str
    token_symbol_0: str
    token_reserve_0: Decimal
    price_token_in_wbnb: Decimal
    
    token_name_1: str
    token_symbol_1: str
    token_address_1: str
    token_reserve_1: Decimal
    price_wbnb_in_token: Decimal

    tx_hash: str

    value1: Optional[Decimal] = None
    value2: Optional[Decimal] = None

    # Новые поля
    token_price_usdt: Optional[Decimal] = None
    wbnb_price_in_usdt: Optional[Decimal] = None






class TokenInfoPrinter:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    def display(self, tokens: list[TokenData]) -> None:
        for token in tokens:
            
            print(
                f"{self.YELLOW}[{datetime.now().strftime("%H:%M:%S.%f")[:-3]}][Token] New Token Detected: {self.CYAN}{token.token_name_0} ({token.token_symbol_0}) reserve_token0({token.token_reserve_0})/{self.CYAN}{token.token_name_1} ({token.token_symbol_1}) reserve_token1({token.token_reserve_1}): {self.MAGENTA}{token.token_address_0} / {token.token_address_1} https://bscscan.com/tx/{token.tx_hash}{self.RESET} Price: Token0_count_IN={str(token.value1)}, Token1_count_OUT={str(token.value2)}"
            )





class TokenPriceCollector:
    
    def __init__(
        self,
        token_info_printer: TokenInfoPrinter,
    ):
        self._tokens_to_check: list[TokenData] = []
        self._token_info_printer = token_info_printer
        self.wbnb_address = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c".lower()  # WBNB address

    async def run(self) -> None:
        while True:
            pending_tokens = []
            checked_tokens = []

            for i, token in enumerate(self._tokens_to_check):
                if i > 29:
                    break

                # Fetch prices for the token addresses
                # List of token addresses to check



                # Assign fetched prices to tokens after looping
                #token.token_price0 = token_price0
                #token.token_price1 = token_price1
                
                checked_tokens.append(token)

            # Update the tokens to check and display the checked tokens
            self._tokens_to_check = pending_tokens
            self._token_info_printer.display(tokens=checked_tokens)

            await asyncio.sleep(5)


    def add_to_queue(
        self,
        token_data: TokenData,
    ) -> None:
        self._tokens_to_check.append(token_data)




class TokensCollector:
    
    def __init__(
        self,
        token_price_collector: TokenPriceCollector,
        liquidity_pair_address: str = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
    ):
        self._web_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider("https://bsc-dataseed2.binance.org/"))
        self._token_price_collector = token_price_collector
        self._liquidity_pair_address = liquidity_pair_address

        self._contract = self._web_client.eth.contract(  # noqa
            address='0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73',  # Testnet #0x6725F303b657a9451d8BA641348b6761A6CC7a17
            abi=json.loads(
                '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
            ),
        )
        self._token_name_abi = json.loads(
            '[ { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "spender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "_owner", "type": "address" }, { "internalType": "address", "name": "spender", "type": "address" } ], "name": "allowance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "approve", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "account", "type": "address" } ], "name": "balanceOf", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getOwner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "name", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transfer", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]'
        )



    async def run(self) -> None:
        global get_token_name00, get_token_name_11, reserve_token0_normal, reserve_token1_normal  
        global token_address_0, token_address_1, price_token_in_wbnb, price_wbnb_in_token
        # Initialize the default variables
        get_token_name00 = None
        get_token_name_11 = None
        reserve_token0_normal = 0
        reserve_token1_normal = 0

        while True:
            for event in event_filter.get_new_entries():
                
                
                transaction_hash = Web3.to_hex(event['transactionHash'])

                # If the hash has already been processed, skip it
                if transaction_hash in processed_hashes:
                    continue

                # Add the hash to the processed set
                processed_hashes.add(transaction_hash)

                try:
                    # Get the details of the transaction
                    tranz_hash = web3.eth.get_transaction(transaction_hash)
                    input_data = tranz_hash["input"]
                    selector = input_data[:4]

                    try:
                            # Trying to decode the function
                        func_obj, func_params = contractbuy.decode_function_input(input_data)

                    except ValueError:
                        try:
                            # Manual decoding
                            param_types = ["uint256", "uint256", "address[]", "address", "uint256"]
                            encoded_params = input_data[4:]  # Remove the selector
                            decoded_params = decode(param_types, bytes.fromhex(encoded_params.hex()))
                            #print(decoded_params)
                            #pancakeswap transactions filter
                            if isinstance(decoded_params, tuple) and len(decoded_params) == 5:
                                if 1 < len(decoded_params[2]) < 3:
                                    value1 = decoded_params[0] / 10**18
                                    value2 = decoded_params[1] / 10**18

                                    # Check that value2 is not equal to 0
                                    #some value2 transactions have 0 , It shouldn't be like this, but the decode is correct , check https://bscscan.com/inputdatadecoder. 
                                    if decoded_params[1] != 0:  # Check the original numeric value
                                        token_address_0, token_address_1 = decoded_params[2]
                                        value1_formatted = f"{value1:.18f}"
                                        value2_formatted = f"{value2:.18f}"
                                        


                                        #print(value1)
                                        #print(value2)
                                        token_address_0_checksum = Web3.to_checksum_address(token_address_0.lower())
                                        token_address_1_checksum = Web3.to_checksum_address(token_address_1.lower())

                                        factory_contract = web3.eth.contract(address=factory_address, abi=factory_abi)
                                        try:
                                            # Make sure the token addresses are in the correct format
                                            token_address_0_checksum = Web3.to_checksum_address(token_address_0.lower())
                                            token_address_1_checksum = Web3.to_checksum_address(token_address_1.lower())

                                            factory_contract = web3.eth.contract(address=factory_address, abi=factory_abi)
                                            pair_address = factory_contract.functions.getPair(token_address_0_checksum, token_address_1_checksum).call()

                                            if pair_address != "0x0000000000000000000000000000000000000000":
                                                pair_contract = web3.eth.contract(address=pair_address, abi=pair_abi_reserve)
                                                reserves = pair_contract.functions.getReserves().call()

                                                reserve_token0_normal = Decimal(reserves[0]) / Decimal(10**decimals)
                                                reserve_token1_normal = Decimal(reserves[1]) / Decimal(10**decimals)

                                                # Setting up the token contract
                                                token_address_00 = token_address_0_checksum
                                                get_token_name00 = self._web_client.eth.contract(
                                                    address=token_address_00,
                                                    abi=self._token_name_abi,
                                                )

                                                token_address_11 = token_address_1_checksum
                                                get_token_name_11 = self._web_client.eth.contract(
                                                    address=token_address_11,
                                                    abi=self._token_name_abi,
                                                )

                                                price_token_in_wbnb = reserve_token1_normal / reserve_token0_normal

                                                price_wbnb_in_token = reserve_token0_normal / reserve_token1_normal



                                                #print("Added new token.")
                                                token_data = TokenData(
                                                    token_name_0=await get_token_name00.functions.name().call(),
                                                    token_symbol_0=await get_token_name00.functions.symbol().call(),
                                                    token_address_0=token_address_00,
                                                    token_reserve_0=reserve_token0_normal,
                                                    price_token_in_wbnb = price_token_in_wbnb,
                                                    value1=value1,
                                                    token_name_1=await get_token_name_11.functions.name().call(),
                                                    token_symbol_1=await get_token_name_11.functions.symbol().call(),
                                                    token_address_1=token_address_11,
                                                    token_reserve_1=reserve_token1_normal,
                                                    price_wbnb_in_token=price_wbnb_in_token,
                                                    value2=value2,
                                                    tx_hash=self._web_client.to_hex(event['transactionHash']),
                                                )
                                                #print(f"Adding TokenData: {token_data}")

                                                self._token_price_collector.add_to_queue(token_data=token_data)

                                                time.sleep(1)

                                        except Exception as e:
                                            #print(f"Error while checking pair: {e}")
                                            continue


                        except Exception as manual_error:
                            pass
                except Exception as e:
                    pass 



async def main():
    token_price_collector = TokenPriceCollector(
        token_info_printer=TokenInfoPrinter(),
    )
    token_collector = TokensCollector(
        token_price_collector=token_price_collector,
    )

    await asyncio.gather(token_collector.run(), token_price_collector.run())

asyncio.run(main())
