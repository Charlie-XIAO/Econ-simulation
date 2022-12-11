from abc import ABC, abstractmethod

import random

UNIT_PER_DAY = 5

class Agent(ABC):

    def __init__(self, food:float, wood:float, ore:float, metal:float, tool:float):
        """
        :param food: the initial number of food the agent has
        :param wood: the initial number of wood the agent has
        :param ore: the initial number of ore the agent has
        :param metal: the initial number of metal the agent has
        :param tool: the initial number of tool the agent has
        """
        self.id = random.randint(100000, 999999)
        self.inventory = {"food": food, "wood": wood, "ore": ore, "metal": metal, "tool": tool}
    
    @abstractmethod
    def unit_work(self) -> None:
        """
        Description: the working behavior of the agent per unit working time
        """
        pass

    def work(self) -> None:
        """
        Description: the behavior of the agent per day
        """
        for _ in range(UNIT_PER_DAY):
            self.unit_work()
        assert(self.inventory["food"] >= 8)
        self.consume("food", 8)

    def die(self, reason:str) -> None:
        """
        :param reason: the reason that the agent dies
        Description: report death of agent due to the specified reason
        """
        print("{} {}: died of {}".format(self.__class__.__name__, self.id, reason))

    def consume(self, comodity:str, n:float) -> None:
        """
        :param comodity: the comodity the agent consumes
        :param n: the number of the specified comodity the agent consumes
        Description: consume the specified number of the specified commodity
        """
        assert(self.inventory[comodity] >= n)
        self.inventory[comodity] -= n

    def produce(self, comodity:str, n:float) -> None:
        """
        :param comodity: the comodity the agent produces
        :param n: the number of the specified comodity the agent produces
        Description: produce the specified number of the specified commodity
        """
        self.inventory[comodity] += n
    
    @abstractmethod
    def surplus(self) -> dict[str, float]:
        """
        :return: the surplus for each comodity of the agent for exchange
        """
        return {comodity: 0 for comodity in ["food", "wood", "ore", "metal", "tool"]}

    @abstractmethod
    def shortage(self) -> dict[str, float]:
        """
        :return: the shortage of each comodity of the agent to exchange
        """
        return {comodity: 0 for comodity in ["food", "wood", "ore", "metal", "tool"]}

class Farmer(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)

    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.2:
            # Produce 7 food, consume 4 wood, abrade 0.2 tool
            source = min(self.inventory["wood"], 4)
            self.consume("wood", source)
            self.consume("tool", 0.2)
            self.produce("food", 1.75 * source)
        else:
            # Produce 4 food, consume 4 wood
            source = min(self.inventory["wood"], 4)
            self.consume("wood", source)
            self.produce("food", source)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["food", "ore", "metal"]}
        shortage["wood"] = max(4 * UNIT_PER_DAY - self.inventory["wood"], 0)
        shortage["tool"] = max(0.2 * UNIT_PER_DAY - self.inventory["tool"], 0)
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["wood", "ore", "metal", "tool"]}
        surplus["food"] = max(self.inventory["food"] - 8, 0)
        return surplus
    
class WoodCutter(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.2:
            # Produce 4 wood, abrade 0.2 tool
            self.consume("tool", 0.2)
            self.produce("wood", 4)
        else:
            # Produce 2 wood
            self.produce("wood", 2)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "ore", "metal"]}
        shortage["food"] = max(8 - self.inventory["food"], 0)
        shortage["tool"] = max(0.2 * UNIT_PER_DAY - self.inventory["tool"], 0)
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "ore", "metal", "tool"]}
        surplus["wood"] = max(self.inventory["wood"], 0)
        return surplus

class Miner(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.3:
            # Produce 3 ore, abrade 0.3 tool
            self.consume("tool", 0.3)
            self.produce("ore", 3)
        else:
            # Produce 1 ore
            self.produce("ore", 1)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "ore", "metal"]}
        shortage["food"] = max(8 - self.inventory["food"], 0)
        shortage["tool"] = max(0.3 * UNIT_PER_DAY - self.inventory["tool"], 0)
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "wood", "metal", "tool"]}
        surplus["ore"] = max(self.inventory["ore"], 0)
        return surplus

class Refiner(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.2:
            # Produce 2 metal, consume 4 ore, abrade 0.2 tool
            source = min(self.inventory["ore"], 4)
            self.consume("ore", source)
            self.consume("tool", 0.2)
            self.produce("metal", 0.5 * source)
        else:
            # Produce 1 metal, consume 4 ore
            source = min(self.inventory["ore"], 4)
            self.consume("ore", source)
            self.produce("metal", 0.25 * source)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "metal"]}
        shortage["food"] = max(8 - self.inventory["food"], 0)
        shortage["ore"] = max(4 * UNIT_PER_DAY - self.inventory["ore"], 0)
        shortage["tool"] = max(0.2 * UNIT_PER_DAY - self.inventory["tool"], 0)
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "wood", "ore", "tool"]}
        surplus["metal"] = max(self.inventory["metal"], 0)
        return surplus
    
class BlackSmith(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        source = min(self.inventory["metal"], 1.2)
        self.consume("metal", source)
        self.produce("tool", 0.68 * source)

    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "ore", "tool"]}
        shortage["food"] = max(8 - self.inventory["food"], 0)
        shortage["metal"] = max(1.2 * UNIT_PER_DAY - self.inventory["metal"], 0)
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "wood", "ore", "metal"]}
        surplus["tool"] = max(self.inventory["tool"], 0)
        return surplus
