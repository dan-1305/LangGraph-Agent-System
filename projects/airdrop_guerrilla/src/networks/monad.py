from .evm_base import EVMBase

class MonadNetwork(EVMBase):
    """Tích hợp Monad Testnet (Layer 1 EVM Parallel)"""
    def __init__(self, private_key: str, proxy_url: str = ""):
        rpc_urls = [
            "https://testnet-rpc.monad.xyz/",
            "https://monad-testnet.rpc.thirdweb.com", 
            "https://monad-testnet.drpc.org"
        ]
        chain_id = 10143
        symbol = "MON"
        explorer_url = "https://testnet.monadexplorer.com"
        
        super().__init__("Monad", rpc_urls, chain_id, private_key, symbol, explorer_url, proxy_url)
