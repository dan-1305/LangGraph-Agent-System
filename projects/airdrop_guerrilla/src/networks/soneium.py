from .evm_base import EVMBase

class SoneiumNetwork(EVMBase):
    """Tích hợp Soneium Minato Testnet (Layer 2 Sony)"""
    def __init__(self, private_key: str, proxy_url: str = ""):
        rpc_urls = [
            "https://rpc.minato.soneium.org/",
            "https://soneium-minato.rpc.thirdweb.com"
        ]
        chain_id = 1946
        symbol = "ETH"
        explorer_url = "https://soneium-minato.blockscout.com"
        
        super().__init__("Soneium", rpc_urls, chain_id, private_key, symbol, explorer_url, proxy_url)
