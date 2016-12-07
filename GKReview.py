from datetime import datetime


class GKReview:
    # TODO add platform(s)
    def __init__(self, reviewer="default", title="default", review_link="default", rating=-1, date="17/07/1994"):
        self.reviewer = reviewer
        self.title = title
        self.link = review_link
        self.rating = int(rating)
        self.date = datetime.strptime(date, '%d/%m/%Y')
        self.content = ""

    def print_review(self):
        print(self.title, " ", self.rating, " by ", self.reviewer)

    def get_year(self):
        return self.date.year

    def get_rating(self):
        return self.rating

    def get_reviewer(self):
        return self.reviewer

    def get_metric(self, metric):
        if metric == 'rating':
            return self.rating
        elif metric == 'length':
            return len(self.content)
        elif metric == 'wordcount':  # Simple implementation
            return len(self.content.split(" "))
        else:
            return self.rating
