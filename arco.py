import sys
from aiohttp import Payload
from mnemonic import Mnemonic
from aptos_sdk.account_address import AccountAddress
from typing import Optional

from utils import PublicKeyUtils
from aptos_sdk.account import Account
from aptos_sdk.client import FaucetClient, RestClient
from aptos_sdk.bcs import Serializer

from aptos_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from aptos_sdk.type_tag import StructTag, TypeTag
import json,os
import yaml

FAUCET_URL = 'https://faucet.devnet.aptoslabs.com' #'https://faucet.testnet.aptoslabs.com'
NODE_URL = 'https://fullnode.devnet.aptoslabs.com/v1' #'https://fullnode.testnet.aptoslabs.com/v1'
save_path = os.path.join('./wallets')
class ArcoClient(RestClient):
    contract_address = "0x5ff046fff9f70bb193cfc287dd92468bc4b5af88920552614b0e5472cbce8e0c"

    def lend(self, sender: Account, num: int) -> str:
        payload = EntryFunction.natural(
            f"{self.contract_address}::arc_protocol",
            "lend",
            [TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))],
            [TransactionArgument(int(num * 100000000), Serializer.u64)],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)
    
    def borrow(self, sender: Account, num: int) -> str:
        payload = EntryFunction.natural(
            f"{self.contract_address}::arc_protocol",
            "borrow",
            [TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))],
            [TransactionArgument(int(num * 100000000), Serializer.u64)],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)
    
    def repay(self, sender: Account, num: int) -> str:
        payload = EntryFunction.natural(
            f"{self.contract_address}::arc_protocol",
            "repay",
            [TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))],
            [TransactionArgument(int(num * 100000000), Serializer.u64)],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

    def withdraw(self, sender: Account, num: int) -> str:
        payload = EntryFunction.natural(
            f"{self.contract_address}::arc_protocol",
            "withdraw",
            [TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))],
            [TransactionArgument(int(num * 100000000), Serializer.u64)],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)
    
    def claim(self, sender: Account) -> str:
        payload = EntryFunction.natural(
            f"{self.contract_address}::arc_protocol",
            "claim",
            [],
            [],
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

c = 0 
while True:
    try:
        mnemonic_alice = Mnemonic('english').generate()
        temp_obj = {}
        print(f'mnemonic_alice is: {mnemonic_alice}')
        temp_obj['mnemonic'] = mnemonic_alice

        pt_alice = PublicKeyUtils(mnemonic_alice)


        alice = Account.load_key(pt_alice.private_key.hex())



        print("\n=== Addresses ===")
        print(f"Alice addresss: {alice.address()}")
        print(f"Alice public_key: {alice.public_key()}")
        print(f"Alice private_key: 0x{pt_alice.private_key.hex()}")
        temp_obj['addresss'] = str(alice.address())
        temp_obj['public_key'] = str(alice.public_key())
        temp_obj['private_key'] = f"0x{pt_alice.private_key.hex()}"


        rest_client = RestClient(NODE_URL)
        faucet_client = FaucetClient(FAUCET_URL, rest_client)  # <:!:section_1


        #:!:>section_3
        for i in range(1):
            faucet_client.fund_account(alice.address(), 100000000)

        print("\n=== Initial Balances ===")
        #:!:>section_4
        print(f"Alice: {rest_client.account_balance(alice.address())}")

        
        rest_arco_client = ArcoClient(NODE_URL)

        txn_hash_lend = rest_arco_client.lend(alice, 0.8)
        rest_arco_client.wait_for_transaction(txn_hash_lend)

        txn_hash_borrow = rest_arco_client.borrow(alice, 0.3)
        rest_arco_client.wait_for_transaction(txn_hash_borrow)

        txn_hash_repay = rest_arco_client.repay(alice, 0.1)
        rest_arco_client.wait_for_transaction(txn_hash_repay)

        txn_hash_withdraw = rest_arco_client.withdraw(alice, 0.1)
        rest_arco_client.wait_for_transaction(txn_hash_withdraw)

        txn_hash_claim = rest_arco_client.claim(alice)
        rest_arco_client.wait_for_transaction(txn_hash_claim)

        print(txn_hash_lend, txn_hash_borrow, txn_hash_repay, txn_hash_withdraw, txn_hash_claim)
        temp_obj['txn_hash_lend'] = txn_hash_lend
        temp_obj['txn_hash_borrow'] = txn_hash_borrow
        temp_obj['txn_hash_repay'] = txn_hash_repay
        temp_obj['txn_hash_withdraw'] = txn_hash_withdraw
        temp_obj['txn_hash_claim'] = txn_hash_claim
        print(temp_obj)
        with open(os.path.join(save_path, str(alice.address())+'.json'), 'w') as f:
            json.dump(temp_obj, f)

        with open(os.path.join(save_path, str(alice.address())+'.yaml'), 'w') as f:
            yaml.dump(temp_obj, f, allow_unicode=True)
        print(f"=========== done count {c} ===========")
        c+=1
    except Exception as e:
        print(e)

# import ipdb;ipdb.set_trace()