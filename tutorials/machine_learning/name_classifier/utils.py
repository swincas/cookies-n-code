import numpy as np
import pandas as pd

# Select which features to use to build the model
FEATURE_NAMES = ['num_chars','num_vowels', 'starts_with_vowel', \
                'ends_with_vowel','sum_letter_nums']

def load_data():
    males = np.loadtxt("./male_names.txt", dtype=str)
    females = np.loadtxt("./female_names.txt", dtype=str)
    return np.concatenate((males,females)),\
            np.concatenate((np.zeros_like(males,dtype=int),np.ones_like(females,dtype=int)))


def extract_features(names):
    names = np.array([name.upper() for name in names], dtype=str)
    num_chars = [len(name) for name in names]
    starts_with_vowel = [1 if name[0] in "AEIOUY" else 0 for name in names]
    ends_with_vowel = [1 if name[-1] in "AEIOUY" else 0 for name in names]
    num_vowels = [sum(map(name.count,"AEIOUY")) for name in names]
    sum_letter_nums = [sum([ord(letter.lower())-96 for letter in name]) for name in names]
    pos_first_vowel = []
    for name in names:
        found = False
        for idx,letter in enumerate(name):
            if letter in "AEIOUY":
                pos_first_vowel.append(idx)
                found = True
                break
        if not found:
            pos_first_vowel.append(-1)


    features = pd.DataFrame()
    features['names'] = names
    features['num_chars'] = num_chars
    features['num_vowels'] = num_vowels
    features['starts_with_vowel'] = starts_with_vowel
    features['ends_with_vowel'] = ends_with_vowel
    features['sum_letter_nums'] = sum_letter_nums
    features['pos_first_vowel'] = pos_first_vowel

    return features[FEATURE_NAMES]
