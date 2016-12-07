import random
from sklearn.neural_network import MLPClassifier


class GKClassifier:
    def __init__(self):
        pass

    @staticmethod
    def predict_reviewer(features, classes):
        """
        Credit: https://www.dataquest.io/blog/natural-language-processing-with-python/
        :param features:
        :param review:
        :return:
        """
        # TODO Implement a proper prediction system... and Cross validation ....

        print("Performing prediction")
        # Run the regression and generate predictions for the test set.
        classifier = MLPClassifier()
        train_features = features[range(features.shape[0] - 1), :]
        train_classes = [classes[idx] for idx in range(len(classes) - 1)]
        classifier.fit(train_features, train_classes)
        return classifier.predict(features[features.shape[0] - 1, :])