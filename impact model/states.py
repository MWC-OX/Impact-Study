# Import functiosn here
import numpy as np

class state:
    """
    Class to define if a state should change
    knows its own state and how long it has been in it
    most useful function is check_transistion which is called by person class after every time step
    """
    # List of states somone can take
    # should be constant
    STATE_LIST = [
        "STATE 1",
        "STATE 2",
        "STATE 3",
    ]

    # state someone should be initalised in
    # probably healthy
    DEFAULT_STATE = STATE_LIST[0]


    # Initaliser function
    def __init__(self):
        self.state = self.DEFAULT_STATE
        self.time_in_state = 0

    # Returns current state
    def get_current_state(self):
        return self.state

    # Ran after aging people
    # should take all relevant risk factors as arguments
    def check_transistion(self, dt,
            risk_factor_1, risk_factor_2,
            risk_factor_3, risk_factor_4
    ):
        
        # used for checking if state changes
        current = self.state

        # increases spent time in current state
        self.time_in_state += dt

        # Logic to check state
        if self.state == "STATE 1":
            # runs a function to check if state should change based on current state
            # Job is define these!
            # ( realy this is the brunt work of this file )
            self._state_1(risk_factor_1, risk_factor_2)
        elif self.state == "STATE 2":
            self._state_2(risk_factor_3)
        else:
            raise Exception("No such state exists")
        

        # resets time in state if changed
        if current != self.state:
            self.time_in_state = 0


    # main job to define these
    # replace _state_1 with whatever the states should be called
    # and risk1 with risk factors that are parsed in 

    def _state_1(self, risk1, risk2):
        raise NotImplementedError()
    
    def _state_2(self, risk3):
        raise NotImplementedError()

