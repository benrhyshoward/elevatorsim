from elevator import DoorState
from elevatoraction import ElevatorAction, Action
from person import Person


class ElevatorSimulation:

    def __init__(self, elevator_system):
        self.elevator_system = elevator_system

        # initialising empty lists of lists
        self.people_waiting_at_floors = [[] for _ in range(elevator_system.total_floors)]
        self.people_in_elevators = [[] for _ in elevator_system.elevators]

        self.time = 0                       # current time of the simulation
        self.calls = []                     # list of all the calls processed by the simulation so far
        self.actions = []                   # list of all the actions taken by the elevators so far
        self.total_people = 0               # total number of people who entered the system
        self.people_turned_away = 0         # total number of people turned away due to a full car
        self.people_served = 0              # total number of people who made a successful end to end journey
        self.total_waiting_time = 0         # total number of seconds spent waiting (for successful journeys)
        self.total_time_in_elevator = 0     # total number of seconds spent in an elevator (for successful journeys)
        self.average_time_waiting = 0       # average number of seconds spent waiting (for successful journeys)
        self.average_time_in_elevator = 0   # average number of seconds spent in an elevator (for successful journeys)

    def simulate_calls(self, calls):
        for call in calls:
            if call.time < self.time:
                raise ValueError("Cannot process call at time " + str(call.time) + " - it is further in the past than the current simulation time " + str(self.time))
            self.calls.append(call)
            # iterate simulation until time of next event
            while self.time < call.time:
                self.iterate()

            # sending the call to the elevator system
            assigned_elevator = self.elevator_system.ingest_call(call.call_floor, call.destination_floor)

            # adding new people to the floor
            people_to_add = [Person(self.time, call.destination_floor, assigned_elevator) for _ in range(call.people)]
            self.people_waiting_at_floors[call.call_floor].extend(people_to_add)
            self.total_people += len(people_to_add)

        # after processing all calls, continue to iterate until all elevators are finished
        while not self.iterate():
            pass

        print("All elevator actions completed")

    def iterate(self):
        finished = True
        for index, elevator in enumerate(self.elevator_system.elevators):
            action = elevator.iterate()
            if action:
                # at least one elevator is still performing actions, so we're not finished yet
                finished = False
                if action != Action.BLOCKED:
                    self.actions.append(ElevatorAction(self.time, index, action,elevator.current_floor))
            if elevator.door_state == DoorState.OPEN :

                # manage people exiting
                people_to_exit = [person for person in self.people_in_elevators[index] if person.target_floor == elevator.current_floor]
                for person in people_to_exit:
                    self.people_served += 1
                    self.total_waiting_time += person.entrance_time - person.call_time
                    self.average_time_waiting = self.total_waiting_time / self.people_served
                    self.total_time_in_elevator += self.time - person.entrance_time
                    self.average_time_in_elevator = self.total_time_in_elevator / self.people_served
                self.people_in_elevators[index] = [person for person in self.people_in_elevators[index] if person.target_floor != elevator.current_floor]

                # manage people entering
                people_waiting = [person for person in self.people_waiting_at_floors[elevator.current_floor] if person.assigned_elevator == index]
                remaining_capacity = elevator.capacity - len(self.people_in_elevators[index])
                people_to_enter = people_waiting[:remaining_capacity]
                self.people_turned_away += len(people_waiting) - len(people_to_enter)
                for person in people_to_enter:
                    person.entrance_time = self.time
                self.people_in_elevators[index].extend(people_to_enter)
                self.people_waiting_at_floors[elevator.current_floor] = [p for p in self.people_waiting_at_floors[elevator.current_floor] if p.assigned_elevator != index]

        self.time += 1
        return finished

    def print_state(self):
        print("Calls:")
        for c in self.calls:
            print(c)
        print("")

        print("Actions:")
        for a in self.actions:
            print(a)
        print("")

        print("Statistics:")
        print("Total people = " + str(self.total_people))
        print("People served = " + str(self.people_served))
        print("People turned away due to full car = " + str(self.people_turned_away))
        print("People still waiting = " + str(sum([len(p) for p in self.people_waiting_at_floors])))
        print("People still in elevators = " + str(sum([len(p) for p in self.people_in_elevators])))
        print("Total wait time = " + str(self.total_waiting_time))
        print("Total time inside elevators = " + str(self.total_time_in_elevator))
        print("Average wait time = " + str(self.average_time_waiting))
        print("Average time inside elevators = " + str(self.average_time_in_elevator))

    def reset_state(self):
        self.people_waiting_at_floors = [[] for _ in range(self.elevator_system.total_floors)]
        self.people_in_elevators = [[] for _ in self.elevator_system.elevators]

        self.time = 0

        self.calls = []
        self.actions = []
        self.total_people = 0
        self.people_turned_away = 0
        self.people_served = 0
        self.total_waiting_time = 0
        self.total_time_in_elevator = 0
        self.average_time_in_elevator = 0
        self.average_time_waiting = 0










