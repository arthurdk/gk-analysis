from itertools import groupby


def group_by_reviewer(reviews):
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


def filter_by_year(reviews, year):
    return [x for x in reviews if x.date.year == year]

