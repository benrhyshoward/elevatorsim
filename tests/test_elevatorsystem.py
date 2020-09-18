import unittest
from unittest.mock import MagicMock

from elevatorsystem import ElevatorSystem


class TestElevatorSystem(unittest.TestCase):

    def test_ingest_call(self):
        behaviour = MagicMock()
        behaviour.ingest_call = MagicMock()
        e = ElevatorSystem(total_floors=10, behaviour=behaviour, elevators=[])

        e.ingest_call(0, 5)

        behaviour.ingest_call.assert_called_with([], 0, 5)

    def test_ingest_call_invalid_call_floor(self):
        e = ElevatorSystem(total_floors=10, behaviour=None, elevators=[])

        self.assertRaises(ValueError, e.ingest_call, 20, 5)

    def test_ingest_call_invalid_destination_floor(self):
        e = ElevatorSystem(total_floors=10, behaviour=None, elevators=[])

        self.assertRaises(ValueError, e.ingest_call, 5, 20)

