from abc import ABC, abstractmethod
from agent import *

import random
import numpy as np

class Market(ABC):

    def __init__(self, agents:list[Agent], prices:dict[str, float]) -> None:
        """
        :param agents: the list of agents
        :param prices: the dictionary with keys as comodities and values as the corresponding initial prices
        """
        self.price_history = {comodity: [prices[comodity]] for comodity in prices.keys()}
        self.agents = agents
    
    def cur_price(self, comodity:str) -> float:
        """
        :param commodity: the commodity to obtain the current price
        :return: the current price of the specified commodity
        """
        return self.price_history[comodity][-1]
    
    def update_price_history(self, prices:dict[str, float]) -> None:
        """
        Description: updates the price history
        :param prices: the dictionary with keys as commodities and values as the corresponding prices to update
        """
        for comodity in self.price_history.keys():
            self.price_history[comodity].append(prices[comodity])

    def demand_matrix(self) -> list[np.ndarray]:
        """
        :return: the demand matrix, with each commodity (food, wood, ore, metal, tool) as a column and each agent as a row
        """
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
    
    def total_demand(self, comodity:str) -> float:
        """
        :param comodity: the commodity to obtain the total demand
        :return: the total demand of the specified commodity
        """
        return sum([agent.shortage()[comodity] for agent in self.agents])
    
    def supply_matrix(self) -> list[np.ndarray]:
        """
        :return: the supply matrix, with each commodity (food, wood, ore, metal, tool) as a column and each agent as a row
        """
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

    def total_supply(self, comodity:str) -> float:
        """
        :param comodity: the commodity to obtain the total supply
        :return: the total supply of the specified commodity
        """
        return sum([agent.surplus()[comodity] for agent in self.agents])
    
    def take_supply(self) -> dict[str, float]:
        """
        Description: takes away all the supplies from all the agents
        """
        total_supply = {comodity: float(0) for comodity in ["food", "wood", "ore", "metal", "tool"]}
        for agent in self.agents:
            for comodity in agent.surplus().keys():
                if agent.surplus()[comodity] > 0:
                    total_supply[comodity] += agent.inventory[comodity]
                    agent.inventory[comodity] = 0
        return total_supply

    def satisfy_demand(self, r:np.ndarray) -> None:
        """
        Description: gives each agent some commodities according to the assigned intensity and their demand
        :param r: the intensity assigned for each agent (same order as in `self.agents`)
        """
        for agent in self.agents:
            for comodity in agent.shortage().keys():
                agent.inventory[comodity] += agent.shortage()[comodity] * r
    
    @abstractmethod
    def update_price(self) -> None:
        """
        Description: updates the price with some market strategy, and update the price history
        # Walrasian: solve ODE with constraint
        # Supply and demand: adjust by some percentage of the ratio of supply versus demand
        """
        pass

    @abstractmethod
    def distribute(self) -> None:
        """
        Description: distributes the supply and demand with some market strategy, according to the updated price
        # Walrasian: obtain r with ODE result, take away everything one produces, give r times everything one demands
        # Supply and demand: take away everything one produces, give each agent corresponding money, with some random order,
        #                    the agents use those money to buy as many times everything they demand as they can
        """
        pass

class WalrasianMarket(Market):

    # Overwrite initialization method
    def __init__(self, agents, prices):
        super().__init__(agents, prices)
    
    # Overwrite abstract method
    def update_price(self):
        pass

    # Overwrite abstract method
    def distribute(self):
        pass

class SupplyDemandMarket(Market):

    # Overwrite initialization method
    def __init__(self, agents, prices):
        super().__init__(agents, prices)
    
    # Overwrite abstract method
    def update_price(self):
        # Create a new price based on the total supply and demand
        new_prices = {comodity: float(0) for comodity in ["food", "wood", "ore", "metal", "tool"]}
        for comodity in new_prices.keys():
            ratio = self.total_demand(comodity) / self.total_supply(comodity)
            if ratio > 1:
                new_prices[comodity] += self.cur_price(comodity) * ratio * 0.03
            else:
                new_prices[comodity] -= self.cur_price(comodity) / ratio * 0.03
        # Update the price history and take away all the supplies from all agents
        self.update_price_history(new_prices)
        self.take_supply()

    # Overwrite abstract method
    def distribute(self):
        # Distribute wealth to each agent based on the current prices and their surplus,
        # meanwhile collecting the commodities they are trying to sell
        wealth = []
        collected = {comodity: 0 for comodity in ["food", "wood", "ore", "metal", "tool"]}
        prices = [self.cur_price(comodity) for comodity in ["food", "wood", "ore", "metal", "tool"]]
        for agent in self.agents:
            surpluses = []
            for comodity in ["food", "wood", "ore", "metal", "tool"]:
                surpluses.append(agent.surplus()[comodity])
                collected[comodity] += surpluses[-1]
            wealth.append(np.dot(prices, surpluses))
        # Each agent tries to spend all of their wealth for what they demand (in certain proportion),
        # note that the last ones to trade may not get what they want, meaning that they receive less value that they give
        order = list(range(len(self.agents)))
        random.shuffle(order)
        for i in order:
            cur_agent = self.agents[i]
            demands = [cur_agent.shortage()[comodity] for comodity in ["food", "wood", "ore", "metal", "tool"]]
            r = wealth[i] / np.dot(prices, demands)
            for comodity in ["food", "wood", "ore", "metal", "tool"]:
                exchange_amount = min(r * cur_agent.shortage()[comodity], collected[comodity])
                cur_agent.inventory[comodity] += exchange_amount
                collected[comodity] -= exchange_amount

