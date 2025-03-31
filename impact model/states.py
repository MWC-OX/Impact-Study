# Import functions here
import numpy as np
from gail_model import gail_model_risk
import random
from stage_mortality_data import survival_probabilities

class state:
    """
    Class to define if a state should change
    knows its own state and how long it has been in it
    most useful function is check_transistion which is called by person class after every time step
    """
    # List of states someone can take
    # should be constant
    STATE_LIST = [
        "healthy",
        "DCIS",
        "localized",
        "regional",
        "distant",
        "dead - cancer",
        "dead - other",
    ]

    # state someone should be initialized in
    # probably healthy
    DEFAULT_STATE = STATE_LIST[0]

    # Initializer function
    def __init__(self, age, life_table_data):
        self.state = self.DEFAULT_STATE
        self.time_in_state = 0
        self.age = age  # Age of the person
        self.life_table_data = life_table_data  # Life table data for mortality probabilities

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
        self.age += dt  # Increment age by the time step

        # Logic to check state
        if self.state == "healthy":
            self._state_healthy(risk_factor_1, risk_factor_2)
        elif self.state == "DCIS":
            self._state_DCIS(risk_factor_3)
        elif self.state == "localized":
            self._state_localized(risk_factor_3)
        elif self.state == "regional":
            self._state_regional(risk_factor_3)
        elif self.state == "distant":
            self._state_distant(risk_factor_4)
        elif self.state == "dead - cancer" or self.state == "dead - other":
            pass  # No transition from dead states
        else:
            raise Exception("No such state exists")
        
        # Check if the person transitions to "dead - other"
        if current != "dead - cancer" and self._check_dead_other():
            self.state = "dead - other"

        # resets time in state if changed
        if current != self.state:
            self.time_in_state = 0

    # Function to check if the person transitions to "dead - other"
    def _check_dead_other(self):
        # Ensure age is within the bounds of the life table
        if self.age >= len(self.life_table_data):
            return False  # No data for ages beyond the life table

        # Get the probability of dying from other causes at the current age
        mortality_probability = self.life_table_data[int(self.age), 1]

        # Generate a random number to decide if the person dies
        return random.random() < mortality_probability

    # main job to define these
# replace _state_1 with whatever the states should be called
    # and risk1 with risk factors that are parsed in 

    def _state_healthy(self, risk1, risk2):
        # Call the Gail Model to get the risk of developing breast cancer
        risk = gail_model_risk(
            age=risk1['age'],
            age_at_menarche=risk1['age_at_menarche'],
            age_at_first_birth=risk1['age_at_first_birth'],
            num_first_degree_relatives=risk1['num_first_degree_relatives'],
            num_biopsies=risk1['num_biopsies'],
            atypical_hyperplasia=risk1['atypical_hyperplasia'],
            race=risk1['race']
        )
        
        # Generate a single random number
        rand = random.random()
        
        # Use the random number to evaluate the Gail risk
        if rand < risk:
            # Breast cancer diagnosis occurs
            rand_stage = random.random()
            
            # Transition to DCIS, localized, regional, or distant based on probabilities
            if rand_stage < 0.166:  # 16.6% chance of DCIS
                self.state = "DCIS"
            elif rand_stage < 0.166 + 0.40061:  # 40.061% chance of localized
                self.state = "localized"
            elif rand_stage < 0.166 + 0.40061 + 0.15239:  # 15.239% chance of regional
                self.state = "regional"
            else:  # 17% chance of distant
                self.state = "distant"
    
    def _state_DCIS(self, risk3):
        # DCIS progression logic
        years_in_stage = int(self.time_in_state)

        # Progression probabilities
        progression_to_localized = 0.031  # 3.1% chance per year to localized https://pmc.ncbi.nlm.nih.gov/articles/PMC4641372/
        progression_to_regional = 0.031  # 3.1% chance per year to regional https://pmc.ncbi.nlm.nih.gov/articles/PMC4641372/
        progression_to_distant = 0.031  # 3.1% chance per year to distant https://pmc.ncbi.nlm.nih.gov/articles/PMC4641372/

        # Progression to localized, regional, or distant
        rand = random.random()
        if rand < progression_to_localized:
            self.state = "localized"
        elif rand < progression_to_localized + progression_to_regional:
            self.state = "regional"
        elif rand < progression_to_localized + progression_to_regional + progression_to_distant:
            self.state = "distant"

        # Remain in DCIS if no progression

    def _state_cancerous_early(self, risk3):
        # Determine if the cancer is localized or regional
        cancer_type = random.choices(["localized", "regional"], weights=[0.724, 0.276])[0]  # Weights from SEER dataset

        # Get the survival probability for the current year in the early stage
        years_in_stage = int(self.time_in_state)
        if years_in_stage < len(survival_probabilities[cancer_type]):
            survival_probability = survival_probabilities[cancer_type][years_in_stage]
        else:
# Use the last available survival probability for years beyond 5
            survival_probability = survival_probabilities[cancer_type][-1]

        # Predict mortality
        if random.random() > survival_probability:
            self.state = "dead - cancer"
            return

    def _state_regional(self, risk3):
        # Get the survival probability for the current year in the regional stage
        years_in_stage = int(self.time_in_state)
        if years_in_stage < len(survival_probabilities["regional"]):
            survival_probability = survival_probabilities["regional"][years_in_stage]
        else:
            survival_probability = survival_probabilities["regional"][-1]

        # Predict mortality
        if random.random() > survival_probability:
            self.state = "dead - cancer"
            return

    def _state_cancerous_late(self, risk4):
        # Use survival probabilities for distant cancer
        cancer_type = "distant"  # Late-stage cancer corresponds to "distant"

        # Get the survival probability for the current year in the late stage
        years_in_stage = int(self.time_in_state)
        if years_in_stage < len(survival_probabilities[cancer_type]):
            survival_probability = survival_probabilities[cancer_type][years_in_stage]
        else:
# Use the last available survival probability for years beyond 5
            survival_probability = survival_probabilities[cancer_type][-1]

        # Predict mortality
        if random.random() > survival_probability:
            self.state = "dead - cancer"

