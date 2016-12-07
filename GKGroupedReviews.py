from itertools import groupby


class GKGroupedReviews():
    def __init__(self, reviews, group_by_option):
        self.flat_reviews = reviews
        self.group_by_option = group_by_option
        self.labels = []
        self.second_level_labels = []
        self.grouped_reviews = []

    def get_depth(self):
        return self.group_by_option.count('_') + 1

    def get_flat_reviews(self):
        return self.flat_reviews

    def get_group_by_option(self):
        return self.group_by_option

    def perform_group_by(self):
        """
        Group review following the group_by attr
        :param flat_reviews:
        :return:
        """
        grouped_reviews = []
        labels = []
        # TODO habdle labels for double grouped data
        if self.group_by_option == "reviewer":
            grouped_reviews, labels = self._actual_group_by(self.flat_reviews, "reviewer")
        elif self.group_by_option == "year":
            grouped_reviews, labels = self._actual_group_by(self.flat_reviews, attr="date", second_attr="year")
        elif self.group_by_option == "year_reviewer":
            top_level_grouped_reviews, labels = self._actual_group_by(self.flat_reviews, attr="date", second_attr="year")
            for idx, group in enumerate(top_level_grouped_reviews):
                grouped_reviews_low, tmp_labels = self._actual_group_by(group, "reviewer")
                self.second_level_labels.append(tmp_labels)
                grouped_reviews.append(grouped_reviews_low)

        elif self.group_by_option == "reviewer_year":
            top_level_grouped_reviews, labels = self._actual_group_by(self.flat_reviews, "reviewer")
            for idx, group in enumerate(top_level_grouped_reviews):
                grouped_reviews_low, tmp_labels = self._actual_group_by(group, attr="date", second_attr="year")
                self.second_level_labels.append(tmp_labels)
                grouped_reviews.append(grouped_reviews_low)
        else:
            raise ValueError("Option Unknown")

        self.grouped_reviews = grouped_reviews
        self.labels = labels

        return self.grouped_reviews, labels

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