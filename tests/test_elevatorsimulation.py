import unittest
from unittest.mock import MagicMock

from elevator import Action, DoorState, Elevator
from elevatoraction import ElevatorAction
from elevatorbehaviour import RoundRobinAppend
from elevatorcall import ElevatorCall
from elevatorsimulation import ElevatorSimulation
from elevatorsystem import ElevatorSystem
from person import Person


class TestElevatorSimulation(unittest.TestCase):

    def test_simulate_calls_invalid_time(self):
        e = ElevatorSimulation(elevator_system=ElevatorSystem(elevators=[], total_floors=5, behaviour=None))
        e.time = 5

        calls = [ElevatorCall(time=3, call_floor=0, destination_floor=4, people=5)]
        self.assertRaises(ValueError, e.simulate_calls, calls)

    def test_simulate_calls_single_call(self):
        system = MagicMock()
        e = ElevatorSimulation(elevator_system=system)

        e.iterate = MagicMock()

        def iterate_behaviour():
            e.time += 1
            return True
        e.iterate.side_effect = iterate_behaviour

        system.ingest_call.return_value = 1

        calls = [ElevatorCall(time=3, call_floor=0, destination_floor=4, people=5)]

        e.simulate_calls(calls)

        self.assertEqual(e.calls, calls)
        self.assertEqual(e.iterate.call_count, 4)
        self.assertEqual(e.total_people, 5)
        self.assertEqual(len(e.people_waiting_at_floors[0]), 5)
        for person in e.people_waiting_at_floors[0]:
            self.assertEqual(person.assigned_elevator, 1)
            self.assertEqual(person.call_time, 3)
            self.assertEqual(person.target_floor,4)
            self.assertTrue(person.entrance_time is None)
            self.assertTrue(person.exit_time is None)

    def test_iterate_simulation_over(self):
        elevator1 = MagicMock()
        elevator2 = MagicMock()

        elevator1.iterate.return_value = None
        elevator2.iterate.return_value = None

        system = ElevatorSystem([elevator1, elevator2], None, 10)
        e = ElevatorSimulation(system)

        result = e.iterate()

        self.assertTrue(result)
        self.assertEqual(e.time, 1)

    def test_iterate_all_doors_closed(self):
        elevator1 = MagicMock()
        elevator2 = MagicMock()

        elevator1.iterate.return_value = Action.MOVE_UP
        elevator1.current_floor = 2
        elevator2.iterate.return_value = Action.BLOCKED
        elevator2.current_floor = 3

        system = ElevatorSystem([elevator1, elevator2], None, 10)
        e = ElevatorSimulation(system)

        result = e.iterate()

        self.assertFalse(result)
        self.assertEqual(e.time, 1)
        self.assertEqual(len(e.actions), 1)
        self.assertEqual(e.actions[0].time, 0)
        self.assertEqual(e.actions[0].elevator_number, 0)
        self.assertEqual(e.actions[0].action, Action.MOVE_UP)
        self.assertEqual(e.actions[0].floor, 2)

    def test_iterate_people_exit(self):
        elevator1 = MagicMock()

        elevator1.iterate.return_value = Action.BLOCKED
        elevator1.door_state = DoorState.OPEN
        elevator1.current_floor = 2

        system = ElevatorSystem([elevator1], None, 10)
        e = ElevatorSimulation(system)
        e.time = 10

        person1 = Person(call_time=0, target_floor=2, assigned_elevator=0)
        person1.entrance_time=2
        person2 = Person(call_time=1, target_floor=3, assigned_elevator=0)
        person2.entrance_time=5
        person3 = Person(call_time=3, target_floor=2, assigned_elevator=0)
        person3.entrance_time=6

        e.people_in_elevators[0] = [person1, person2, person3]

        result = e.iterate()

        self.assertFalse(result)
        self.assertEqual(len(e.people_in_elevators[0]), 1)
        self.assertEqual(e.people_in_elevators[0][0], person2)
        self.assertEqual(e.people_served,2)
        self.assertEqual(e.total_waiting_time, 5)
        self.assertEqual(e.average_time_waiting, 2.5)
        self.assertEqual(e.total_time_in_elevator, 12)
        self.assertEqual(e.average_time_in_elevator, 6)

    def test_iterate_people_enter(self):
        elevator1 = MagicMock()

        elevator1.iterate.return_value = Action.BLOCKED
        elevator1.door_state = DoorState.OPEN
        elevator1.current_floor = 2
        elevator1.capacity = 10

        system = ElevatorSystem([elevator1], None, 10)
        e = ElevatorSimulation(system)
        e.time = 10

        person1 = Person(call_time=0, target_floor=3, assigned_elevator=0)
        person2 = Person(call_time=1, target_floor=4, assigned_elevator=0)
        person3 = Person(call_time=2, target_floor=5, assigned_elevator=1)

        e.people_waiting_at_floors[2] = [person1, person2, person3]

        result = e.iterate()

        self.assertFalse(result)
        self.assertEqual(len(e.people_in_elevators[0]), 2)
        for person in e.people_in_elevators[0]:
            self.assertEqual(person.entrance_time, 10)
        self.assertEqual(e.people_in_elevators[0][0], person1)
        self.assertEqual(e.people_in_elevators[0][1], person2)
        self.assertEqual(len(e.people_waiting_at_floors[2]),1)
        self.assertEqual(e.people_waiting_at_floors[2][0], person3)

    def test_iterate_people_turned_away(self):
        elevator1 = MagicMock()

        elevator1.iterate.return_value = Action.BLOCKED
        elevator1.door_state = DoorState.OPEN
        elevator1.current_floor = 2
        elevator1.capacity = 1

        system = ElevatorSystem([elevator1], None, 10)
        e = ElevatorSimulation(system)
        e.time = 10

        person1 = Person(call_time=0, target_floor=3, assigned_elevator=0)
        person2 = Person(call_time=1, target_floor=4, assigned_elevator=0)
        person3 = Person(call_time=2, target_floor=5, assigned_elevator=1)

        e.people_waiting_at_floors[2] = [person1, person2, person3]

        result = e.iterate()

        self.assertFalse(result)
        self.assertEqual(len(e.people_in_elevators[0]), 1)
        self.assertEqual(e.people_in_elevators[0][0], person1)
        self.assertEqual(e.people_in_elevators[0][0].entrance_time, 10)
        self.assertEqual(len(e.people_waiting_at_floors[2]),1)
        self.assertEqual(e.people_waiting_at_floors[2][0], person3)
        self.assertEqual(e.people_turned_away, 1)

    def test_reset_state(self):
        system = ElevatorSystem([Elevator()], None, 10)
        e = ElevatorSimulation(system)

        e.people_waiting_at_floors = [[Person(call_time=1,target_floor=1,assigned_elevator=1)]]
        e.people_in_elevators = [[Person(call_time=2,target_floor=2,assigned_elevator=2)]]

        e.time = 5
        e.calls = [ElevatorCall(1,2,3,4)]
        e.actions = [ElevatorAction(1,2,3,4)]
        e.total_people = 5
        e.people_turned_away = 6
        e.people_served = 7
        e.total_waiting_time = 8
        e.total_time_in_elevator = 9
        e.average_time_waiting = 10
        e.average_time_in_elevator = 11

        e.reset_state()

        self.assertEqual(len(e.people_waiting_at_floors[0]), 0)
        self.assertEqual(len(e.people_in_elevators[0]), 0)
        self.assertEqual(e.time, 0)
        self.assertEqual(len(e.calls), 0)
        self.assertEqual(len(e.actions), 0)
        self.assertEqual(e.total_people, 0)
        self.assertEqual(e.people_turned_away, 0)
        self.assertEqual(e.people_served, 0)
        self.assertEqual(e.total_waiting_time, 0)
        self.assertEqual(e.total_time_in_elevator, 0)
        self.assertEqual(e.average_time_waiting, 0)
        self.assertEqual(e.average_time_in_elevator, 0)

    # Integration test for a whole example simulation flow
    def test_simulate_calls_end_to_end(self):
        elevators = [Elevator(capacity=10, current_floor=0) for _ in range(2)]

        system = ElevatorSystem(
            elevators=elevators,
            behaviour=RoundRobinAppend(),
            total_floors=10)

        simulation = ElevatorSimulation(
            elevator_system=system)

        calls = [
            ElevatorCall(time=1, call_floor=0, destination_floor=2, people=2),
            ElevatorCall(time=2, call_floor=1, destination_floor=3, people=2),
            ElevatorCall(time=3, call_floor=1, destination_floor=0, people=5)
        ]

        expected_actions= [
            ElevatorAction(time=1, elevator_number=1, action=Action.OPEN_DOORS_LOBBY, floor=0),
            ElevatorAction(time=2, elevator_number=0, action=Action.MOVE_UP, floor=1),
            ElevatorAction(time=3, elevator_number=0, action=Action.OPEN_DOORS, floor=1),
            ElevatorAction(time=8, elevator_number=0, action=Action.MOVE_UP, floor=2),
            ElevatorAction(time=9, elevator_number=0, action=Action.MOVE_UP, floor=3),
            ElevatorAction(time=10, elevator_number=0, action=Action.OPEN_DOORS, floor=3),
            ElevatorAction(time=31, elevator_number=1, action=Action.MOVE_UP, floor=1),
            ElevatorAction(time=32, elevator_number=1, action=Action.MOVE_UP, floor=2),
            ElevatorAction(time=33, elevator_number=1, action=Action.OPEN_DOORS, floor=2),
            ElevatorAction(time=38, elevator_number=1, action=Action.MOVE_DOWN, floor=1),
            ElevatorAction(time=39, elevator_number=1, action=Action.OPEN_DOORS, floor=1),
            ElevatorAction(time=44, elevator_number=1, action=Action.MOVE_DOWN, floor=0),
            ElevatorAction(time=45, elevator_number=1, action=Action.OPEN_DOORS_LOBBY, floor=0)
        ]

        simulation.simulate_calls(calls)

        self.assertEqual(simulation.calls, calls)
        self.assertEqual(simulation.actions, expected_actions)
        self.assertEqual(len(simulation.people_waiting_at_floors[0]), 0)
        self.assertEqual(len(simulation.people_in_elevators[0]), 0)
        self.assertEqual(simulation.time, 76)
        self.assertEqual(simulation.total_people, 9)
        self.assertEqual(simulation.people_turned_away, 0)
        self.assertEqual(simulation.people_served, 9)
        self.assertEqual(simulation.total_waiting_time, 182)
        self.assertEqual(simulation.total_time_in_elevator, 108)
        self.assertAlmostEqual(simulation.average_time_waiting, 20.222, 3)
        self.assertEqual(simulation.average_time_in_elevator, 12.0)
