class LeftBrainPredictor:
    def __init__(self):
        self.symbol = ""
        
    def predict(self, df):
        return {"ml_signal": "HOLD", "confidence": 50, "reason": "Not enough data"}
