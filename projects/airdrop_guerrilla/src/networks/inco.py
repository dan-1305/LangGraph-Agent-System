from .evm_base import EVMBase

class IncoNetwork(EVMBase):
    """Tích hợp Inco Network Testnet (Modular Confidential L1)"""
    def __init__(self, private_key: str, proxy_url: str = ""):
        rpc_urls = [
            "https://testnet.inco.org/",
            "https://validator.testnet.inco.org/",
            "https://inco-gentry-rpc.dataseed.org",
            "https://rpc-testnet.inco.org/"
        ]
        chain_id = 9090
        symbol = "INCO"
        explorer_url = "https://explorer.testnet.inco.org"
        
        super().__init__("Inco", rpc_urls, chain_id, private_key, symbol, explorer_url, proxy_url)
