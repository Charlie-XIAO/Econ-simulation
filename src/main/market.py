class Market:

    def __init__(self, agents, prices):
        self.price_history = {comodity: [prices[comodity]] for comodity in prices.keys()}
        self.agents = agents
    
    def agents_alive(self):
        return [agent for agent in self.agents if agent.alive == 1]
    
    def cur_price(self, comodity):
        return self.price_history[comodity][-1]
    
    def update_price(self):
        # Calculation
        new_price = {"food": 0, "wood": 0, "ore": 0, "metal": 0, "tool": 0}
        for commodity in self.price_history.keys():
            self.price_history[commodity].append(new_price[commodity])

    def distribute(self):
        
