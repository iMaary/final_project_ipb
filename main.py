import random
import time

from mpi4py import MPI
from typing import Tuple

from repast4py import core, random, space, schedule, logging, parameters
from repast4py import context as ctx
import repast4py

class ConsumerAgent(core.Agent):
    TYPE=0

    def __init__(self, local_id: int, rank: int, name, budget, initial_usage=0):
        super().__init__(id=local_id, type=ConsumerAgent.TYPE, rank=rank)
        self.name = name
        self.budget = budget
        self.usage = initial_usage

    def calculate_cost(self, price_per_unit):
        return self.usage * price_per_unit

    def make_decision(self, producers=[]):
        """
            Choose "Producer" based on price (unit_cost) and trust.
        """
        producer_scores = {}
        for prod in producers:
            # how add budget criteria on best producer calculation?
            # self.budget
            # Adjust decision based on trust level
            if prod.trust_level >= 0.5:
                # If trust level is high or medium, make decision as usual
                cost = self.calculate_cost(prod.unit_cost)
                if cost <= self.budget and prod.produce_electricity(self.usage):
                    producer_scores[prod.name] = prod.get_score()
                else:
                    """Reduce Usage""" 
            else:
                # If trust level is low, reduce usage regardless of cost
                """Reduce Usage"""

        if(producer_scores):
            max_score_producer_name = max(producer_scores, key=producer_scores.get)
        else:
            max_score_producer_name = "None producer avaliable."

        print(f"Choosen Producer: {max_score_producer_name}")
        return max_score_producer_name

    def save(self) -> Tuple:
        return (self.uid, self.budget)
    

class ProducerAgent(core.Agent):
    TYPE=1

    def __init__(self, local_id: int, rank: int, name, initial_trust_level, unit_cost, initial_capacity=0, energy_type=1, failure_prob=0):
        super().__init__(id=local_id, type=ProducerAgent.TYPE, rank=rank)
        self.name = name
        self.trust_level = initial_trust_level
        self.unit_cost = unit_cost
        self.capacity = initial_capacity
        self.energy_type = energy_type
        self.alpha = 0.01
        self.beta = 0.08
        # On the furute we can add the historic of failures and trust level to update that.
        self.failure_prob = failure_prob
        # measured by the seasonality based on its energy type and avaliability. 
        self.quality = 0.9  # Initial quality rating
        # On the furute these vars (gammas, significance, trend) should be setted by:
        # PRODUCER: seasonality based on its energy type and avaliability.
        # CONSUMER: consumer payment historic
        self.gammas = []
        self.significance = None
        self.trend = None

    def produce_electricity(self, amount):
        """
            Function: produce electricty and updates the capacity.
            -
            It is based on the capacity avaliable, but there is a test
            for simulate the failed operation, besides the low capacity 
            scenario.
        """
        if amount <= self.capacity and not self.isOperationFailed():
            self.capacity -= amount
            self.update_trust_level()
            return True
        else:
            self.update_trust_level(failed=True)
            return False

    def get_score(self):
        return self.unit_cost*(1+0.001-self.trust_level)

    def update_trust_level(self, failed=False):
        if failed:
            self.trust_level = max(self.trust_level*(1 - self.beta), 0)
        else:
            self.trust_level = min(self.trust_level*(1 + self.alpha), 1)  
        self.print_status()

    def set_alpha_beta(gammas=[]):
        self.alpha = gammas[0]*significance + gammas[1]*trend
        self.beta = gammas[2]*significance + gammas[3]*trend
    
    def isOperationFailed(self):
        """
            Function: decide if the operation is failed or not
        """
        if random.random() < self.failure_prob:
            return True
        else:
            return False

    def print_status(self):
        space_fmt = " "*(20 - len(self.name))
        print(f"{self.name}{space_fmt}| TRUST LEVEL: {self.trust_level} - CAPACITY: {self.capacity}")

    def save(self) -> Tuple:
        return (self.uid, self.trust_level)


class Model:
    def __init__(self, comm: MPI.Intracomm):
        self.runner = schedule.init_schedule_runner(comm)
        self.runner.schedule_repeating_event(1, 1, self.handle_agent)
        self.runner.schedule_stop(20)

        # create the context to hold the agents and manage cross process synchronization
        self.context = ctx.SharedContext(comm)

        rank = comm.Get_rank()
        if rank == 0:
            agent_c1 = ConsumerAgent(123, rank, "Genivaldo", 5000, 9)
            self.context.add(agent_c1)
        elif rank == 1:
            p1 = ProducerAgent(111, rank, "Eólica", 0.8, 12, 1200, 1, 0.2)
            self.context.add(p1)
            p2 = ProducerAgent(222, rank, "Solar", 0.75, 6, 600, 2, 0.15)
            self.context.add(p2)
            p3 = ProducerAgent(333, rank, "Hidroelétrica", 0.9, 17, 1700, 3, 0.1)
            self.context.add(p3)

    def handle_agent(self):
        producers = []
    
        for agent in self.context.agents():
            if agent.type == 0:
                agent.make_decision(producers)

def main():
    comm = MPI.COMM_WORLD
    # id = comm.Get_rank()                    #number of the process running the code
    # numProcesses = comm.Get_size()          #total number of processes running
    # myHostName = MPI.Get_processor_name()   #machine name running the code

    model = Model(comm)
    model.runner.execute()

main()

# mpirun -n 2 python3 main.py
