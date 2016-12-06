from itertools import groupby
import numpy as np


class GKPreprocessor:
    def __init__(self, metric, group_by_option='nothing'):
        self.group_by = group_by_option
        self.metric = metric

    def perform_group_by(self, reviews):
        if self.group_by == "reviewer":
            return self._actual_group_by(reviews, "reviewer")
        elif self.group_by == "year":
            return self._actual_group_by(reviews, attr="date", second_attr="year")
        else:
            return reviews, []

    def grouped_mean(self, grouped_reviews, labels):
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

        print(labels)
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

