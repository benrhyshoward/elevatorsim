from enum import Enum


class ElevatorAction:
    def __init__(self, time, elevator_number, action, floor):
        self.time = time
        self.elevator_number = elevator_number
        self.action = action
        self.floor = floor

    def __repr__(self):
        return "t = " + str(self.time) + \
               ", elevator = " + str(self.elevator_number) + \
               ", action = " + str(self.action.name) + \
               ", floor = " + str(self.floor)

    def __eq__(self, other):
        if isinstance(other, ElevatorAction):
            return self.time == other.time and \
                   self.elevator_number == other.elevator_number and \
                   self.action == other.action and \
                   self.floor == other.floor
        return False


class Action(Enum):
    BLOCKED = 1
    MOVE_UP = 2
    MOVE_DOWN = 3
    OPEN_DOORS = 4
    OPEN_DOORS_LOBBY = 5


ActionTimings = {
    Action.BLOCKED: 1,
    Action.MOVE_UP: 1,
    Action.MOVE_DOWN: 1,
    Action.OPEN_DOORS: 5,
    Action.OPEN_DOORS_LOBBY: 30
}