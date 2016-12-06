import matplotlib.pyplot as plt
import numpy as np


class VisualizationStrategy:
    def __init__(self):
        pass
    # Homemade enumeration
    Plot, CSV, ASCII = range(3)


def determine_date(grouped_reviews):

    max_date = grouped_reviews[0][0].date
    min_date = grouped_reviews[0][0].date

    for group in grouped_reviews:
        for review in group:
            if min_date > review.date:
                min_date = review.date
            if max_date < review.date:
                max_date = review.date
    return min_date, max_date


# TODO optimized to not call this one everytime
def get_dated_title(title, grouped_reviews):
    """
    Return the title with a proper date
    :param title:
    :param grouped_reviews:
    :return:
    """
    min_date, max_date = determine_date(grouped_reviews)
    if min_date.year == max_date.year:
        title += " (%d)" % max_date.year
    else:
        title += " (%d to %d)" % (min_date.year, max_date.year)
    return title


def plot_mean_ratings(grouped_reviews, reviewers):
    """

    :param grouped_reviews:
    :param reviewers:
    :return:
    """
    means = []
    for index, group in enumerate(grouped_reviews):
        ratings = [x.rating for x in group]
        means.append(np.mean(ratings))
        reviewers[index] += " \n (%d)" % len(group)

    plt.bar(range(len(grouped_reviews)), means, align='center')
    plt.xticks(range(len(grouped_reviews)), reviewers)

    plt.xlabel("Reviewer")
    plt.ylabel("Mean rating")
    plt.legend(loc='upper left')
    plt.title(get_dated_title("Mean rating given by GK reviewers", grouped_reviews))
    plt.show()


def plot_variance_ratings(grouped_reviews, reviewers):
    """

    :param grouped_reviews:
    :param reviewers:
    :return:
    """
    ratings = []
    variances = []
    for group in grouped_reviews:
        ratings.append(list(r.rating for r in group))
    for idx, ratings_by_reviewer in enumerate(ratings):
        variances.append(np.var(ratings_by_reviewer, 0))
    plt.bar(range(len(grouped_reviews)), variances, align='center')
    plt.xticks(range(len(grouped_reviews)), reviewers)

    plt.xlabel("Reviewer")
    plt.ylabel("Variance ")
    plt.legend(loc='upper left')
    plt.title(get_dated_title("Variance of the ratings given by GK reviewers", grouped_reviews))
    plt.show()


