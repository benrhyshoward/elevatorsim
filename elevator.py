from enum import Enum

from elevatoraction import Action, ActionTimings


class DoorState(Enum):
    CLOSED = 0
    OPEN = 1


class Elevator:
    def __init__(self, capacity=10, current_floor=0):
        self.capacity = capacity
        self.current_floor = current_floor

        self.destinations = []
        self.blocked_for = 0
        self.door_state = DoorState.CLOSED

    # iterates the elevator's internal state forward one time step and returns the action taken
    def iterate(self):
        if self.blocked_for > 0:
            # still waiting
            self.blocked_for -= 1
            return Action.BLOCKED

        if len(self.destinations) == 0:
            # nowhere to go
            return None

        if self.current_floor == self.destinations[0]:
            # we are at our next destination, can open doors
            self.destinations.pop(0)
            self.door_state = DoorState.OPEN
            if self.current_floor == 0:
                self.blocked_for = ActionTimings[Action.OPEN_DOORS_LOBBY]-1
                return Action.OPEN_DOORS_LOBBY
            else:
                self.blocked_for = ActionTimings[Action.OPEN_DOORS]-1
                return Action.OPEN_DOORS

        self.door_state = DoorState.CLOSED
        if self.current_floor < self.destinations[0]:
            # Moving up
            self.current_floor += 1
            return Action.MOVE_UP
        else:
            # Moving down
            self.current_floor -= 1
            return Action.MOVE_DOWN
