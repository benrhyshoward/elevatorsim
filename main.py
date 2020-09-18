import random

from elevator import Elevator
from elevatorbehaviour import RoundRobinAppend
from elevatorcall import generate_calls
from elevatorsimulation import ElevatorSimulation
from elevatorsystem import ElevatorSystem

# optional seed
random.seed(12345)

number_of_elevators = 3
floors = 100

# creating elevators
elevators = [Elevator(capacity=10, current_floor=0) for _ in range(number_of_elevators)]

system = ElevatorSystem(
    elevators=elevators,
    behaviour=RoundRobinAppend(),
    total_floors=floors)

simulation = ElevatorSimulation(
    elevator_system=system)

calls = generate_calls(
    start_time=0,
    end_time=2000,
    floors=floors)

simulation.simulate_calls(calls)
simulation.print_state()
