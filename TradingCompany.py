import random

class Trader:
    
    def __init__(self, trading_company):
        self.trader = []
        self.trading_company = trading_company
        
    def add_trader(self, trader):
        self.trader.append(trader)
        
    def return_details(self):
        ret = {
            "Trader" : random.choice(self.trader),
            "Company" : self.trading_company
        }
        
        return ret
