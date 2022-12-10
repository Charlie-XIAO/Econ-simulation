from abc import ABC, abstractmethod

import random
import numpy as np

UNIT_PER_DAY = 5

class Agent(ABC):

    def __init__(self, food, wood, ore, metal, tool):
        self.id = random.randint(100000, 999999)
        self.alive = 1
        self.inventory = {"food": food, "wood": wood, "ore": ore, "metal": metal, "tool": tool}

    @abstractmethod
    def unit_work(self) -> None:
        pass

    def work(self):
        for _ in range(UNIT_PER_DAY):
            self.unit_work()
        assert(self.inventory["food"] >= 8)
        self.consume("food", 8)

    def die(self):
        self.alive = 0
        print("{} {}: died of starvation", self.__class__.__name__, self.id)
    

    def consume(self, comodity, n):
        assert(comodity in ["food", "wood", "ore", "metal"])
        self.inventory[comodity] -= n
    
    def has_tool(self):
        return self.inventory["tool"] >= 1
    
    def break_tool(self, prob):
        if (random.random() < prob):
            self.inventory["tool"] -= 1

    def produce(self, comodity, n):
        assert(self.inventory[comodity] >= n)
        self.inventory[comodity] += n
    
    @abstractmethod
    def surplus(self) -> dict:
        return {comodity: 0 for comodity in ["food", "wood", "ore", "metal", "tool"]}

    @abstractmethod
    def shortage(self) -> dict:
        return {comodity: 0 for comodity in ["food", "wood", "ore", "metal", "tool"]}

class Farmer(Agent):

    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)

    def unit_work(self):
        if self.has_tool():
            source = max(self.inventory["wood"], 4)
            self.consume("wood", source)
            self.produce("food", 2 * source)
            self.break_tool(0.03)
        else:
            source = max(self.inventory["food"], 4)
            self.consume("wood", source)
            self.produce("food", source)
    
    def shortage(self):
        shortage = {comodity: 0 for comodity in ["food", "ore", "metal"]}
        shortage["wood"] = 4 * UNIT_PER_DAY - self.inventory["wood"]
        shortage["tool"] = 1 - self.inventory["tool"]
        return shortage

    def surplus(self):
        surplus = {comodity: 0 for comodity in ["wood", "ore", "metal", "tool"]}
        surplus["food"] = self.inventory["food"] - 8
    
class WoodCutter(Agent):

    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    def unit_work(self):
        if self.has_tool():
            self.produce("wood", 4)
            self.break_tool(0.03)
        else:
            self.produce("wood", 2)
    
    def shortage(self):
        shortage = {comodity: 0 for comodity in ["wood", "ore", "metal"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["tool"] = 1 - self.inventory["tool"]
        return shortage

    def surplus(self):
        surplus = {comodity: 0 for comodity in ["food", "ore", "metal", "tool"]}
        surplus["wood"] = self.inventory["wood"]

class Miner(Agent):

    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    def unit_work(self):
        if self.has_tool():
            self.produce("ore", 8)
            self.break_tool(0.05)
        else:
            self.produce("ore", 4)
    
    def shortage(self):
        shortage = {comodity: 0 for comodity in ["wood", "ore", "metal"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["tool"] = 1 - self.inventory["tool"]
        return shortage

    def surplus(self):
        surplus = {comodity: 0 for comodity in ["food", "wood", "metal", "tool"]}
        surplus["ore"] = self.inventory["ore"]

class Refiner(Agent):

    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    def unit_work(self):
        if self.has_tool():
            source = max(self.inventory["ore"], 2)
            self.consume("ore", source)
            self.produce("metal", source)
            self.break_tool(0.05)
        else:
            source = max(self.inventory["ore"], 4) // 2 * 2
            self.consume("ore", source)
            self.produce("metal", source // 2)
        
    def shortage(self):
        shortage = {comodity: 0 for comodity in ["wood", "metal"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["ore"] = 2 * UNIT_PER_DAY - self.inventory["ore"]
        shortage["tool"] = 1 - self.inventory["tool"]
        return shortage

    def surplus(self):
        surplus = {comodity: 0 for comodity in ["food", "wood", "ore", "tool"]}
        surplus["metal"] = self.inventory["metal"]
    
class BlackSmith(Agent):

    def __init__(self, food, wood, ore, metal, tool):
        super().__init__(food, wood, ore, metal, tool)
    
    def unit_work(self):
        if self.inventory["metal"] >= 2:
            self.consume("metal", 2)
            self.produce("tool", 1)

    def shortage(self):
        shortage = {comodity: 0 for comodity in ["wood", "ore", "tool"]}
        shortage["food"] = 8 - self.inventory["food"]
        shortage["metal"] = 2 * UNIT_PER_DAY - self.inventory["metal"]
        return shortage

    def surplus(self):
        surplus = {comodity: 0 for comodity in ["food", "wood", "ore", "metal"]}
        surplus["tool"] = self.inventory["tool"]
