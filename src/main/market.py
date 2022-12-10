from abc import ABC, abstractmethod

import numpy as np

class Market(ABC):

    def __init__(self, agents, prices):
        self.price_history = {comodity: [prices[comodity]] for comodity in prices.keys()}
        self.agents = agents
    
    def agents_alive(self):
        return [agent for agent in self.agents if agent.alive == 1]
    
    def cur_price(self, comodity):
        return self.price_history[comodity][-1]

    def demand_matrix(self):
        demand_matrix = []
        for agent in self.agents:
            demand_matrix.append(np.array(
                agent.shortage()["food"],
                agent.shortage()["wood"],
                agent.shortage()["ore"],
                agent.shortage()["metal"],
                agent.shortage()["tool"],
            ))
        return demand_matrix
    
    def supply_matrix(self):
        supply_matrix = []
        for agent in self.agents:
            supply_matrix.append(np.array(
                agent.surplus()["food"],
                agent.surplus()["wood"],
                agent.surplus()["ore"],
                agent.surplus()["metal"],
                agent.surplus()["tool"],
            ))
        return supply_matrix
    
    def take_all_production(self):
        pass

    def satisfy_demand(self, r):
        pass
    
    @abstractmethod
    def update_price(self) -> None:
        # Walrasian: solve ODE with constraint
        # Supply and demand: adjust by some percentage of the ratio of supply versus demand
        pass

    @abstractmethod
    def distribute(self) -> None:
        # Walrasian: obtain r with ODE result, take away everything one produces, give r times everything one demands
        # Supply and demand: take away everything one produces, give each agent corresponding money, with some random order,
        #                    the agents use those money to buy as many times everything they demand as they can
        pass

class WalrasianMarket(Market):

    def __init__(self, agents, prices):
        super().__init__(agents, prices)
    
    def update_price(self):
        pass

    def distribute(self):
        pass

class SupplyDemandMarket(Market):

    def __init__(self, agents, prices):
        super().__init__(agents, prices)
    
    def update_price(self):
        pass

    def distribute(self):
        pass
