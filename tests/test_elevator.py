import unittest

from elevator import Elevator, Action, ActionTimings, DoorState


class TestElevator(unittest.TestCase):

    def test_iterate_up(self):
        e = Elevator(current_floor=0)
        e.destinations.append(2)
        e.door_state = DoorState.OPEN

        result = e.iterate()

        self.assertEqual(result, Action.MOVE_UP)
        self.assertEqual(e.door_state, DoorState.CLOSED)
        self.assertEqual(e.current_floor, 1)

    def test_iterate_down(self):
        e = Elevator(current_floor=2)
        e.destinations.append(0)
        e.door_state = DoorState.OPEN

        result = e.iterate()

        self.assertEqual(result, Action.MOVE_DOWN)
        self.assertEqual(e.door_state, DoorState.CLOSED)
        self.assertEqual(e.current_floor, 1)

    def test_iterate_blocked(self):
        e = Elevator(current_floor=0)
        e.destinations.append(2)
        e.blocked_for = 5

        result = e.iterate()

        self.assertEqual(result, Action.BLOCKED)
        self.assertEqual(e.current_floor, 0)
        self.assertEqual(e.blocked_for, 4)

    def test_iterate_finished(self):
        e = Elevator(current_floor=0)

        result = e.iterate()

        self.assertEqual(result, None)

    def test_iterate_open_doors_lobby(self):
        e = Elevator(current_floor=0)
        e.door_state = DoorState.CLOSED
        e.destinations.append(0)

        result = e.iterate()

        self.assertEqual(result, Action.OPEN_DOORS_LOBBY)
        self.assertEqual(e.door_state, DoorState.OPEN)
        self.assertEqual(len(e.destinations), 0)
        self.assertEqual(e.blocked_for, ActionTimings[Action.OPEN_DOORS_LOBBY]-1)

    def test_iterate_open_doors_not_lobby(self):
        e = Elevator(current_floor=5)
        e.door_state = DoorState.CLOSED
        e.destinations.append(5)

        result = e.iterate()

        self.assertEqual(result, Action.OPEN_DOORS)
        self.assertEqual(e.door_state, DoorState.OPEN)
        self.assertEqual(len(e.destinations), 0)
        self.assertEqual(e.blocked_for, ActionTimings[Action.OPEN_DOORS]-1)