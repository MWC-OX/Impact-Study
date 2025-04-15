from person import Person
from time import time

class Simulator:

    def __init__(self):
        self.data = []


    def simulate_person(self, age, dt=1):

        subject = Person.generate_person(age)
        result = {"age": [], "state": [], "risk score": [], "bmi": []}

        result["race"] = subject.ethn

        while subject.get_state() not in ["dead - cancer", "dead - other"]:

            result["age"].append(subject.age)
            result["state"].append(subject.get_state())
            result["risk score"].append(subject.risk_level)
            # result["bmi"].append(subject.get_bmi())

            subject.tic(dt)

        result["age"].append(subject.age)
        result["state"].append(subject.get_state())
        result["self detect"] = subject.state.self_detect
        result["screen detect"] = subject.state.screen_detect
        
        result["screen costs"] = subject.screen_cost

        self.data.append(result)


    def simulate_population(self, n=1000, upper=80, lower=20, dt=1):

        self.clear_data()
        tic = time()

        for x in range(n):
            self.simulate_person(30, dt)

            if x % 100 == 0 and x != 0:
                print(f"Simulated {x} people")

        print(f"Simulation completed in {time() - tic:.2f} seconds")
        return self.data
    
    def clear_data(self):
        self.data = []

if __name__ == "__main__":
    sim = Simulator()
    n = 100
    sim.simulate_population(n, 30, 1)
    y = 0
    screen = 0
    self = 0
    for x in sim.data:
        screen += x["screen detect"]
        self += x["self detect"]
        if "dead - cancer" in x["state"]:
            y += 1

    print(f"{(self/(self+screen))*100:.2f}% of cancer cases self detected (n={self+screen})")
    print(f"{(y/n)*100:.2f}% die of breast cancer")


    

    