from math import sqrt
def get_data(filename):

    # reads in file
    with open(filename, "r") as f:
        data = f.read()

    # splits each entry
    data = data.split("\n")

    # removes last line which is " "
    data.pop()

    #makes each entry a list
    data = [x.split(" ") for x in data]

    #remove blank ("") entries and makes data intergers
    for idx, val in enumerate(data):
        data[idx] = [int(x) for x in val if x != ""]
    
    return data

def check_subject_to(entry, subject_to):
    # checks if the entry meets requirements of for {collumn: value, collum, value, ...}
    for collum, value in subject_to.items():
        if entry[collum - 1] != value:
            return False
    return True



def get_distribution(data, target_index, ignore_values=[], subject_to={}, bin_centre=[]):

    # get highest entry
    maximum = 0
    for x in data:
        if x[target_index - 1] > maximum and x[target_index - 1] not in ignore_values:
            maximum = x[target_index - 1]

    # make list to store distribution
    counts = [0 for x in range(0, maximum + 1)]

    # for each entry check its not got a value to ignore 
    # and meets the prior criteria
    for entry in data:
        if entry[target_index - 1] not in ignore_values and check_subject_to(entry, subject_to):
            counts[ entry[target_index - 1] ] += entry[riskEstimation.count - 1]

    
    if bin_centre == []:
        return sum(counts), [x / sum(counts) for x in counts]
    
    x_bar = sum([val * bin_centre[idx] for idx, val in enumerate(counts)]) / sum(counts)
    var = sum([val*((bin_centre[idx] - x_bar)**2) for idx, val in enumerate(counts)]) /sum(counts)

    return sum(counts), [x / sum(counts) for x in counts], x_bar, sqrt(var)
        

class riskEstimation:
    # Index values for each collumn
    menopause = 1
    age_group = 2
    density = 3
    race = 4
    hispanic = 5
    bmi = 6
    age_first_birth = 7
    relatives = 8
    prev_brest_procedure = 9
    last_mammogram = 10
    surgical_menopause = 11
    hrt = 12
    invasive_cancer = 13
    cancer = 14
    training_data = 15
    count = 16



if __name__ == "__main__":

    # Import data
    data = get_data("risk.txt")
    
    # get the distribution
    total, distribution, mean, var = get_distribution(data, riskEstimation.bmi, [9], {riskEstimation.age_group: 10}, bin_centre=[0, 20, 27.5, 32.5, 40])

    # print out
    print(f"data collected from {total} entries")
    for idx, val in enumerate(distribution):
        print(f"{idx}: {val * 100:.2f}%")
    
    print(f"\nMean: {mean:.2f}\ndeviation: {var:.2f}")
        



    

