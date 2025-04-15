# hypperparameter tuning
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
import joblib  # Ensure this import is at the top of your file
from BCSC_encoder import encode_inputs
from time import time
# Assuming risk_unfiltered, X_train, y_train, sample_weight, X_val, y_val, and sample_weight_val are already defined

# Input arry size 1x12 to risk_prediction function to get the probability of cancer
# and either low, medium, significant or high for each feature - in function 
# risk_prediction - then to see which risk group just look t the thresholds

class classifier:

    def __init__(self):
        # Load the model and thresholds from the file
        data = joblib.load('dtree.joblib')
        self.best_clf = data['tree']
        self.thresholds = data['thresholds']


    def risk_prediction(self, risk_data):
        risk_data = np.array(risk_data).reshape(1, -1)
        
        # Predict the probability of cancer
        predicted_prob = self.best_clf.predict_proba(risk_data)[0][1]
        
        # Determine the risk category based on thresholds
        if predicted_prob <= self.thresholds[0]:
            risk_category = 1
        elif predicted_prob <= self.thresholds[1]:
            risk_category = 2
        elif predicted_prob <= self.thresholds[2]:
            risk_category = 3
        else:
            risk_category = 4
        
        # Print the risk category
        #print(f"Risk category: {risk_category}")
        return risk_category


if __name__ == "__main__":
    start = time()

    tree = classifier()
    print(f"took {time()-start}s to import")

    start = time()

    menopause = True
    age = 65
    breast_density = 2
    race = "WHITE"
    bmi = 30
    birth = -1
    rel = 0
    procedure = False
    mamo = False
    surg_meno = False
    hrt = False
    data = encode_inputs(menopause, age, breast_density, race, bmi, birth, rel, procedure, mamo, surg_meno, hrt)
    print(f"took {time()-start}s to infer")
    print( tree.risk_prediction(data) )

    



