from ocean_lib.config import Config
from ocean_lib.ocean.ocean import Ocean

DIDs = {
    "AlgoveraAI/dcgan" : "did:op:E2e123115d5758Dd4C6F434E1c142e72ed8B2820",
}

config = Config('config.ini')
ocean = Ocean(config)

class OceanAlgorithms:
    def __init__(self):
        pass

    def load_algorithm(self, did):
        algorithm = ocean.assets.resolve(DIDs[did])

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
    did = DIDs[algorithm_name]
    algorithm = ocean.assets.resolve(did)
    return algorithm