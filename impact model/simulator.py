from person import Person
from time import time

class Simulator:

    def __init__(self):
        self.data = []


    def simulate_person(self, upper=80, lower=20, dt=1):

        subject = Person.generate_person(upper, lower)
        result = {"age": [], "state": [], "risk score": [], "bmi": []}

        result["race"] = subject.get_race()

        while subject.get_state() != "DEAD":

            result["age"].append(subject.get_age())
            result["state"].append(subject.get_state())
            result["risk score"].append(subject.get_risk_score())
            result["bmi"].append(subject.get_bmi())

            subject.tic(dt)
        
        result["costs"] = subject.b_cancer_costs

        self.data.append(result)


    def simulate_population(self, n=1000, upper=80, lower=20, dt=1):

        self.clear_data()
        tic = time()

        for x in range(n):
            self.simulate_person(upper, lower, dt)

            if x % 100 == 0:
                print(f"Simulated {x} people")

        print(f"Simulation completed in {time() - tic:.2f} seconds")
        return self.data
    
    def clear_data(self):
        self.data = []

    

