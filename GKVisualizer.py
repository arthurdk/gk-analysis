import plotly
from plotly.graph_objs import Scatter, Layout, Bar, Figure


'''
class VisualizationStrategy:
    def __init__(self):
        pass
    # Homemade enumeration
    Plot, CSV, ASCII = range(3)

'''


class GKVisualizer:

    def __init__(self, reviewers_filtering, group_by_option='nothing'):
        self.reviewers_filtering = reviewers_filtering
        self.group_by = group_by_option

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
        trace = Bar(x=[1, 2, 3], y=[4, 5, 6])
        data = [trace]
        layout = Layout(title='My Plot')
        fig = Figure(data=data, layout=layout)
        plotly.offline.plot(figure)
        # Save the figure as a png image:
        # plotly.plotly.image.save_as(fig, 'my_plot.png')
