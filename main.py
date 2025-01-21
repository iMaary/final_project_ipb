from utils.csv import *
from utils.json import *
from utils.handle_agent import *
from utils.handle_agent.restore import *
from src.model.producer import ProducerAgent
from src.model.consumer import ConsumerAgent

from typing import Dict
from mpi4py import MPI

from repast4py import space, schedule, parameters
from repast4py import context as ctx

class Model:    
    def __init__(self, comm: MPI.Intracomm, params: Dict):
        self.runner = schedule.init_schedule_runner(comm)
        self.runner.schedule_repeating_event(1, 1, self.step)
        self.runner.schedule_stop(params['stop.at'])

        # create the context to hold the agents and manage cross process synchronization
        self.context = ctx.SharedContext(comm)

        # create a bounding box equal to the size of the entire global world grid
        box = space.BoundingBox(0, params['world.width'], 0, params['world.height'], 0, 0)
        # create a SharedGrid of 'box' size with sticky borders that allows multiple agents
        # in each grid location.
        self.grid = space.SharedGrid(name='grid', bounds=box, borders=space.BorderType.Sticky,
                                     occupancy=space.OccupancyType.Multiple, buffer_size=3, comm=comm)
        self.context.add_projection(self.grid)

        rank = comm.Get_rank()
        
        if rank == 0:
            consumers = read_json_file('utils/data/consumers1000.json')
            add_agents(self, consumers, rank, ConsumerAgent, "name", "budget", "usage")
        elif rank == 1:
            producers = read_json_file('utils/data/producers1000.json')
            add_agents(self, producers, rank, ProducerAgent, "name", "unit_cost", "initial_capacity")

    def step(self):
        best_producers, curr_consumers = {}, []
        chosen_uid = None

        self.context.synchronize(restore_producer)

        for agent in self.context.agents():
            if agent.type == 0:
                producer, consumer = agent.make_decision(producer_cache)
                best_producers[consumer.uid] = producer
                curr_consumers.append(consumer)

        if best_producers:
            keys = list(best.uid if best else None for best in best_producers.values())
            unique_elements = list(set(keys))
            unique_elements = unique_elements.remove(None) if None in unique_elements else unique_elements
            chosen_uid = max(unique_elements, key=lambda x: keys.count(x)) if unique_elements else None

        if chosen_uid:
            curr_tick = self.runner.schedule.tick

            for consumer in curr_consumers:
                chosen_producer = producer_cache[chosen_uid]
                local_best_producer = best_producers[consumer.uid]

                # check if the local choice is significantly better than the collective choice
                isSelfish, score_diff = compare_scores(local_best_producer, chosen_producer)
                if(isSelfish):
                    chosen_producer = producer_cache[local_best_producer.uid]                 
                    consumer.trust_level = max(consumer.trust_level*(1 - consumer.beta), 0)
                else:                   
                    consumer.trust_level = min(consumer.trust_level*(1 + consumer.alpha), 1)
                
                old_capacity = chosen_producer.capacity
                # require slots electricity, success depends on avaliable capacity
                status = chosen_producer.produce_electricity(consumer.usage)
                # update trust levels in each consumer based on received energy success
                curr_tl = consumer.update_trust_level(chosen_producer.uid, positive="Success" in status)
 
                write_agreement("result.csv", [curr_tick,
                                               status, 
                                               chosen_producer.name,
                                               old_capacity, 
                                               chosen_producer.capacity, 
                                               curr_tl,
                                               consumer.uid,
                                               chosen_producer.uid,
                                               consumer.usage,
                                               consumer.budget,
                                               chosen_producer.unit_cost,
                                               consumer.trust_level,
                                               score_diff,
                                            ])


    def start(self):
        self.runner.execute()


def run():
    comm = MPI.COMM_WORLD
    # id = comm.Get_rank()                    #number of the process running the code
    # numProcesses = comm.Get_size()          #total number of processes running
    # myHostName = MPI.Get_processor_name()   #machine name running the code
    
    parser = parameters.create_args_parser()
    args = parser.parse_args()
    params = parameters.init_params(args.parameters_file, args.parameters)

    initialize_csv(params['csv_name'], params['csv_header'])

    # Run Model
    # ---
    # Instance
    model = Model(comm, params)
    # Start Model
    model.start()

if __name__ == "__main__":
    run()

# mpirun -n 3 python3 main.py conf.yaml
