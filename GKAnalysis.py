import GKFetcher as GKFetcher
from GKPreprocessor import *
from GKVisualizer import *
import GKSentiment as GKSentiment
import argparse

DEFAULT_NB_PAGE = 10


def main():
    parser = argparse.ArgumentParser(description='Perform analysis on Gamekult reviews.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Optional parameters
    parser.add_argument('-F', '--force-dl', action='store_true',
                        help='Force download even if there is cache (default: false)')
    parser.add_argument('-C', '--no-cache', action='store_true',
                        help='Disable data caching (default: false)')

    subparsers = parser.add_subparsers(help='Available commands', dest='command')
    visualize_commands = ["variance", "mean"]
    # Visualization parser
    parser_visualize = subparsers.add_parser('visualize', help='See visualization help for more information',
                                             formatter_class=argparse.RawTextHelpFormatter)
    parser_visualize.add_argument('visualize_command', metavar='command', nargs="+",
                                  help="List of available visualization commands: \n"
                                       "- " + "\n- ".join(visualize_commands),
                                  choices=visualize_commands)
    parser_visualize.add_argument('-R', '--reviewers', metavar='reviewers', nargs="?",
                                  help='List of reviewers to visualize \n'
                                       'Example: "Stoon,Gautoz"', type=str)
    group_by_choices = ["reviewer", "year"]
    parser_visualize.add_argument('-G', '--group-by', metavar='by',
                                  help='Determine how to group by data (Default: data grouped by reviewer) '
                                       "\nList of options:\n- " + "\n- ".join(group_by_choices),
                                  choices=group_by_choices, default='reviewer')
    metric_choices = ["rating", "length", "wordcount"]
    parser_visualize.add_argument('-M', '--metric', metavar='metric',
                                  help='Determine which metric to analyze (Default: Rating) '
                                       "\nList of options:\n- " + "\n- ".join(metric_choices),
                                  choices=metric_choices, default='rating')
    parser_visualize.add_argument('-Y', '--filter-by-year', metavar='year', type=int,
                                  help='Visualize data for a particular year')
    # Fetch parser
    parser_fetch = subparsers.add_parser('fetch', help='Fetch data from Gamekult')
    parser_fetch.add_argument('-N', '--nb_page', metavar="nb_page", type=int,
                              help="Number of page containing reviews to fetch (Default: 10)",
                              default=DEFAULT_NB_PAGE, nargs='?')
    '''
    parser_fetch.add_argument('-T', '--translate', action='store_true',
                              help="Translate reviews")
    '''
    # Analyse parser
    parser_analyse = subparsers.add_parser('analyse', help='Analyse data (sentiment analysis)')
    analyse_command = ["sentiment"]
    parser_analyse.add_argument('analyse_command', metavar='command', nargs="+",
                                help="List of available analysing commands: \n"
                                     "- " + "\n- ".join(analyse_command),
                                choices=analyse_command)
    # Actual parsing
    args = parser.parse_args()
    # print(args)
    reviews = []
    nb_page = DEFAULT_NB_PAGE

    if "nb_page" in args:
        nb_page = args.nb_page

    if args.command == 'fetch' or args.command == 'visualize':
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

    if args.command == 'visualize':
        pre_processor = GKPreprocessor(group_by_option=args.group_by, metric=args.metric)
        # Filtering
        if args.filter_by_year is not None:
            reviews = pre_processor.filter_by_year(reviews, args.filter_by_year)

        reviewers_filtering = []
        if args.reviewers is not None:
            reviewers_filtering = args.reviewers.split(",")
            reviews = GKPreprocessor.filter_by_reviewers(reviews, reviewers_filtering)
        reviews, labels = pre_processor.perform_group_by(reviews)
        visualizer = GKVisualizer(reviewers_filtering=reviewers_filtering, group_by_option=args.group_by)

        # Visualize all methods
        for method in args.visualize_command:
            if visualizer.group_by == 'nothing':
                getattr(visualizer, "plot_" + method)(reviews)
            else:
                data, anno_labels = getattr(pre_processor,
                                            "grouped_" + method)(reviews, labels)
                title = visualizer.get_named_title(method + " rating given by GK reviewers", reviewers_filtering)
                title = visualizer.get_dated_title(title, reviews)
                ylabel = method + " " + args.metric
                visualizer.group_plot(data=data,
                                      labels=anno_labels,
                                      ylabel=ylabel,
                                      title=title)


if __name__ == "__main__":
    main()
