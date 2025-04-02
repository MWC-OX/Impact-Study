from person import Person
from time import time

class Simulator:

    def __init__(self):
        self.data = []


    def simulate_person(self, upper=80, lower=20, dt=1):

        subject = Person.generate_person(upper, lower)
        result = {"age": [], "state": [], "risk score": [], "bmi": []}

        result["race"] = subject.ethn

        while subject.get_state() not in ["dead - cancer", "dead - other"]:

            result["age"].append(subject.age)
            result["state"].append(subject.get_state())
            # result["risk score"].append(subject.get_risk_score())
            # result["bmi"].append(subject.get_bmi())

            subject.tic(dt)

        result["age"].append(subject.age)
        result["state"].append(subject.get_state())
        
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

if __name__ == "__main__":
    sim = Simulator()
    n = 1000
    sim.simulate_population(n, 30.1, 30, 1)

    x = 0
    for person in sim.data:
        if "DCIS" in person["state"] or "localized" in person["state"] or "regional" in person["state"] or "distant" in person["state"]:
            x += 1
    y = 0
    for person in sim.data:
        if "dead - cancer" in person["state"]:
            y += 1
    
    
    print(f"{(x/n)*100:.2f}% got cancer")
    print(f"{(y/n)*100:.2f}% died from cancer")
    

    