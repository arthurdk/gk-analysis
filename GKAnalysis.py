import GKFetcher as GKFetcher
import GKPreprocessor as GKPreprocessor
import GKVisualizer as GKVisualizer
import argparse


def main():
    parser = argparse.ArgumentParser(description='Perform analysis on Gamekult reviews.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Optional parameters
    parser.add_argument('-F', '--force-dl', action='store_true',
                        help='Force download even if there is cache (default: false)')
    parser.add_argument('-C', '--no-cache', action='store_true',
                        help='Disable data caching (default: false)')
    parser.add_argument('-Y', '--filter-by-year', metavar='year', type=int,
                        help='Visualize data for a particular year')
    subparsers = parser.add_subparsers(help='Available commands', dest='command')
    commands = ["variance", "mean"]
    parser_visualize = subparsers.add_parser('visualize', help='See visualiation help for more information',
                                             formatter_class=argparse.RawTextHelpFormatter)
    parser_visualize.add_argument('visualize_command', metavar='command', nargs="+",
                                  help="List of available visualization commands: \n"
                                       "- " + "\n- ".join(commands),
                                  choices=commands)
    parser_visualize.add_argument('nb_page', metavar="nb_page", type=int,
                              help="Number of page containing reviews to fetch (Default: 10)",
                              default=10, nargs='?')
    parser_fetch = subparsers.add_parser('fetch', help='Fetch data from Gamekult')
    parser_fetch.add_argument('nb_page', metavar="nb_page", type=int,
                              help="Number of page containing reviews to fetch (Default: 10)",
                              default=10, nargs='?')
    args = parser.parse_args()

    reviews = []

    if args.command == 'fetch' or args.command == 'visualize':
        reviews = GKFetcher.fetch_parse_full_tests(force_download=args.force_dl,
                                                   cache=not args.no_cache,
                                                   nb_page=args.nb_page)
        if args.filter_by_year is not None:
            reviews = GKPreprocessor.filter_by_year(reviews, args.filter_by_year)
    if args.command == 'visualize':
        grouped_reviews, reviewers = GKPreprocessor.group_by_reviewer(reviews)
        if "variance" in args.visualize_command:
            GKVisualizer.plot_variance_ratings(grouped_reviews, reviewers)
        if "mean" in args.visualize_command:
            GKVisualizer.plot_mean_ratings(grouped_reviews, reviewers)


if __name__ == "__main__":
    main()
