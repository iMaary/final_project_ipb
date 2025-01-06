from random import random as rd
from typing import Tuple

from repast4py import core

class ProducerAgent(core.Agent):
    TYPE=1

    def __init__(self, local_id: int, rank: int, name, unit_cost, initial_capacity=0):
        super().__init__(id=local_id, type=ProducerAgent.TYPE, rank=rank)
        self.name = name
        self.unit_cost = unit_cost
        self.capacity = initial_capacity
        # for consumer local accounting
        self.trust_level = 0.5
        self.failure_prob = 0.15
    
    def save(self) -> Tuple:
        return (self.uid, self.name, self.unit_cost, self.capacity)

    def produce_electricity(self, amount):
        """
            Function: produce electricty and updates the capacity.
            -
            It is based on the capacity avaliable, but there is a test
            for simulate the failed operation, besides the low capacity 
            scenario.
        """
        failed = rd() < self.failure_prob # failure simulation

        if amount <= self.capacity and not failed:
            self.capacity -= amount
            return "Success"
        else:
            return "Failed"
    
    def get_score(self):
        return self.unit_cost*(1+(10**(-3))-self.trust_level)
