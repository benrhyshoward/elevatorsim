class Person:
    def __init__(self, call_time, target_floor, assigned_elevator):
        self.call_time = call_time
        self.entrance_time = None
        self.exit_time = None
        self.target_floor = target_floor
        self.assigned_elevator = assigned_elevator

    def __repr__(self):
        return "call_time - " + str(self.call_time) + \
               ", target_floor - " + str(self.target_floor) + \
               ", assigned_elevator - " + str(self.assigned_elevator)
