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
        self.alive = 1
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
        Description: kill the agent and report death due to the specified reason
        """
        self.alive = 0
        print("{} {}: died of {}", self.__class__.__name__, self.id, reason)
    

    def consume(self, comodity:str, n:float) -> None:
        """
        :param comodity: the comodity the agent consumes
        :param n: the number of the specified comodity the agent consumes
        Description: consume the specified number of the specified commodity
        """
        self.inventory[comodity] -= n

    def produce(self, comodity:str, n:float) -> None:
        """
        :param comodity: the comodity the agent produces
        :param n: the number of the specified comodity the agent produces
        Description: produce the specified number of the specified commodity
        """
        assert(self.inventory[comodity] >= n)
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
        if self.inventory["tool"] >= 0.03:
            source = max(self.inventory["wood"], 4)
            self.consume("wood", source)
            self.consume("tool", 0.03)
            self.produce("food", 2 * source)
        else:
            source = max(self.inventory["food"], 4)
            self.consume("wood", source)
            self.produce("food", source)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["food", "ore", "metal"]}
        shortage["wood"] = 4 * UNIT_PER_DAY - self.inventory["wood"]
        shortage["tool"] = 0.03 * UNIT_PER_DAY - self.inventory["tool"]
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["wood", "ore", "metal", "tool"]}
        surplus["food"] = self.inventory["food"] - 8
        return surplus
    
class WoodCutter(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.03:
            self.consume("tool", 0.03)
            self.produce("wood", 4)
        else:
            self.produce("wood", 2)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "ore", "metal"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["tool"] = 0.03 * UNIT_PER_DAY - self.inventory["tool"]
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "ore", "metal", "tool"]}
        surplus["wood"] = self.inventory["wood"]
        return surplus

class Miner(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.05:
            self.consume("tool", 0.05)
            self.produce("ore", 8)
        else:
            self.produce("ore", 4)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "ore", "metal"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["tool"] = 0.05 * UNIT_PER_DAY - self.inventory["tool"]
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "wood", "metal", "tool"]}
        surplus["ore"] = self.inventory["ore"]
        return surplus

class Refiner(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["tool"] >= 0.05:
            source = max(self.inventory["ore"], 2)
            self.consume("ore", source)
            self.consume("tool", 0.05)
            self.produce("metal", source)
        else:
            source = max(self.inventory["ore"], 4) // 2 * 2
            self.consume("ore", source)
            self.produce("metal", source // 2)
    
    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "metal"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["ore"] = 2 * UNIT_PER_DAY - self.inventory["ore"]
        shortage["tool"] = 0.05 * UNIT_PER_DAY - self.inventory["tool"]
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "wood", "ore", "tool"]}
        surplus["metal"] = self.inventory["metal"]
        return surplus
    
class BlackSmith(Agent):

    # Overwrite initialization method
    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    # Overwrite abstract method
    def unit_work(self):
        if self.inventory["metal"] >= 2:
            self.consume("metal", 2)
            self.produce("tool", 1)

    # Overwrite abstract method
    def shortage(self):
        shortage = {comodity: float(0) for comodity in ["wood", "ore", "tool"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["metal"] = 2 * UNIT_PER_DAY - self.inventory["metal"]
        return shortage

    # Overwrite abstract method
    def surplus(self):
        surplus = {comodity: float(0) for comodity in ["food", "wood", "ore", "metal"]}
        surplus["tool"] = self.inventory["tool"]
        return surplus
