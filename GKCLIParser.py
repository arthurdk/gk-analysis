import argparse


class GKCLIParser:
    def __init__(self):
        self.DEFAULT_NB_PAGE = 10

    def do_parse_args(self):
        # TODO Make this parsing GREAT again
        parser = argparse.ArgumentParser(description='Perform analysis on Gamekult reviews.',
                                         formatter_class=argparse.RawTextHelpFormatter)
        # Optional parameters
        parser.add_argument('-F', '--force-dl', action='store_true',
                            help='Force download even if there is cache (default: false)')
        parser.add_argument('-C', '--no-cache', action='store_true',
                            help='Disable data caching (default: false)')

        subparsers = parser.add_subparsers(help='Available commands', dest='command')
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('-R', '--reviewers', metavar='reviewers', nargs="?",
                                   help='List of reviewers to visualize \n'
                                        'Example: "Stoon,Gautoz"', type=str)
        parent_parser.add_argument('-Y', '--filter-by-year', metavar='year', type=int,
                                   help='Visualize data for a particular year')
        parent_parser.add_argument('--rating-le', metavar='rating', type=int,
                                   help='Filter review having ratings less or equals than the given one')
        parent_parser.add_argument('--rating-ge', metavar='rating', type=int,
                                   help='Filter review having ratings greater or equals than the given one')
        parent_parser.add_argument('--rating-eq', metavar='rating', type=int,
                                   help='Filter review having a rating equals to the given one')
        group_by_choices = ["reviewer", "year"]
        parent_parser.add_argument('-G', '--group-by', metavar='by', nargs='?',
                                   help='Determine how to group by data (Default: data grouped by reviewer) '
                                        "\nList of options:\n- " + "\n- ".join(group_by_choices),
                                   choices=group_by_choices, default='reviewer')

        visualize_commands = ["variance", "mean", "scatter"]
        # Visualization parser
        parser_visualize = subparsers.add_parser('visualize', help='See visualization help for more information',
                                                 formatter_class=argparse.RawTextHelpFormatter,
                                                 parents=[parent_parser])
        parser_visualize.add_argument('visualize_command', metavar='command', nargs="+",
                                      help="List of available visualization commands: \n"
                                           "- " + "\n- ".join(visualize_commands),
                                      choices=visualize_commands)
        metric_choices = ["rating", "length", "wordcount"]
        parser_visualize.add_argument('-M', '--metric', metavar='metric',
                                      help='Determine which metric to analyze (Default: Rating) '
                                           "\nList of options:\n- " + "\n- ".join(metric_choices),
                                      choices=metric_choices, default='rating')
        # Fetch parser
        parser_fetch = subparsers.add_parser('fetch', help='Fetch data from Gamekult')
        parser_fetch.add_argument('-N', '--nb_page', metavar="nb_page", type=int,
                                  help="Number of page containing reviews to fetch (Default: 10)",
                                  default=self.DEFAULT_NB_PAGE, nargs='?')
        '''
        parser_fetch.add_argument('-T', '--translate', action='store_true',
                                  help="Translate reviews")
        '''
        # Analyse parser
        analyse_parent_parser = argparse.ArgumentParser(add_help=False)
        parser_analyse = subparsers.add_parser('analyse', help='Analyse data see help for more information',
                                               parents=[parent_parser, analyse_parent_parser])
        analyse_parent_parser.add_argument('-N', '--nb_words', metavar="nb_words", type=int,
                                           help="Number of best ranked words to select (Default: 100)",
                                           default=500, nargs='?')
        sub_parser_analyse = parser_analyse.add_subparsers(help='Available analyse commands', dest='analyse_commands')

        ## Word cloud command
        parser_word_cloud = sub_parser_analyse.add_parser('words', help='See words help for more information',
                                                          formatter_class=argparse.RawTextHelpFormatter,
                                                          parents=[parent_parser, analyse_parent_parser])
        parser_word_cloud.add_argument('--word-cloud-bg', metavar='color', default='white',
                                       help='Background color for the word cloud Example: black')
        parser_word_cloud.add_argument('--word-cloud-color-scheme', metavar='color_scheme',
                                       help="Color scheme for the word cloud (anything only grey is supported for now)")
        group = parser_word_cloud.add_mutually_exclusive_group()
        group.add_argument('--mask-url', metavar='url', help='URL of a mask for the wordcloud')
        group.add_argument('--mask-path', metavar='path-to-file', help='Path to a mask for the wordcloud')

        ## Review command
        parser_review = sub_parser_analyse.add_parser('review', help='See review help for more information',
                                                      formatter_class=argparse.RawTextHelpFormatter,
                                                      parents=[parent_parser, analyse_parent_parser])
        prediction_choices = ["reviewer", "rating"]
        parser_review.add_argument('predict_target', metavar='prediction',
                                   help="Choose which elment do you want to make prediction on "
                                        "\nList of options:\n- " + "\n- ".join(prediction_choices),
                                   choices=prediction_choices)
        parser_review.add_argument('review_path', metavar='filepath',
                                   help="Path to the review to analyse")

        # Actual parsing
        return parser.parse_args()
