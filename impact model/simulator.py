from person import Person
from time import time

class Simulator:

    def __init__(self):
        self.data = []


    def simulate_person(self, age, scheme, dt):

        subject = Person.generate_person(age, scheme)
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


    def simulate_population(self, n, age, scheme, dt, only_cancer):

        def has_cancer(states):
            cancer_states = {"DCIS", "localized", "regional", "distant", 
                     "DCIS - detected", "localized - detected", 
                     "regional - detected", "distant - detected", 
                     "dead - cancer"}
            return any(state in cancer_states for state in states)

        self.clear_data()
        printed = False
        tic = time()

        while len(self.data) < n:
            self.simulate_person(age, scheme, dt)
            if only_cancer and not has_cancer(self.data[-1]["state"]):
                self.data.pop()
            else:
                printed = False

            if len(self.data) % 100 == 0 and len(self.data) != 0 and not only_cancer:
                print(f"Simulated {len(self.data)} people")
            if len(self.data) % 10 == 0 and len(self.data) != 0 and only_cancer and not printed:
                printed = True
                print(f"Simulated {len(self.data)} people")

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


    

    