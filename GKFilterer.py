

class GKFilterer:
    def __init__(self):
        self.reviewers_filtering = []
        self.rating_filters = []

    def do_filter(self, reviews, args):
        if args.year_le is not None:
            reviews = self.filter_by_attribute(reviews, cmp_item=args.year_le, cmp_option="le", attr="year")

        if args.year_eq is not None:
            reviews = self.filter_by_attribute(reviews, cmp_item=args.year_eq, cmp_option="le", attr="year")

        if args.year_ge is not None:
            reviews = self.filter_by_attribute(reviews, cmp_item=args.year_ge, cmp_option="le", attr="year")

        if args.reviewers is not None:
            self.reviewers_filtering = args.reviewers.split(",")
            reviews = self.filter_by_reviewers(reviews, self.reviewers_filtering)

        if args.rating_le is not None:
            reviews = self.filter_by_attribute(reviews, cmp_item=args.rating_le, cmp_option="le", attr="rating")
            self.rating_filters.append(("<=", args.rating_le))

        if args.rating_ge is not None:
            reviews = self.filter_by_attribute(reviews, cmp_item=args.rating_ge, cmp_option="ge", attr="rating")
            self.rating_filters.append((">=", args.rating_ge))

        if args.rating_eq is not None:
            reviews = self.filter_by_attribute(reviews, cmp_item=args.rating_eq, cmp_option="eq", attr="rating")
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
    def filter_by_attribute(reviews, cmp_option, cmp_item, attr):
        """

        :param reviews:
        :param cmp_option:
        :param cmp_item:
        :param attr:
        :return:
        """
        if cmp_option == "le":
            return [x for x in reviews if getattr(x, "get_" + attr)() <= cmp_item]
        if cmp_option == "ge":
            return [x for x in reviews if getattr(x, "get_" + attr)() >= cmp_item]
        if cmp_option == "eq":
            return [x for x in reviews if getattr(x, "get_" + attr)() == cmp_item]
        else:
            return reviews
