import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from words_builder import Words_Builder


def get_csv(csv_path):
    f1 = open('classifier.pickle', 'rb')
    rf = pickle.load(f1)
    f1.close()

    f2 = open('word_builder.pickle', 'rb')
    wb = pickle.load(f2)
    f2.close()
    wb.onehot_test(csv_path)
    result = rf.predict(wb.ts_oh_x.astype(int))
    return list(result)
