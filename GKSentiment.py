from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()


def perform_analysis(reviews, attribute):
    for review in reviews:
        review.sentiment_analysis = sid.polarity_scores(text=review.attribute)
    return reviews
