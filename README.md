## Elevator simulation

An exercise to simulate an elevator system, written in Python 3.

Used to simulate of a set of elevator calls against an elevator system and output the list of actions taken by the elevators, along with usage statistics.
It allows configuration through parameters such as number of elevators, elevator capacity, number of floors, and the elevator algorithm itself.
New elevator algorithms can be created and tested by implementing an abstract class and plugging into the simulation.

#### Usage (see an example in `main.py`)
 - Seed Python's `random` library using `random.seed` (optional)
 - Decide on an elevator algorithm to use from `elevatorbehaviour.py`, or create your own
 - Create a list of elevators with desired capacities and starting floors
 - Create a new elevator system, passing in the elevators and behaviour
 - Create a new elevator simulation, passing in the elevator system
 - Generate a time series of elevator calls using `elevatorcall.generate_calls`, or create your own set
 - Pass as many sets of calls into the elevator simulation as you like using `.simulate_calls`
 - View a summary of the state at any time using `.print_state()`, or query the state variables directly
 - If desired, reset the simulation using `.reset_state()`
 
 The tests can be run from the project root with  
 `python -m unittest discover`

#### More technical details
There are three main stateful objects that are used as part of the simulation

 - Elevator (`elevator.py`)
    - Fairly simple object, just tracks its current location, list of destinations, and door state
    - Will un-intelligently move towards and stop at floors based on its destination list using the `.iterate` method
    - Doesn't track state of people, time, or other elevators
    
 - Elevator system (`elevatorsystem.py`)
    - Composed of a set of elevators and a behaviour
    - Responsible for ingesting elevator calls and updating the elevators' destination lists as required based on the given behaviour
    - Doesn't track state of people or time
    - Behaviours can be easily created, updated, or swapped out as desired (see `elevatorbehaviour.py`)
    
 - Elevator simulation (`elevatorsimulation.py`)
    - Responsible for simulating an elevator system over time
    - Takes in sets of calls, sends them to the elevator system, and records the actions taken by the elevators
    - Iterates the system until no more actions are being made by the elevators
    - Tracks time and the state of people in the simulation
    - Generates statistics about how efficiently the system is serving people

 
#### Assumptions / Notes:
 - The elevator simulation cannot accept calls at a time further in the past than the current simulation time
 - After requesting an elevator, people are informed which elevator they should be getting on, and will only get on the one they are assigned to
 - Statistics are only gathered for people who make a successful end to end journey
 - People don't make calls where the source and destination floor are the same
 - Calling `.reset_state()` on the simulation will not effect the state of the elevator system or elevators themselves, these would need to be updated separately if required
 - Elevators are not able to make routing decisions based on state or locations of people
    -   If this was required (face tracking?) we could move the state of people into the elevator objects and pass any extra information into the `ingest_call` method

 
#### Some possible future improvements
 - More granular elevator algorithm classes, could maybe split into an elevator selection algorithm and an elevator destination algorithm, could then mix and match
 - More control over the call generation algorithm. e.g. parameters for frequency/number/distribution of calls, currently have a few hardcoded values in `elevatorcall.generate_calls`
 - Some conditional logic for the elevator algorithm to be swapped mid-simulation based on the state of the system or external factors (e.g. time of day)
 - Graphical/ASCII representation of how the system is progressing
 - Experiment with other algorithms and compare performance - some ideas:
    - Elevators assigned to ranges of floors (+ lobby)
    - Elevators assigned to floors based on factors (e.g. odd/evens)
    - Elevators always go back to lobby after completing their destination list
    - All elevators go to all the same floors at the same times, could be better when we are going to be serving lots of large groups