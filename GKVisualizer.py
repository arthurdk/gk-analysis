import matplotlib.pyplot as plt
import numpy as np

'''
class VisualizationStrategy:
    def __init__(self):
        pass
    # Homemade enumeration
    Plot, CSV, ASCII = range(3)

'''


class GKVisualizer:

    def __init__(self, reviewers_filtering, group_by_option='nothing'):
        self.reviewers_filtering = reviewers_filtering
        self.group_by = group_by_option



    @staticmethod
    def _determine_min_max(reviews, min_date, max_date):
        for review in reviews:
            if min_date > review.date:
                min_date = review.date
            if max_date < review.date:
                max_date = review.date
        return min_date, max_date

    def determine_date(self, reviews):
        if self.group_by != 'nothing':
            max_date = reviews[0][0].date
            min_date = reviews[0][0].date

            for group in reviews:
                min_date, max_date = self._determine_min_max(reviews=group, min_date=min_date, max_date=max_date)
        else:
            max_date = reviews[0].date
            min_date = reviews[0].date
            min_date, max_date = self._determine_min_max(reviews=reviews, min_date=min_date, max_date=max_date)

        return min_date, max_date

    # TODO optimized to not call this one everytime
    def get_dated_title(self, title, grouped_reviews):
        """
        Return the title with a proper date
        :param title:
        :param grouped_reviews:
        :return:
        """
        min_date, max_date = self.determine_date(grouped_reviews)
        if min_date.year == max_date.year:
            title += " (%d)" % max_date.year
        else:
            title += " (%d to %d)" % (min_date.year, max_date.year)
        return title

    @staticmethod
    def get_named_title(title, reviewers):
        if len(reviewers) > 0:
            title += " (" + ", ".join(reviewers) + ") "
        return title

    def group_plot(self, data, labels, title, ylabel):
        plt.bar(range(len(data)), data, align='center')
        plt.xticks(range(len(data)), labels)
        plt.xlabel(self.group_by)
        plt.ylabel(ylabel)
        plt.legend(loc='upper left')
        plt.title(title)
        plt.show()

    # Unused anymore
    def plot_variance(self, reviews):
        ratings = [list(r.rating for r in reviews)]
        plt.bar(1, np.var(ratings))
        plt.xticks(range(1), ["Data"])
        plt.xlabel(self.group_by)
        plt.ylabel("Variance ")
        plt.legend(loc='upper left')
        title = self.get_named_title("Variance of the ratings given by GK reviewers", self.reviewers_filtering)
        plt.title(self.get_dated_title(title, reviews))
        plt.show()

    # Unused anymore
    def plot_mean(self, reviews):

        ratings = [x.rating for x in reviews]
        mean = np.mean(ratings)

        plt.bar(range(1), mean, align='center')
        plt.xticks(range(1), ["Data"])
        plt.xlabel(self.group_by)
        plt.ylabel("Mean rating")
        plt.legend(loc='upper left')
        title = self.get_named_title("Mean rating given by GK reviewers", self.reviewers_filtering)
        plt.title(self.get_dated_title(title, reviews))
        plt.show()
