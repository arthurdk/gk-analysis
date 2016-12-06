from datetime import datetime


class GKReview:
    # TODO add platform(s)
    def __init__(self, reviewer, title, review_link, rating, date):
        self.reviewer = reviewer
        self.title = title
        self.link = review_link
        self.rating = int(rating)
        self.date = datetime.strptime(date, '%d/%m/%Y')

    def print_review(self):
        print(self.title, " ", self.rating, " by ", self.reviewer)
