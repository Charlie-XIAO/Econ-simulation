from abc import ABC, abstractmethod
from . import agent as _agent

import random
import numpy as np
import scipy.linalg as linalg
import scipy.optimize as optimize
import matplotlib.pyplot as plt

class Market(ABC):

    def __init__(self, agents:list[_agent.Agent], prices:dict[str, float]) -> None:
        """
        :param agents: the list of agents
        :param prices: the dictionary with keys as comodities and values as the corresponding initial prices
        """
        self.price_history = {comodity: [prices[comodity]] for comodity in prices.keys()}
        self.agents = agents
    
    def simulate(self, n, verbose=False) -> None:
        """
        :param n: the number of exchange days to simulate, or simulate until all agents die]
        :param verbose: whether to print verbose to stdout <DEFAULT: False>
        Description: simulate the market system for a few exchange days
        """
        for _ in range(n):
            agents_alive = []
            for agent in self.agents:
                if agent.inventory["food"] < 8:
                    agent.die("starvation")
                else:
                    agents_alive.append(agent)
            self.agents = agents_alive
            if len(self.agents) == 0:
                break
            for agent in self.agents:
                agent.work()
                if verbose: print("AFTER WORKING:", agent.__class__.__name__, agent.inventory)
            if verbose: print()
            self.update_price()
            self.distribute()
            # Debuging module
            for agent in self.agents:
                if verbose: print("AFTER DISTRIBUTION:", agent.__class__.__name__, agent.inventory)
            if verbose: print()
    
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
        :return: the total supply of all agents for each comodity
        Description: takes away all the supply of all agents
        """
        total_supply = {comodity: float(0) for comodity in ["food", "wood", "ore", "metal", "tool"]}
        for agent in self.agents:
            surpluses = agent.surplus()
            for comodity in surpluses.keys():
                total_supply[comodity] += surpluses[comodity]
                agent.inventory[comodity] -= surpluses[comodity]
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
        - Walrasian: solve ODE with constraint
        - Supply and demand: adjust by some percentage of the ratio of supply versus demand
        """
        pass

    @abstractmethod
    def distribute(self) -> None:
        """
        Description: distributes the supply and demand with some market strategy, according to the updated price
        - Walrasian: obtain r with ODE result, take away everything one produces, give r times everything one demands
        - Supply and demand: take away everything one produces, give each agent corresponding money, with some random order,
                             the agents use those money to buy as many times everything they demand as they can
        """
        pass
    
    def cur_wealth(self) -> list[float]:
        """
        :return: the list of wealth of the agents (same order as in `self.agents`)
        """
        return [sum([agent.inventory[comodity] * self.cur_price(comodity) for comodity in agent.inventory.keys()]) for agent in self.agents]
    
    def gini(self) -> float:
        """
        :return: the Gini coefficient of the current population (agents)
        """
        wealths = np.array(self.cur_wealth())
        total = sum([np.sum(np.abs(xi - wealths[i:])) for i, xi in enumerate(wealths[:-1], 1)])
        return total / (len(wealths) ** 2 * np.mean(wealths))
    
    def plot_price_history(self, save=False) -> None:
        """
        :param save: whether to save the plot <DEFAULT: False>
        Description: plots the price history of each comodity and saves the plot if desired
        """
        plt.title("Price history")
        plt.xlabel("Number of exchanges")
        plt.ylabel("Price")
        for comodity in self.price_history.keys():
            plt.plot(self.price_history[comodity], label=comodity)
        plt.legend()
        if save:
            plt.savefig("price_history.png")
        plt.show()

class WalrasianMarket(Market):

    # Overwrite initialization method
    def __init__(self, agents, prices):
        super().__init__(agents, prices)
    
    # Overwrite abstract method
    def update_price(self):
        # Walrasian excess demand
        """
        这里是不是有问题 我大概改了一下 但是我也不知道改的对不对 还是得你自己再看
        而且我看A和B还没有放进去 A和B我给你写了函数了 就是self.demand_matrix()和self.supply_matrix()
        函数的返回类型你往上翻就有了 应该是list of np.ndarray (其实是list of np.array)
        """
        def walras(p, A, B):
            e = np.zeros(len(self.agents))
            for j in range(len(self.agents)):
                e[j] = np.sum(np.dot(B[:,j], p) / np.dot(A[:,j], p) * A[:j] - B[:,j])
            return e * p
        # Constraint functions
        def f1(p): return p[0]            
        def f2(p): return p[1]
        def f3(p): return p[2]
        def f4(p): return p[3]
        def f5(p): return p[4]
        constraints = [
            {"type": "ineq", "fun": f1},
            {"type": "ineq", "fun": f2},
            {"type": "ineq", "fun": f3},
            {"type": "ineq", "fun": f4},
            {"type": "ineq", "fun": f5},
        ]
        # Using the previous price as the last guess
        p0 = [self.cur_price(comodity) for comodity in ["food", "wood", "ore", "metal", "tool"]]
        result = optimize.minimize(walras, p0, constraints=constraints)
        # Update the price history
        ref_list = ["food", "wood", "ore", "metal", "tool"]
        new_prices = {ref_list[i]: result[i] for i in range(len(ref_list))}
        self.update_price_history(new_prices)

    # Overwrite abstract method
    def distribute(self):
        """
        这里我也稍微改了几笔 你看看是不是你本来想写的意思
        """
        self.take_supply()
        A = self.demand_matrix()
        B = self.supply_matrix()
        p = [self.cur_price(comodity) for comodity in ["food", "wood", "ore", "metal", "tool"]]
        for i in range(len(self.agents)):
            cur_agent = self.agents[i]
            r = np.sum(B[i] * p) / np.sum(A[i] * p) * A[i] - B[i]
            for comodity in ["food", "wood", "ore", "metal", "tool"]:
                cur_agent.inventory[comodity] += cur_agent.shortage()[comodity] * r

class SupplyDemandMarket(Market):

    # Overwrite initialization method
    def __init__(self, agents, prices):
        super().__init__(agents, prices)
    
    # Overwrite abstract method
    def update_price(self):
        # Create a new price based on the total supply and demand
        new_prices = {comodity: self.cur_price(comodity) for comodity in ["food", "wood", "ore", "metal", "tool"]}
        for comodity in new_prices.keys():
            ratio = (self.total_demand(comodity) + 0.001) / (self.total_supply(comodity) + 0.001)
            if ratio > 1:
                new_prices[comodity] += min(self.cur_price(comodity) * ratio * 0.1, self.cur_price(comodity) * 0.05)
            else:
                new_prices[comodity] -= min(self.cur_price(comodity) / ratio * 0.1, self.cur_price(comodity) * 0.05)
        # Update the price history
        self.update_price_history(new_prices)

    # Overwrite abstract method
    def distribute(self):
        # Distribute wealth to each agent based on the current prices and their surplus,
        # meanwhile collecting the commodities they are trying to sell
        wealth = []
        collected = {comodity: float(0) for comodity in ["food", "wood", "ore", "metal", "tool"]}
        prices = [self.cur_price(comodity) for comodity in ["food", "wood", "ore", "metal", "tool"]]
        for agent in self.agents:
            surpluses = agent.surplus()
            for comodity in ["food", "wood", "ore", "metal", "tool"]:
                collected[comodity] += surpluses[comodity]
            wealth.append(np.dot(prices, [surpluses[comodity] for comodity in ["food", "wood", "ore", "metal", "tool"]]))
        self.take_supply()
        # Each agent tries to spend all of their wealth for what they demand (in certain proportion),
        # note that the last ones to trade may not get what they want, meaning that they receive less value that they give
        order = list(range(len(self.agents)))
        random.shuffle(order)
        for i in order:
            cur_agent = self.agents[i]
            demands = [cur_agent.shortage()[comodity] for comodity in ["food", "wood", "ore", "metal", "tool"]]
            if np.dot(prices, demands) > 0.01:
                r = wealth[i] / np.dot(prices, demands)
                for comodity in ["food", "wood", "ore", "metal", "tool"]:
                    exchange_amount = min(r * cur_agent.shortage()[comodity], collected[comodity])
                    cur_agent.inventory[comodity] += exchange_amount
                    collected[comodity] -= exchange_amount

