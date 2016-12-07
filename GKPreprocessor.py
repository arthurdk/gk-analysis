import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words


class GKPreprocessor:
    def __init__(self, metric='wordcount', group_by_option='reviewer'):
        self.group_by = group_by_option
        self.metric = metric

    @staticmethod
    def construct_bag_of_words(gk_grouped_reviews, class_attr):
        """

        :param gk_grouped_reviews:
        :param class_attr:
        :return:
        """
        vectorizer = CountVectorizer(lowercase=True, stop_words=get_stop_words('french'))
        contents = []
        classes = []
        for group in gk_grouped_reviews.grouped_reviews:
            for review in group:
                contents.append(review.content)
                classes.append(getattr(review, class_attr))
        matrix = vectorizer.fit_transform(contents)
        vocab = np.array([word for word in vectorizer.vocabulary_])
        return matrix.todense(), classes, vocab

    def grouped_stats(self, gk_grouped_reviews, method):
        grouped_reviews = gk_grouped_reviews.grouped_reviews
        labels = gk_grouped_reviews.labels

        if gk_grouped_reviews.get_depth() == 1:
            stats = []
            annotated_labels = list(labels)
            for index, group in enumerate(grouped_reviews):
                metrics = [x.get_metric(self.metric) for x in group]
                if method == "variance":
                    stats.append(np.var(metrics, 0))
                elif method == "mean":
                    stats.append(np.mean(metrics))
                # Label annotation
                if isinstance(labels[index], basestring):
                    annotated_labels[index] += " \n (%d)" % len(group)
                else:
                    annotated_labels[index] = str(annotated_labels[index]) + " \n (%d)" % len(group)
            return stats, annotated_labels
        else:  # double grouped data
            full_labels = []
            for label_list in gk_grouped_reviews.second_level_labels:
                full_labels += label_list
            full_labels = list(set(full_labels))
            _, option2 = self.group_by.split("_")
            stats = np.zeros(shape=(len(grouped_reviews), len(full_labels)))
            # annotated_labels = list(labels)
            for first_index, first_group in enumerate(grouped_reviews):
                for second_index, second_group in enumerate(first_group):
                    metrics = [x.get_metric(self.metric) for x in second_group]

                    getter = getattr(second_group[0], "get_"+option2)
                    if method == "variance":
                        stats[first_index][full_labels.index(getter())] = np.var(metrics, 0)
                    elif method == "mean":
                        stats[first_index][full_labels.index(getter())] = np.mean(metrics)

                    # Label annotation
            return stats, full_labels  # todo annotate labels

    def grouped_mean(self, gk_grouped_reviews):
        self.grouped_stats()
    def grouped_variance(self, gk_grouped_reviews):

        grouped_reviews = gk_grouped_reviews.grouped_reviews
        labels = gk_grouped_reviews.labels

        if gk_grouped_reviews.get_depth() == 1:
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
        else:  # double grouped data

            _, max_length_labels = max(enumerate(gk_grouped_reviews.second_level_labels), key=lambda tup: len(tup))
            _, max_size = max(enumerate(gk_grouped_reviews.grouped_reviews), key=lambda tup: len(tup))
            print(max_size)
            means = np.zeros(shape=(len(grouped_reviews), len(max_size)))
            # annotated_labels = list(labels)
            for first_index, first_group in enumerate(grouped_reviews):
                print("f", first_index, first_group[0][0].reviewer)
                for second_index, second_group in enumerate(first_group):
                    print("s", second_index, second_group[0].date.year)
                    metrics = [x.get_metric(self.metric) for x in second_group]
                    print(means)
                    means[first_index][max_length_labels.index(second_group[0].date.year)] = np.mean(metrics)
                    print(means)
                    # Label annotation
            print(means)
            return means, []

    @staticmethod
    def older_than(reviews, date):
        return []

    @staticmethod
    def in_range(reviews, begin, end):
        return []
