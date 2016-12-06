from itertools import groupby


def group_by_reviewer(reviews):
    """
    Group reviews by reviewer
    :param reviews:
    :return: group of reviews, and list of reviewers
    """
    groups = []
    reviewers = []
    sorted_reviews = sorted(reviews, key=lambda x: x.reviewer)
    for k, g in groupby(sorted_reviews, lambda x: x.reviewer):
        groups.append(list(g))  # Store group iterator as a list
        reviewers.append(k)
    return groups, reviewers


def older_than(reviews, date):
    return []


def in_range(reviews, begin, end):
    return []


def filter_by_reviewers(reviews, selected_reviewers):
    """
    Filter reviews by the reviewers given
    :param reviews:
    :param selected_reviewers:
    :return:
    """
    return [x for x in reviews if x.reviewer in selected_reviewers]


def filter_by_year(reviews, year):
    """
    Filter reviews for the year given
    :param reviews:
    :param year:
    :return: Filtered reviews
    """
    return [x for x in reviews if x.date.year == year]

