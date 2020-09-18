import unittest

from elevator import Elevator
from elevatorbehaviour import (
    ClosestCallPrepend,
    LeastBusyAppend,
    StandardElevator
)


class TestElevatorCall(unittest.TestCase):

    def test_closest_elevator_to_floor(self):
        elevators = [Elevator(current_floor=0), Elevator(current_floor=2), Elevator(current_floor=5)]
        behaviour = ClosestCallPrepend()

        result = behaviour.closest_elevator_to_floor(elevators, 3)

        self.assertEqual(result, 1)

    def test_closest_elevator_to_floor_no_elevators(self):
        behaviour = ClosestCallPrepend()
        result = behaviour.closest_elevator_to_floor([], 3)

        self.assertEqual(result, None)

    def test_least_busy_elevator(self):
        behaviour = LeastBusyAppend()

        elevator1 = Elevator()
        elevator1.destinations = [1, 2, 3, 4]
        elevator2 = Elevator()
        elevator2.destinations = [5, 6]
        elevator3 = Elevator()
        elevator3.destinations = [7, 8, 9]

        elevators = [elevator1, elevator2, elevator3]

        result = behaviour.least_busy_elevator(elevators)

        self.assertEqual(result, 1)

    def test_least_busy_elevator_no_elevators(self):
        behaviour = LeastBusyAppend()
        result = behaviour.least_busy_elevator([])

        self.assertEqual(result, None)

    def test_insert_floor_considering_direction_empty(self):
        behaviour = StandardElevator()
        destinations = []
        behaviour.insert_floor_considering_direction(destinations, 2, behaviour.Direction.UP)
        expected = [2]

        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_going_up(self):
        behaviour = StandardElevator()
        destinations = [2, 4, 6, 8, 6, 4, 2]
        result = behaviour.insert_floor_considering_direction(destinations, 3, behaviour.Direction.UP)
        expected = [2, 3, 4, 6, 8, 6, 4, 2]

        self.assertEqual(result, 1)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_going_up_2(self):
        behaviour = StandardElevator()
        destinations = [8, 6, 4, 2, 4, 6, 8]
        result = behaviour.insert_floor_considering_direction(destinations, 3, behaviour.Direction.UP)
        expected = [8, 6, 4, 2, 3, 4, 6, 8]

        self.assertEqual(result, 4)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_going_down(self):
        behaviour = StandardElevator()
        destinations = [2, 4, 6, 8, 6, 4, 2]
        result = behaviour.insert_floor_considering_direction(destinations, 5, behaviour.Direction.DOWN)
        expected = [2, 4, 6, 8, 6, 5, 4, 2]

        self.assertEqual(result, 5)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_going_down_2(self):
        behaviour = StandardElevator()
        destinations = [8, 6, 4, 2, 4, 6, 8]
        result = behaviour.insert_floor_considering_direction(destinations, 5, behaviour.Direction.DOWN)
        expected = [8, 6, 5, 4, 2, 4, 6, 8]

        self.assertEqual(result, 2)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_one_already_exists(self):
        behaviour = StandardElevator()
        destinations = [2, 4, 6, 8, 6, 4, 2]
        result = behaviour.insert_floor_considering_direction(destinations, 6, behaviour.Direction.DOWN)
        expected = [2, 4, 6, 8, 6, 4, 2]

        self.assertEqual(result, 4)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_no_suitable_place(self):
        behaviour = StandardElevator()
        destinations = [2, 4, 6, 8]
        result = behaviour.insert_floor_considering_direction(destinations, 5, behaviour.Direction.DOWN)
        expected = [2, 4, 6, 8, 5]

        self.assertEqual(result, 4)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_bottom(self):
        behaviour = StandardElevator()
        destinations = [8, 6, 4, 2, 4]
        result = behaviour.insert_floor_considering_direction(destinations, 0, behaviour.Direction.DOWN)
        expected = [8, 6, 4, 2, 0, 4]

        self.assertEqual(result, 4)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_insert_after_start(self):
        behaviour = StandardElevator()
        destinations = [4]
        result = behaviour.insert_floor_considering_direction(destinations, 0, behaviour.Direction.UP)
        expected = [4, 0]

        self.assertEqual(result, 1)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_insert_after_given_index(self):
        behaviour = StandardElevator()
        destinations = [2, 4, 6, 8]
        result = behaviour.insert_floor_considering_direction(destinations, 5, behaviour.Direction.UP, after=2)
        expected = [2, 4, 6, 8, 5]

        self.assertEqual(result, 4)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_insert_after_given_index_with_direction_change(self):
        behaviour = StandardElevator()
        destinations = [5, 0]
        result = behaviour.insert_floor_considering_direction(destinations, 10, behaviour.Direction.UP, after=1)
        expected = [5, 0, 10]

        self.assertEqual(result, 2)
        self.assertEqual(destinations, expected)

    def test_insert_floor_considering_direction_insert_duplicate_on_bottom(self):
        behaviour = StandardElevator()
        destinations = [2, 0, 2, 4]
        result = behaviour.insert_floor_considering_direction(destinations, 0, behaviour.Direction.UP)
        expected = [2, 0, 2, 4]

        self.assertEqual(result, 1)
        self.assertEqual(destinations, expected)



