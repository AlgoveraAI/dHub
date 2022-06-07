from dhub.core.storage_provider.storage_provider import StorageProvider
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.ocean.ocean_assets import OceanAssets
from ocean_lib.services.service import Service
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.web3_internal.currency import to_wei
from pathlib import Path

from ..utils import convert_github_link

class Algorithm():

    def create(user, path, algorithm_url):

        algorithm_name = Path(algorithm_url).parent.stem
        algorithm_url = convert_github_link(algorithm_url)

        # Publish the algorithm NFT token
        ALGO_nft_token = user.ocean.create_erc721_nft("NFTToken1", "NFT1", user.wallet)
        print(f"ALGO_nft_token address = '{ALGO_nft_token.address}'")

        # Publish the datatoken
        ALGO_datatoken = ALGO_nft_token.create_datatoken(
            template_index=1,
            name="Datatoken 1",
            symbol="DT1",
            minter=user.wallet.address,
            fee_manager=user.wallet.address,
            publish_market_order_fee_address=ZERO_ADDRESS,
            publish_market_order_fee_token=user.ocean.OCEAN_address,
            cap=ocean.to_wei(100000),
            publish_market_order_fee_amount=0,
            bytess=[b""],
            from_wallet=user.wallet,
        )
        print(f"ALGO_datatoken address = '{ALGO_datatoken.address}'")

        # Specify metadata and services
        ALGO_date_created = "2021-12-28T10:55:11Z"
        image = "algovera/algo_dockers" 
        tag = "dhub"
        author = "AlgoveraAI"
        description = "description"

        ALGO_metadata = {
            "created": ALGO_date_created,
            "updated": ALGO_date_created,
            "description": description,
            "name": algorithm_name,
            "type": "algorithm",
            "author": author,
            "license": "CC0: PublicDomain",
            "algorithm": {
                "language": "python",
                "format": "docker-image",
                "version": "0.1",
                "container": {
                    "entrypoint": "python $ALGO",
                    "image": image,
                    "tag": tag,
                    "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
                },
            }
        }

        # ocean.py offers multiple file types, but a simple url file should be enough for this example
        ALGO_url_file = UrlFile(
            url=algorithm_url
        )

        # Encrypt file(s) using provider
        ALGO_encrypted_files = user.ocean.assets.encrypt_files([ALGO_url_file])

        # Publish metadata and service info on-chain
        ALGO_asset = user.ocean.assets.create(
            metadata=ALGO_metadata,
            publisher_wallet=user.wallet,
            encrypted_files=ALGO_encrypted_files,
            erc721_address=ALGO_nft_token.address,
            deployed_erc20_tokens=[ALGO_datatoken],
        )

        print(f"ALGO_asset did = '{ALGO_asset.did}'")

        return ALGO_asset