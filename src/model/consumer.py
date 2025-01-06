from src.model.producer import ProducerAgent
from typing import Tuple

from repast4py import core

class ConsumerAgent(core.Agent):
    TYPE=0

    def __init__(self, local_id: int, rank: int, name, budget, initial_usage=0):
        super().__init__(id=local_id, type=ConsumerAgent.TYPE, rank=rank)
        self.name = name
        self.budget = budget
        self.usage = initial_usage
        self.producers = {}
        # confidence and distrust coefficients
        self.alpha = 0.01
        self.beta = 0.08
        # for global local accounting
        self.trust_level = 0.5

    def save(self) -> Tuple:
        return (self.uid, self.name, self.budget, self.usage)
    
    def update_trust_level(self, uid, positive=True):
        curr_producer = self.producers[uid]
        trust_level = curr_producer.trust_level

        if positive:
            curr_producer.trust_level = min(trust_level*(1 + self.alpha), 1)
        else:
            curr_producer.trust_level = max(trust_level*(1 - self.beta), 0)

        return curr_producer.trust_level
    
    def make_decision(self, producers=[]):
        """
            Choose "Producer" based on price (unit_cost) and trust.
        """
        producer_scores = {}
        best_producer = None
        
        for prod in producers:
            if prod in self.producers.keys():
                self.producers[prod].capacity = producers[prod].capacity
                self.producers[prod].unit_cost = producers[prod].unit_cost
            else:
                self.producers[prod] = ProducerAgent(
                                            producers[prod].uid[0],
                                            producers[prod].uid[2],
                                            producers[prod].name,
                                            producers[prod].unit_cost,
                                            producers[prod].capacity,
                                        )
                
            curr_prod = self.producers[prod] # get current producer
            cost = curr_prod.unit_cost * self.usage # calculate cost

            # Adjust decision based on trust level
            if curr_prod.trust_level >= 0.5 and cost <= self.budget:
                # If trust level is high or medium, make decision as usual
                producer_scores[curr_prod.uid] = curr_prod.get_score()
            else:
                # If trust level is low, reduce usage regardless of cost
                """Reduce Usage"""

        if(producer_scores):
            uid = min(producer_scores, key=producer_scores.get)
            best_producer = self.producers[uid]

        return best_producer, self
