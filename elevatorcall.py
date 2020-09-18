import random


class ElevatorCall:
    def __init__(self, time, call_floor, destination_floor, people):
        self.time = time
        self.call_floor = call_floor
        self.destination_floor = destination_floor
        self.people = people

    def __repr__(self):
        return "t = " + str(self.time) + \
               ", call_floor = " + str(self.call_floor) + \
               ", destination_floor = " + str(self.destination_floor) + \
               ", people = " + str(self.people)

    def __eq__(self, other):
        if isinstance(other, ElevatorCall):
            return self.time == other.time and \
                   self.call_floor == other.call_floor and \
                   self.destination_floor == other.destination_floor and \
                   self.people == other.people
        return False


# generates a random list of elevator calls
def generate_calls(start_time, end_time, floors):
    result = []
    for t in range(start_time, end_time):
        calls_this_timestep = clamped_log_normal(mean=-2.5, sdev=1, low=0, high=5)
        for i in range(calls_this_timestep):
            call_floor = random_0_weighted(floors, 2)
            destination_floor = random_0_weighted(floors, 2)
            if call_floor != destination_floor:
                result.append(ElevatorCall(
                    time=t,
                    call_floor=call_floor,
                    destination_floor=destination_floor,
                    people=clamped_log_normal(mean=0, sdev=1, low=1, high=5)))
    return result


# returning a random number between 0 and 'high'
# but weighted towards 0 such that 0 is returned 0 (1-1/factor) of the time
def random_0_weighted(high, factor):
    n = random.randrange(0, high*factor)
    if n >= high:
        n = 0
    return n


# rounded and clamped lognormal distribution
def clamped_log_normal(mean, sdev, low, high):
    return max(low, min(round(random.lognormvariate(mu=mean, sigma=sdev)), high))










