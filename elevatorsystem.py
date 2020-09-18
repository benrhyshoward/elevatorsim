class ElevatorSystem:
    def __init__(self, elevators, behaviour, total_floors):
        self.elevators = elevators
        self.behaviour = behaviour
        self.total_floors = total_floors

    def ingest_call(self, call_floor, destination_floor):
        if call_floor >= self.total_floors or call_floor < 0:
            raise ValueError("Made a call from floor " + str(call_floor) + " which doesn't exist")
        if destination_floor >= self.total_floors or destination_floor < 0:
            raise ValueError("Made a call to floor " + str(destination_floor) + " which doesn't exist")
        return self.behaviour.ingest_call(self.elevators, call_floor, destination_floor)