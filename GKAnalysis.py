# -*- coding: utf-8 -*-
import GKFetcher as GKFetcher
import GKReview
from GKPreprocessor import *
from GKVisualizer import *
from GKFilterer import *
from GKClassifier import *
from GKCLIParser import *
from GKReview import *
from GKFeatureSelector import *
import GKSentiment as GKSentiment


def main():
    # TODO: Make this MAIN great again
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

    if args.command == 'analyse':
        if "words" in args.analyse_commands:
            bag_of_words, classes, vocab = pre_processor.construct_bag_of_words(reviews, "rating")
            mask_array, scores = feat_selector.perform_feature_selection(bag_of_words, classes, nb_words=args.nb_words)
            print("Most representative words for GK ", filterer.reviewers_filtering)
            mask = None
            top_words = vocab[mask_array]

            if args.mask_url is not None:
                mask = GKFetcher.image_url_fetcher(args.mask_url)
            elif args.mask_path is not None:
                mask = GKFetcher.image_fetcher(args.mask_path)

            visualizer.word_cloud_background = args.word_cloud_bg
            visualizer.word_cloud_color_scheme = args.word_cloud_color_scheme
            visualizer.word_cloud(zip(top_words, scores), mask=mask)

        if "review" in args.analyse_commands:
            # TODO ditch this mess - don't forget the parse argument mess too !!!
            # Insert a new group with the review to predict
            review = GKReview(reviewer='Unknown')
            to_predict = [review]
            review_path = args.review_path
            content = ""
            with open(review_path, 'r') as review_file:
                content = review_file.read()
            to_predict[0].content = content
            reviews.append(to_predict) # inject the fake new group
            bag_of_words, classes, vocab = pre_processor.construct_bag_of_words(reviews, "reviewer")
            # Create hash of class label as it's not working with string
            processed_classes = [hash(label) for label in classes]
            # toDO the review to predict SHOULD NOT be in the feature selection process !!!!
            mask_array, scores = feat_selector.perform_feature_selection(bag_of_words, processed_classes, nb_words=args.nb_words)
            # Keep best ranked features
            processed_bag_of_words = bag_of_words[:, mask_array]
            # Predict the newly added feature
            result = GKClassifier.predict_reviewer(features=processed_bag_of_words, classes=processed_classes)
            prediction = []
            # Search for the true label
            for idx, label in enumerate(processed_classes):
                if label == result:
                    prediction = classes[idx]
            print("You are like ", prediction)

    if args.command == 'visualize':
        pre_processor.metric = args.metric

        # Visualize all methods
        for method in args.visualize_command:
            if visualizer.group_by == 'nothing':
                getattr(visualizer, "plot_" + method)(reviews)
            else:
                data, anno_labels = getattr(pre_processor,
                                            "grouped_" + method)(reviews, labels)
                title = visualizer.get_named_title(method + " " + args.metric + " given by GK reviewers",
                                                   filterer.reviewers_filtering)
                title = visualizer.get_dated_title(title, reviews)
                title = visualizer.get_rating_filtered_title(title)
                ylabel = method + " " + args.metric
                visualizer.group_plot(data=data,
                                      labels=anno_labels,
                                      ylabel=ylabel,
                                      title=title)


if __name__ == "__main__":
    main()
