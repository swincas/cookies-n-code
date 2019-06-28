from __future__ import print_function

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.model_selection import RandomizedSearchCV
import matplotlib.pyplot as plt
from utils import load_data, extract_features, FEATURE_NAMES
from sklearn.externals import joblib

# Laod data and extract features
names,y = load_data()
features = extract_features(names)

# Select which features to use to build the model
#feature_names = ['num_chars','num_vowels', 'starts_with_vowel', \
        #'ends_with_vowel','sum_letter_nums']

# Create a grid of hyperparameters
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 500, num = 5)]

# Number of features to consider at every split
max_features = ['auto', 'sqrt']

# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(2, 10, num = 5)]
max_depth.append(None)

# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]

# Method of selecting samples for training each tree
bootstrap = [False,True]

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


# Use the random grid to search for best hyperparameters
# First create the base model to tune
clf = RFC()

# Random search of parameters, using 3 fold cross validation, 
clf_random = RandomizedSearchCV(estimator = clf, param_distributions = random_grid,
        n_iter = 50, cv = 3, verbose=2, random_state=42, n_jobs = 4)

# Fit the random search model
clf_random.fit(features, y)

# Use the best hyperparameter setup to retrain the model
clf = RFC(**clf_random.best_params_)
clf.fit(features, y)

print("-"*79)
print("Feature names and their importances:")
print(FEATURE_NAMES)
print(clf.feature_importances_)

# Save model
if not os.path.exists("./model"):
    os.mkdir("./model")
joblib.dump(clf, "./model/finalised_model.sav")
