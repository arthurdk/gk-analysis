from itertools import groupby
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.linear_model import LogisticRegression


class GKFeatureSelector:
    def __init__(self):
        pass

    @staticmethod
    def perform_feature_selection(bag_of_words, classes, nb_words):
        # TODO Cross validation ;)
        # feature selection
        print("Performing feature selection on ", bag_of_words.shape[0], " reviews")
        selector = SelectKBest(chi2, k=nb_words)
        selector.fit(bag_of_words, classes)
        scores = -np.log10(selector.pvalues_)
        selector.fit(bag_of_words, classes)
        return selector.get_support(), scores[selector.get_support()]



