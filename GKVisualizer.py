import matplotlib.pyplot as plt
import numpy as np


def plot_mean_ratings(grouped_reviews, reviewers):

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
    plt.title("Mean rating given by GK reviewers")
    plt.show()


def plot_variance_ratings(grouped_reviews, reviewers):
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
    plt.title("Variance of the ratings given by GK reviewers")
    plt.show()

