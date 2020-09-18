import unittest
from unittest.mock import patch

from elevatorcall import generate_calls, random_0_weighted, clamped_log_normal


class TestElevatorCall(unittest.TestCase):

    @patch('elevatorcall.clamped_log_normal')
    @patch('elevatorcall.random_0_weighted')
    def test_generate_call(self, random_0_weighted_mock, clamped_log_normal_mock):

        clamped_log_normal_mock.return_value = 2
        random_0_weighted_mock.side_effect = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        result = generate_calls(start_time=0, end_time=2, floors=10)

        self.assertEqual(len(result), 4)
        self.assertTrue(all(call.people == 2 for call in result))
        for index, call in enumerate(result):
            self.assertEqual(call.call_floor, index*2)
            self.assertEqual(call.destination_floor, index*2+1)

    def test_generate_call_no_time(self):
        result = generate_calls(start_time=0, end_time=0, floors=10)

        self.assertEqual(len(result), 0)

    @patch('random.randrange')
    def test_random_0_weighted(self, randrange_mock):
        def randrange_side_effect(arg1, arg2):
            if arg1 == 0 and arg2 == 2*10:
                return 5

        randrange_mock.side_effect = randrange_side_effect
        result = random_0_weighted(high=10, factor=2)
        self.assertEqual(result, 5)

    @patch('random.randrange')
    def test_random_0_weighted_above_high(self, randrange_mock):
        def randrange_behaviour(low, high):
            if low == 0 and high == 3*5:
                return 11

        randrange_mock.side_effect = randrange_behaviour
        result = random_0_weighted(high=5, factor=3)
        self.assertEqual(result, 0)

    @patch('random.lognormvariate')
    def test_clamped_log_normal_in_range(self, lognormvariate_mock):
        def lognormvariate_behaviour(mu, sigma):
            if mu == 1 and sigma == 2:
                return 5

        lognormvariate_mock.side_effect = lognormvariate_behaviour
        result = clamped_log_normal(1,2,0,10)
        self.assertEqual(result, 5)

    @patch('random.lognormvariate')
    def test_clamped_log_normal_low(self, lognormvariate_mock):
        def lognormvariate_behaviour(mu, sigma):
            if mu == 1 and sigma == 2:
                return 10

        lognormvariate_mock.side_effect = lognormvariate_behaviour
        result = clamped_log_normal(1,2,0,5)
        self.assertEqual(result, 5)

    @patch('random.lognormvariate')
    def test_clamped_log_normal_high(self, lognormvariate_mock):
        def lognormvariate_behaviour(mu, sigma):
            if mu == 1 and sigma == 2:
                return 0

        lognormvariate_mock.side_effect = lognormvariate_behaviour
        result = clamped_log_normal(1,2,5,10)
        self.assertEqual(result, 5)
