import GKFetcher as GKFetcher
from GKReview import *
from GKClassifier import *


class GKDispatcher:
    def __init__(self, pre_processor, filterer, feat_selector, visualizer, args):
        self.pre_processor = pre_processor
        self.filterer = filterer
        self.feat_selector = feat_selector
        self.args = args
        self.visualizer = visualizer
        self.classifier = GKClassifier()

    def dispatch(self, reviews):
        getattr(self, "dispatch_" + self.args.command)(reviews)

    def dispatch_analyse(self, reviews):
        # TODO MAKE THIS CLASS GREAT AGAIN !
        if "words" in self.args.analyse_commands:
            bag_of_words, classes, vocab = self.pre_processor.construct_bag_of_words(reviews, "rating")
            mask_array, scores = self.feat_selector.perform_feature_selection(bag_of_words, classes,
                                                                              nb_words=self.args.nb_words)
            print("Most representative words for GK ", self.filterer.reviewers_filtering)
            mask = None
            top_words = vocab[mask_array]

            if self.args.mask_url is not None:
                mask = GKFetcher.image_url_fetcher(self.args.mask_url)
            elif self.args.mask_path is not None:
                mask = GKFetcher.image_fetcher(self.args.mask_path)

            self.visualizer.word_cloud_background = self.args.word_cloud_bg
            self.visualizer.word_cloud_color_scheme = self.args.word_cloud_color_scheme
            self.visualizer.word_cloud(zip(top_words, scores), mask=mask)

        if "prediction" in self.args.analyse_commands:
            # Perform Group By
            reviews, labels = self.pre_processor.perform_group_by(reviews)
            # TODO ditch this mess
            # Insert a new group with the review to predict
            review = GKReview(reviewer='Unknown')
            to_predict = [review]
            review_path = self.args.review_path
            content = ""
            with open(review_path, 'r') as review_file:
                content = review_file.read()
            to_predict[0].content = content
            reviews.append(to_predict)  # inject the fake new group
            bag_of_words, classes, vocab = self.pre_processor.construct_bag_of_words(reviews, self.args.predict_target)
            # Create hash of class label as it's not working with string
            processed_classes = [hash(label) for label in classes]
            # TODO the review to predict SHOULD NOT be in the feature selection process !!!!
            mask_array, scores = self.feat_selector.perform_feature_selection(bag_of_words, processed_classes,
                                                                              nb_words=self.args.nb_words)
            # Keep best ranked features
            processed_bag_of_words = bag_of_words[:, mask_array]
            # Predict the newly added feature
            result = self.classifier.predict_reviewer(features=processed_bag_of_words, classes=processed_classes)
            prediction = []
            # Search for the true label
            for idx, label in enumerate(processed_classes):
                if label == result:
                    prediction = classes[idx]
            print("Prediction ", prediction)

            classes.remove(getattr(review, self.args.predict_target))
            classes = list(set(classes))
            title = self.visualizer.get_named_title(
                "Prediction of %s on given review" % self.args.predict_target,
                self.filterer.reviewers_filtering)
            title = self.visualizer.get_rating_filtered_title(title)
            self.visualizer.display_gauge(classes, prediction, title)

    def dispatch_visualize(self, reviews):
        self.pre_processor.metric = self.args.metric
        # Visualize all methods
        for method in self.args.visualize_command:
            if self.visualizer.group_by == 'nothing':
                getattr(self.visualizer, "plot_" + method)(reviews)
            else:
                if "scatter" in self.args.visualize_command:
                    print("Group by ignored for now ")  # TODO fix this non generic code :(

                    dates = [review.date for review in reviews]
                    labels = [review.rating for review in reviews]
                    title = self.visualizer.get_named_title("Scatter plot of review according to rating "
                                                            "and date given by GK reviewers",
                                                            self.filterer.reviewers_filtering)
                    title = self.visualizer.get_rating_filtered_title(title)
                    self.visualizer.scatter(x=dates, y=labels, title=title)

                else:
                    # Perform Group By
                    reviews, labels = self.pre_processor.perform_group_by(reviews)
                    data, anno_labels = getattr(self.pre_processor,
                                                "grouped_" + method)(reviews, labels)
                    title = self.visualizer.get_named_title(method + " " + self.args.metric + " given by GK reviewers",
                                                            self.filterer.reviewers_filtering)
                    title = self.visualizer.get_dated_title(title, reviews)
                    title = self.visualizer.get_rating_filtered_title(title)
                    ylabel = method + " " + self.args.metric
                    self.visualizer.group_plot(data=data,
                                               labels=anno_labels,
                                               ylabel=ylabel,
                                               title=title)
