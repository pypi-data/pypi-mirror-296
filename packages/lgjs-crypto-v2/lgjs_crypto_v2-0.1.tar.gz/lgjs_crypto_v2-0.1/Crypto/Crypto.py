# Requirements

import ccxt
import pandas as pd

# Classes

class Settings:
    
    providers = {
        "kraken": 1,
    }
    
    # Default settings
    defaultSettings = {
        "provider": providers["kraken"]
    }

class CryptoSearcher:
    def __init__(self, **kwargs) -> None:
        
        defaultKwargs = Settings.defaultSettings
        kwargs = { **defaultKwargs, **kwargs }
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.loadProvider()
            
    def loadProvider(self):
        match self.provider:
            case 1:
                self.provd = ccxt.kraken()
            
    def searchCrypto(self, symbol, interval="1h", limit=100):
        data = self.provd.fetch_ohlcv(symbol, interval, limit=limit)
        return pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])