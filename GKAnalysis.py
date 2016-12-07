# -*- coding: utf-8 -*-
from GKPreprocessor import *
from GKVisualizer import *
from GKFilterer import *
from GKCLIParser import *
from GKDispatcher import *
from GKFeatureSelector import *
import GKFetcher as GKFetcher


class GKAnalysis:

    def __init__(self):
        pass

    def start(self):
        cli_parser = GKCLIParser()
        args = cli_parser.do_parse_args()
        pre_processor = GKPreprocessor(group_by_option=args.group_by)
        filterer = GKFilterer()
        feat_selector = GKFeatureSelector()
        # print(args)

        reviews = []
        nb_page = cli_parser.DEFAULT_NB_PAGE

        if "nb_page" in args:
            nb_page = args.nb_page

        if args.command == 'fetch' or args.command == 'visualize' or args.command == 'analyse':
            reviews = GKFetcher.fetch_parse_full_tests(force_download=args.force_dl,
                                                       cache=not args.no_cache,
                                                       nb_page=nb_page)
            '''
            if args.translate is not None:
                reviews = GKFetcher.fetch_translation(reviews)
            '''

        ''' TODO implement in the right place!!!
        if args.command == "analyse":
            if "sentiment" in args.analyse_command:
                reviews = GKSentiment.perform_analysis(reviews, "content")
        '''

        reviews = filterer.do_filter(reviews=reviews, args=args)

        visualizer = GKVisualizer(reviewers_filtering=filterer.reviewers_filtering, group_by_option=args.group_by,
                                  rating_filters=filterer.rating_filters)
        # Perform Group By
        reviews, labels = pre_processor.perform_group_by(reviews)

        dispatcher = GKDispatcher(pre_processor=pre_processor, filterer=filterer, feat_selector=feat_selector,
                                  visualizer=visualizer, args=args)
        dispatcher.dispatch(reviews, labels)


def main():
    gk_analyser = GKAnalysis()
    gk_analyser.start()

if __name__ == "__main__":
    main()
