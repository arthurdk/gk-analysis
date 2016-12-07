from itertools import groupby
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.linear_model import LogisticRegression


class GKPreprocessor:
    def __init__(self, metric='wordcount', group_by_option='reviewer'):
        self.group_by = group_by_option
        self.metric = metric

    @staticmethod
    def construct_bag_of_words(reviews, class_attr):
        """
        Credits: https://www.dataquest.io/blog/natural-language-processing-with-python/
        :param reviews:
        :return:
        """
        vectorizer = CountVectorizer(lowercase=True, stop_words=get_stop_words('french'))
        contents = []
        classes = []
        for group in reviews:
            for review in group:
                contents.append(review.content)
                classes.append(getattr(review, class_attr))
        matrix = vectorizer.fit_transform(contents)
        vocab = np.array([word for word in vectorizer.vocabulary_])
        return matrix.todense(), classes, vocab

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

    def perform_group_by(self, reviews):
        """
        Group review following the group_by attr
        :param reviews:
        :return:
        """
        if self.group_by == "reviewer":
            return self._actual_group_by(reviews, "reviewer")
        elif self.group_by == "year":
            return self._actual_group_by(reviews, attr="date", second_attr="year")
        else:
            return reviews, []

    def grouped_mean(self, grouped_reviews, labels):
        """
        Compute the mean of each group
        :param grouped_reviews:
        :param labels:
        :return:
        """
        means = []
        annotated_labels = list(labels)
        for index, group in enumerate(grouped_reviews):
            metrics = [x.get_metric(self.metric) for x in group]
            means.append(np.mean(metrics))
            # Label annotation
            if isinstance(labels[index], basestring):
                annotated_labels[index] += " \n (%d)" % len(group)
            else:
                annotated_labels[index] = str(annotated_labels[index]) + " \n (%d)" % len(group)
        return means, annotated_labels

    def grouped_variance(self, grouped_reviews, labels):
        """
        Compute the variance of each group
        :param grouped_reviews:
        :param labels:
        :return:
        """
        metrics = []
        variances = []
        annotated_labels = list(labels)
        for group in grouped_reviews:
            metrics.append(list(r.get_metric(self.metric) for r in group))
        for idx, metrics_by_label in enumerate(metrics):
            variances.append(np.var(metrics_by_label, 0))
            # Label annotation
            if isinstance(labels[idx], basestring):
                annotated_labels[idx] += " \n (%d)" % len(metrics_by_label)
            else:
                annotated_labels[idx] = str(annotated_labels[idx]) + " \n (%d)" % len(metrics_by_label)
        return variances, annotated_labels

    @staticmethod
    def _actual_group_by(reviews, attr, second_attr=None):
        groups = []
        labels = []

        if second_attr is not None:
            sorted_reviews = sorted(reviews, key=lambda x: getattr(getattr(x, attr), second_attr))
            for k, g in groupby(sorted_reviews, lambda x: getattr(getattr(x, attr), second_attr)):
                groups.append(list(g))  # Store group iterator as a list
                labels.append(k)
        else:
            sorted_reviews = sorted(reviews, key=lambda x: getattr(x, attr))
            for k, g in groupby(sorted_reviews, lambda x: getattr(x, attr)):
                groups.append(list(g))  # Store group iterator as a list
                labels.append(k)

        return groups, labels

    @staticmethod
    def older_than(reviews, date):
        return []

    @staticmethod
    def in_range(reviews, begin, end):
        return []

    @staticmethod
    def filter_by_reviewers(reviews, selected_reviewers):
        """
        Filter reviews by the reviewers given
        :param reviews:
        :param selected_reviewers:
        :return:
        """
        return [x for x in reviews if x.reviewer in selected_reviewers]

    @staticmethod
    def filter_by_year(reviews, year):
        """
        Filter reviews for the year given
        :param reviews:
        :param year:
        :return: Filtered reviews
        """
        return [x for x in reviews if x.date.year == year]

    @staticmethod
    def filter_by_rating(reviews, rating_option, rating):
        """

        :param reviews:
        :param rating_option:
        :param rating:
        :return:
        """
        if rating_option == "rating_le":
            return [x for x in reviews if x.rating <= rating]
        if rating_option == "rating_ge":
            return [x for x in reviews if x.rating >= rating]
        if rating_option == "rating_eq":
            return [x for x in reviews if x.rating == rating]
        else:
            return reviews
