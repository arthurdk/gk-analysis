import plotly
from plotly.graph_objs import Scatter, Layout, Bar, Figure
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objs as go

'''
class VisualizationStrategy:
    def __init__(self):
        pass
    # Homemade enumeration
    Plot, CSV, ASCII = range(3)

'''
import random


class GKVisualizer:
    def __init__(self, reviewers_filtering, group_by_option='nothing',
                 rating_filters=[],
                 word_cloud_background="white",
                 color_scheme=None):
        self.reviewers_filtering = reviewers_filtering
        self.group_by = group_by_option
        self.rating_filters = rating_filters
        self.word_cloud_background = word_cloud_background
        self.word_cloud_color_scheme = color_scheme

    @staticmethod
    def _grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        """
        Credit to word_cloud project on github
        :param word:
        :param font_size:
        :param position:
        :param orientation:
        :param random_state:
        :param kwargs:
        :return:
        """
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

    def word_cloud(self, frequencies, mask=None):

        if mask is not None:
            word_cloud = WordCloud(background_color=self.word_cloud_background,
                                   width=1200,
                                   height=1000,
                                   mask=mask
                                   ).generate_from_frequencies(frequencies)
        else:
            word_cloud = WordCloud(background_color=self.word_cloud_background,
                                   width=1200,
                                   height=1000
                                   ).generate_from_frequencies(frequencies)

        if self.word_cloud_color_scheme is not None:
            plt.imshow(word_cloud.recolor(color_func=GKVisualizer._grey_color_func, random_state=3))
        else:
            plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()

    @staticmethod
    def display_gauge(labels, target, title):

        value = 100.0 / len(labels)
        values = [value] * len(labels)

        base_chart = {
            "values": values,
            "domain": {"x": [0, .48]},
            "marker": {
                "line": {
                    "width": 1
                }
            },
            "name": "Gauge",
            "hole": .4,
            "type": "pie",
            "direction": "clockwise",
            "showlegend": False,
            "hoverinfo": "none",
            "textinfo": "none",
            "textposition": "outside"
        }

        meter_chart = {
            "values": values,
            "labels": labels,
            'textfont': {
                "size": 22,
                "color": "white"

            },
            "domain": {"x": [0, 0.48]},
            "name": "Gauge",
            "hole": .3,
            "type": "pie",
            "direction": "clockwise",
            "showlegend": False,
            "textinfo": "label",
            "textposition": "inside",
            "hoverinfo": "none"
        }

        layout = {
            'title': title,
            'xaxis': {
                'showticklabels': False,
                'autotick': False,
                'showgrid': False,
                'zeroline': False,
            },
            'yaxis': {
                'showticklabels': False,
                'autotick': False,
                'showgrid': False,
                'zeroline': False,
            },
            'annotations': [
                {
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0.23,
                    'y': 0.5,
                    'text': target,
                    'font': {
                        "size": 22,
                        "color": "black"
                    },
                    'showarrow': False
                }
            ]
        }

        # apparently we don't want the boundary now
        base_chart['marker']['line']['width'] = 0

        fig = {"data": [base_chart, meter_chart],
               "layout": layout}
        plotly.offline.plot(fig)

    @staticmethod
    def _determine_min_max(reviews, min_date, max_date):
        for review in reviews:
            if min_date > review.date:
                min_date = review.date
            if max_date < review.date:
                max_date = review.date
        return min_date, max_date

    def determine_date(self, reviews):
        if self.group_by != 'nothing':
            max_date = reviews[0][0].date
            min_date = reviews[0][0].date

            for group in reviews:
                min_date, max_date = self._determine_min_max(reviews=group, min_date=min_date, max_date=max_date)
        else:
            max_date = reviews[0].date
            min_date = reviews[0].date
            min_date, max_date = self._determine_min_max(reviews=reviews, min_date=min_date, max_date=max_date)

        return min_date, max_date

    # TODO optimized to not call this one everytime
    def get_dated_title(self, title, grouped_reviews):
        """
        Return the title with a proper date
        :param title:
        :param grouped_reviews:
        :return:
        """
        min_date, max_date = self.determine_date(grouped_reviews)
        if min_date.year == max_date.year:
            title += " (%d)" % max_date.year
        else:
            title += " (%d to %d)" % (min_date.year, max_date.year)
        return title

    @staticmethod
    def get_named_title(title, reviewers):
        if len(reviewers) > 0:
            title += " (" + ", ".join(reviewers) + ") "
        return title

    def get_rating_filtered_title(self, title):
        for opt, rating in self.rating_filters:
            title += " (" + opt + " " + str(rating) + ")"
        return title

    def group_plot(self, data, labels, title, ylabel):

        figure = {
            "data": [
                Bar(x=labels, y=data)
            ],
            "layout": Layout(
                title=title,
                xaxis=dict(
                    title=self.group_by
                ),
                yaxis=dict(
                    title=ylabel
                ),
            )
        }

        plotly.offline.plot(figure)

    @staticmethod
    def scatter(x, y, title):

        layout = dict(title=title,
                      yaxis=dict(
                          title="Rating")
                      ,
                      xaxis=dict(
                          title="Date")
                      )

        # Create a trace
        trace = go.Scatter(
            x=x,
            y=y,
            mode='markers'
        )

        data = [trace]
        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig)
