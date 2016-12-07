import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


class GKFeatureSelector:
    RFE, KBest = range(2)

    def __init__(self):
        # self.method = method
        pass

    def perform_feature_selection(self, bag_of_words, classes, nb_words):
        # TODO Cross validation ;)
        # feature selection
        print("Performing feature selection on ", bag_of_words.shape[0], " reviews")
        support = None
        choosen_scores = None

        """
        if self.method == GKFeatureSelector.RFE:
            model = LogisticRegression()
            rfe = RFE(model, nb_words)
            fit = rfe.fit(bag_of_words, classes)
            support = fit.support_
        elif self.method == GKFeatureSelector.KBest:
        """
        selector = SelectKBest(chi2, k=nb_words)
        selector.fit(bag_of_words, classes)
        scores = -np.log10(selector.pvalues_)
        support = selector.get_support()
        choosen_scores = scores[selector.get_support()]
        return support, choosen_scores



