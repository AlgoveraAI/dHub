

DIDs = {
    "AlgoveraAI/dcgan" : "did:op:E2e123115d5758Dd4C6F434E1c142e72ed8B2820",
}

class Algorithms:
    def __init__(self, cfg):
        self.cfg = cfg

    def load_algorithm(self, did):
        algorithm = self.cfg.ocean.assets.resolve(DIDs[did])

        print(f"Alg token info = '{algorithm.values['dataTokenInfo']}'")
        print(f"Alg name = '{algorithm.metadata['main']['name']}'")

        return Algorithm(algorithm)

    def ls(self):
        for DID in DIDs:
            print(DID)

    
class Algorithm:
    def __init__(self, algorithm):
        self.algorithm = algorithm