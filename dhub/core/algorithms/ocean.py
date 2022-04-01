from dotenv import load_dotenv
from ocean_lib.common.agreements.service_types import ServiceTypes
from ocean_lib.config import Config
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.services.service import Service
from ocean_lib.web3_internal.currency import to_wei
from ocean_lib.web3_internal.wallet import Wallet
import os
from ..utils import convert_github_link

catalogue = {
    "AlgoveraAI/dcgan" : "did:op:E2e123115d5758Dd4C6F434E1c142e72ed8B2820",
}

load_dotenv()

config = Config('config.ini')
ocean = Ocean(config)
wallet = Wallet(ocean.web3, os.environ.get("PRIVATE_KEY"), transaction_timeout=20, block_confirmations=config.block_confirmations)

def get_algorithms():
    return list(catalogue.keys())

class OceanAlgorithms:
    def __init__(self):
        pass

    def load_algorithm(self, did):
        algorithm = ocean.assets.resolve(catalogue[did])

        print(f"Alg token info = '{algorithm.values['dataTokenInfo']}'")
        print(f"Alg name = '{algorithm.metadata['main']['name']}'")

        return OceanAlgorithm(algorithm)

    def ls(self):
        for DID in DIDs:
            print(DID)

    
class OceanAlgorithm:
    def __init__(self, algorithm):
        self.algorithm = algorithm

def load_algorithm_from_ocean(algorithm_name):
    did = catalogue[algorithm_name]
    algorithm = ocean.assets.resolve(did)
    return algorithm

def create_model_token(model_name, model_url):
    model_token = ocean.create_data_token(model_name, model_name, from_wallet=wallet)
    model_token.mint(wallet.address, to_wei(100), wallet)

    date_created = "2019-12-28T10:55:11Z"
    metadata =  {
        "main": {
            "type": "dataset", "name": "branin", "author": "Trent",
            "license": "CC0: Public Domain", "dateCreated": date_created,
            "files": [{"index": 0, "contentType": "text/text",
                "url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff"}]}
    }
    service_attributes = {
            "main": {
                "name": "dataAssetAccessServiceAgreement",
                "creator": alice_wallet.address,
                "timeout": 3600 * 24,
                "datePublished": date_created,
                "cost": 1.0, # <don't change, this is obsolete>
            }
        }

    #Publish metadata and service attributes on-chain.
    # The service urls will be encrypted before going on-chain.
    # They're only decrypted for datatoken owners upon consume.
    from ocean_lib.data_provider.data_service_provider import DataServiceProvider
    from ocean_lib.common.agreements.service_factory import ServiceDescriptor

    service_endpoint = DataServiceProvider.get_url(ocean.config)
    download_service = ServiceDescriptor.access_service_descriptor(service_attributes, service_endpoint)
    assert alice_wallet.web3.eth.get_balance(alice_wallet.address) > 0, "need ETH"
    asset = ocean.assets.create(
        metadata,
        alice_wallet,
        service_descriptors=[download_service],
        data_token_address=token_address)
    assert token_address == asset.data_token_address

    return asset


def create_algorithm_ocean(algorithm_name, algorithm_url):

    algorithm_url = convert_github_link(algorithm_url)

    algorithm_token = ocean.create_data_token(algorithm_name, algorithm_name, wallet, blob=ocean.config.metadata_cache_uri)
    algorithm_token.mint(wallet.address, to_wei(100), wallet)

    image = "algovera/algo_dockers" 
    tag = "generative-art"
    author = "AlgoveraAI"

    ALG_metadata =  {
        "main": {
            "type": "algorithm",
            "algorithm": {
                "language": "python",
                "format": "docker-image",
                "version": "0.1",
                "container": {
                "entrypoint": "python $ALGO",
                "image": image,
                "tag": tag
                }
            },
            "files": [
        {
            "url": algorithm_url,
            "index": 0,
            "contentType": "text/text",
        }
        ],
        "name": algorithm_name, "author": author, "license": "CC0",
        "dateCreated": "2021-12-02T15:00:00Z"
        }
    }

    ALG_service_attributes = {
            "main": {
                "name": "ALG_dataAssetAccessServiceAgreement",
                "creator": wallet.address,
                "timeout": 3600 * 24,
                "datePublished": "2020-01-28T10:55:11Z",
                "cost": 1.0, # <don't change, this is obsolete>
            }
        }

    provider_url = DataServiceProvider.get_url(ocean.config) # returns "http://localhost:8030"

    # Calc ALG service access descriptor. We use the same service provider as DATA
    ALG_access_service = Service(
        service_endpoint=provider_url,
        service_type=ServiceTypes.CLOUD_COMPUTE,
        attributes=ALG_service_attributes
    )

    # Publish metadata and service info on-chain
    ALG_ddo = ocean.assets.create(
        metadata=ALG_metadata, 
        publisher_wallet=wallet,
        services=[ALG_access_service],
        data_token_address=algorithm_token.address)

    return ALG_ddo