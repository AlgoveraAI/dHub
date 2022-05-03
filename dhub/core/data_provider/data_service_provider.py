import base64
from datetime import datetime
import hashlib
import json
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.web3_internal.wallet import Wallet
import requests
from requests.models import PreparedRequest, Response
from typing import Any, Dict, List, Optional, Tuple, Union
from web3.main import Web3

class DataServiceProvider(DataServiceProvider):

    def decrypt(
        objects_to_decrypt: Union[list, str, bytes], 
        provider_uri: str,
        consumer_wallet: Wallet,
    ) -> Response:
        if isinstance(objects_to_decrypt, list):
            data_items = list(map(lambda file: file.to_dict(), objects_to_decrypt))
            data = json.dumps(data_items, separators=(",", ":"))
            objects_to_decrypt = data.encode("utf-8")
        elif isinstance(objects_to_decrypt, str):
            objects_to_decrypt = objects_to_decrypt.encode("utf-8")
        else:
            objects_to_decrypt = objects_to_decrypt

        ddo_hash_hexstr = Web3.toHex(hashlib.sha256(objects_to_decrypt).digest())

        chain_id = 4
        nonce = str(int(datetime.utcnow().timestamp()))

        _, signature = DataServiceProvider.sign_message(
            consumer_wallet, f"{consumer_wallet.address}{chain_id}{nonce}"
        )

        payload = {
            # "transactionId": txid,
            "chainId": chain_id,
            "decrypterAddress": consumer_wallet.address,
            # "dataNftAddress": contract_address,
            "encryptedDocument": objects_to_decrypt.decode('utf-8'),
            'flags': 2,
            "documentHash": ddo_hash_hexstr,
            "signature": signature,
            "nonce": nonce,
        }

        _, decrypt_endpoint = DataServiceProvider.build_decrypt_endpoint(provider_uri)

        response = DataServiceProvider._http_method(
            "post",
            decrypt_endpoint,
            data=json.dumps(payload),
            headers={"content-type": "application/json"},
        )

        # if not response or not hasattr(response, "status_code"):
        #     raise DataProviderException(
        #         f"Failed to get a response for request: encryptEndpoint={encrypt_endpoint}, payload={payload}, response is {response}"
        #     )

        # if response.status_code != 201:
        #     msg = (
        #         f"Encrypt file urls failed at the encryptEndpoint "
        #         f"{encrypt_endpoint}, reason {response.text}, status {response.status_code}"
        #     )
        #     logger.error(msg)
        #     raise OceanEncryptAssetUrlsError(msg)

        # logger.info(
        #     f"Asset urls encrypted successfully, encrypted urls str: {response.text},"
        #     f" encryptedEndpoint {encrypt_endpoint}"
        # )

        return response

    def build_decrypt_endpoint(provider_uri: str) -> Tuple[str, str]:
        return DataServiceProvider.build_endpoint("decrypt", provider_uri)