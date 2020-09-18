from abc import ABC, abstractmethod
from enum import Enum


# To define a new elevator algorithm, extend this class and implement ingest_call
# Some examples can be seen below
class ElevatorBehaviour(ABC):

    # Accepts request floor information and updates the elevator state to account for this request
    # Returns the index of the elevator that the requester should enter to get to their destination
    @abstractmethod
    def ingest_call(self, elevators, call_floor, destination_floor):
        pass


# Picks an elevator through round robin and adds source and destination to the end of it's destination list
class RoundRobinAppend(ElevatorBehaviour):
    def __init__(self):
        self.current_elevator = 0

    def ingest_call(self, elevators, call_floor, destination_floor):
        self.current_elevator = (self.current_elevator + 1) % len(elevators)
        elevator_to_use = elevators[self.current_elevator]
        elevator_to_use.destinations.append(call_floor)
        elevator_to_use.destinations.append(destination_floor)
        return self.current_elevator


# Picks the closest elevator and adds source and destination to the start of it's destination list
class ClosestCallPrepend(ElevatorBehaviour):

    def ingest_call(self, elevators, call_floor, destination_floor):
        closest = self.closest_elevator_to_floor(elevators, call_floor)
        elevator_to_use = elevators[closest]
        elevator_to_use.destinations.insert(0, destination_floor)
        elevator_to_use.destinations.insert(0, call_floor)
        return closest

    def closest_elevator_to_floor(self, elevators, floor):
        closest = None
        for index, elevator in enumerate(elevators):
            if closest is None or (abs(elevator.current_floor - floor) < abs(elevators[closest].current_floor - floor)):
                closest = index
        return closest


# Picks the elevator with fewest destinations and adds source and destination to the end of it's destination list
class LeastBusyAppend(ElevatorBehaviour):

    def ingest_call(self, elevators, call_floor, destination_floor):
        least_busy = self.least_busy_elevator(elevators)
        elevator_to_use = elevators[least_busy]
        elevator_to_use.destinations.append(call_floor)
        elevator_to_use.destinations.append(destination_floor)
        return least_busy

    def least_busy_elevator(self, elevators):
        least_busy = None
        for index, elevator in enumerate(elevators):
            if least_busy is None or len(elevators[index].destinations) < len(elevators[least_busy].destinations):
                least_busy = index
        return least_busy


# Pick the elevator through round robin but elevators go all the way in one direction before changing
class StandardElevator(ElevatorBehaviour):
    def __init__(self):
        self.current_elevator = 0

    class Direction(Enum):
        UP = 1
        DOWN = 2

    def ingest_call(self, elevators, call_floor, destination_floor):
        self.current_elevator = (self.current_elevator + 1) % len(elevators)
        elevator_to_use = elevators[self.current_elevator]

        call_direction = None
        if destination_floor > call_floor:
            call_direction = self.Direction.UP
        elif destination_floor < call_floor:
            call_direction = self.Direction.DOWN

        # adding then later removing current floor from destinations list to reduce edge case checks
        elevator_to_use.destinations.insert(0, elevator_to_use.current_floor)
        call_insert_point = self.insert_floor_considering_direction(elevator_to_use.destinations, call_floor, call_direction)
        self.insert_floor_considering_direction(elevator_to_use.destinations, destination_floor, call_direction, after=call_insert_point)
        elevator_to_use.destinations.pop(0)

        return self.current_elevator

    # Inserts a new floor into a list of destinations, ensuring it is only added when going in the desired direction
    # Assumes destinations are ordered asc->desc->asc (or equivalent)
    def insert_floor_considering_direction(self, destinations, floor_to_insert, call_direction, after=0):
        previous_direction = None
        current_direction = None

        for index in range(1, len(destinations)):
            if destinations[index - 1] < destinations[index]:
                current_direction = self.Direction.UP
            if destinations[index - 1] > destinations[index]:
                current_direction = self.Direction.DOWN

            # don't want to insert anything until given point, but still need to track direction changes
            if index <= after:
                previous_direction = current_direction
                continue

            # if we are moving in the desired direction
            if current_direction == call_direction or call_direction is None:
                # already visiting this floor in this direction, do nothing
                if destinations[index] == floor_to_insert:
                    return index

                # can insert at current point
                if (
                        current_direction == self.Direction.UP and destinations[index] > floor_to_insert > destinations[index-1]
                ) or (
                        current_direction == self.Direction.DOWN and destinations[index] < floor_to_insert < destinations[index-1]
                ):
                    destinations.insert(index, floor_to_insert)
                    return index

            # at the top
            if current_direction == self.Direction.DOWN and previous_direction == self.Direction.UP:
                # need to add another value above the top
                if floor_to_insert > destinations[index-1]:
                    destinations.insert(index, floor_to_insert)
                    return index
                # duplicate value at the top
                if floor_to_insert == destinations[index-1]:
                    return index - 1

            # at the bottom
            if current_direction == self.Direction.UP and previous_direction == self.Direction.DOWN:
                # need to add another value below the bottom
                if floor_to_insert < destinations[index-1]:
                    destinations.insert(index, floor_to_insert)
                    return index
                # duplicate value at the bottom
                if floor_to_insert == destinations[index-1]:
                    return index - 1

            previous_direction = current_direction

        # no suitable place in the middle of the list, we can just insert at the end
        if len(destinations) == 0 or len(destinations) == 1 or destinations[len(destinations)-1] != floor_to_insert:
            destinations.append(floor_to_insert)
        return len(destinations)-1

