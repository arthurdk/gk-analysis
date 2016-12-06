

class GKFilterer:
    def __init__(self, pre_processor):
        self.pre_processor = pre_processor
        self.reviewers_filtering = []
        self.rating_filters = []

    def do_filter(self, reviews, args):
        if args.filter_by_year is not None:
            reviews = self.pre_processor.filter_by_year(reviews, args.filter_by_year)

        if args.reviewers is not None:
            self.reviewers_filtering = args.reviewers.split(",")
            reviews = self.pre_processor.filter_by_reviewers(reviews, self.reviewers_filtering)

        if args.rating_le is not None:
            reviews = self.pre_processor.filter_by_rating(reviews, rating=args.rating_le, rating_option="rating_le")
            self.rating_filters.append(("<=", args.rating_le))

        if args.rating_ge is not None:
            reviews = self.pre_processor.filter_by_rating(reviews, rating=args.rating_ge, rating_option="rating_ge")
            self.rating_filters.append((">=", args.rating_ge))

        if args.rating_eq is not None:
            reviews = self.pre_processor.filter_by_rating(reviews, rating=args.rating_eq, rating_option="rating_eq")
            self.rating_filters.append(("=", args.rating_eq))

        return reviews