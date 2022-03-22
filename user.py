from ocean_lib.config import Config
from ocean_lib.models.btoken import BToken #BToken is ERC20
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.currency import from_wei # wei is the smallest denomination of ether e.g. like cents
from ocean_lib.web3_internal.wallet import Wallet

class User():
    def __init__(self, cfg):
        self.config = Config(cfg)
        self.ocean = Ocean(self.config)
        self.wallet = Wallet(self.ocean.web3, private_key="96e91d1c5eb836330b86c7f16ad7da4b0c923bccda1c427a3c70a8372415b715", transaction_timeout=20, block_confirmations=self.config.block_confirmations)

        self.OCEAN_token = BToken(self.ocean.web3, self.ocean.OCEAN_address)
        

    def check_wallet(self):

        print(f"ETH balance = '{from_wei(self.ocean.web3.eth.get_balance(self.wallet.address))}'")
        print(f"OCEAN balance = '{from_wei(self.OCEAN_token.balanceOf(self.wallet.address))}'")