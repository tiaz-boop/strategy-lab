class PaperAccount:
    def __init__(self, balance=10000.0):
        self.starting_balance=balance
        self.balance=balance
        self.positions=[]
        self.history=[]

    def apply_pnl(self, pnl):
        self.balance += pnl
        self.history.append(float(pnl))

    def snapshot(self):
        return {"balance":self.balance,"return":self.balance/self.starting_balance-1,
                "positions":len(self.positions),"trades":len(self.history)}
