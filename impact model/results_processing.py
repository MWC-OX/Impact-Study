from simulator import Simulator
import matplotlib.pyplot as plt
import numpy as np

# https://pmc.ncbi.nlm.nih.gov/articles/PMC8526485/
QALY_utility = {
    "healthy": 1,
    "DCIS": 0.99,
    "DCIS - detected": 0.95,
    "localized": 0.73,
    "localized - detected": 0.73 - 0.05,
    "regional": 0.61,
    "regional - detected": 0.61 - 0.05,
    "distant": 0.5,
    "distant - detected": 0.5 - 0.05,
    "dead - cancer": 0,
    "dead - other": 0
}

# localsied + reigonal https://www.valueinhealthjournal.com/article/S1098-3015(20)32123-9/fulltext
cost = {
    "DCIS - detected": 5167,
    "localized - detected": 5167,
    "regional - detected": 7613,
    "distant - detected": 13330
}

if __name__ == "__main__":
    sim = Simulator()
    n = 1000  # Number of people to simulate
    sim.simulate_population(n, 30, 1)

    total_qalys = 0
    total_cost = 0
    deaths_cancer = 0

    for person_data in sim.data:
        # Calculate QALYs for the person
        qalys = sum(QALY_utility.get(state, 0) for state in person_data["state"])
        total_qalys += qalys

        # Calculate costs for the person
        detected_cost = sum(cost.get(state, 0) for state in person_data["state"])
        total_cost += detected_cost + person_data["screen costs"]

        # Count deaths due to cancer
        if "dead - cancer" in person_data["state"]:
            deaths_cancer += 1

    # Calculate averages
    avg_qalys = total_qalys / n
    avg_cost = total_cost / n
    cancer_death_percentage = (deaths_cancer / n) * 100

    # Print results
    print("--------------------------------------------------------")
    print(f"{cancer_death_percentage:.2f}% die of breast cancer")
    print(f"Average QALYs per person: {avg_qalys:.2f}")
    print(f"Average total cost per person: {avg_cost:.2f} pounds")


