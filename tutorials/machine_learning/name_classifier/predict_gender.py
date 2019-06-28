from __future__ import print_function

from sklearn.externals import joblib
import sys
from utils import load_data,extract_features


if len(sys.argv) < 2:
    print("Please enter a name...")
    print("Usage: python %s name" %sys.argv[0])
    sys.exit(-1)

print("Predicting gender of: '%s'" %sys.argv[1])
unknown_name = [sys.argv[1]]

print("Loading model")
clf = joblib.load("./model/finalised_model.sav")

f = extract_features(unknown_name)
gender = "Female" if clf.predict(f).squeeze() else "Male"

print("'%s' is a: '%s'" %(unknown_name[0],gender))
