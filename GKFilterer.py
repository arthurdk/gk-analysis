

class GKFilterer:
    def __init__(self):
        self.reviewers_filtering = []
        self.rating_filters = []

    def do_filter(self, reviews, args):
        if args.filter_by_year is not None:
            reviews = self.filter_by_year(reviews, args.filter_by_year)

        if args.reviewers is not None:
            self.reviewers_filtering = args.reviewers.split(",")
            reviews = self.filter_by_reviewers(reviews, self.reviewers_filtering)

        if args.rating_le is not None:
            reviews = self.filter_by_rating(reviews, rating=args.rating_le, rating_option="rating_le")
            self.rating_filters.append(("<=", args.rating_le))

        if args.rating_ge is not None:
            reviews = self.filter_by_rating(reviews, rating=args.rating_ge, rating_option="rating_ge")
            self.rating_filters.append((">=", args.rating_ge))

        if args.rating_eq is not None:
            reviews = self.filter_by_rating(reviews, rating=args.rating_eq, rating_option="rating_eq")
            self.rating_filters.append(("=", args.rating_eq))

        return reviews

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

    @staticmethod
    def filter_by_rating(reviews, rating_option, rating):
        """

        :param reviews:
        :param rating_option:
        :param rating:
        :return:
        """
        if rating_option == "rating_le":
            return [x for x in reviews if x.rating <= rating]
        if rating_option == "rating_ge":
            return [x for x in reviews if x.rating >= rating]
        if rating_option == "rating_eq":
            return [x for x in reviews if x.rating == rating]
        else:
            return reviews
