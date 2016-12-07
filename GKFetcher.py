from bs4 import BeautifulSoup
import urllib2
import urllib
from GKReview import *
import pickle
import os.path
import re
import sys
from PIL import Image
import numpy as np
from os import path

db_file = "gk-list.db"
db_file2 = "gk-full.db"


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def fetch_parse_test_content(url):
    """
    Spaghetti code retrieving content from a single test
    :param url:
    :return: the test content (string)
    """
    content = ""
    try:
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find("div", {"id": "articleId"}).getText()
        # conclusion = soup.find("div", {"id": "story-conclusion"}).getText()
        # summary = soup.find("div", {"class": "summary"}).getText() # Pro and Cons
    except AttributeError, urllib2.HTTPError:
        print("An error happened, review (content) skipped.")
        pass
    return content.encode('utf-8')


def fetch_parse_page(url):
    """
    Spaghetti code retrieving a list of reviews
    :param url:
    :return: list of reviews
    """
    gk_reviews = []
    nb_try = 0
    while(nb_try < 3):
        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            for article in soup.find_all('article'):
                try:
                    review_content = article.findAll("div", {"class": "review-content"})
                    rating = article.findAll("div", {"class": "rating"})[0].getText()
                    if len(review_content) > 0 and represents_int(rating):
                        review_soup = review_content[0]
                        info_div = review_soup.findAll("p", {"class": "title"})[0]
                        review_link = "http://www.gamekult.com" + info_div.findAll("a")[0].get('href')
                        title = info_div.getText()

                        # Shitty regex hackline
                        raw_reviewer = review_soup.findAll("p", {"class": "byline"})[0].getText()
                        raw_reviewer = raw_reviewer.split("Par ")[1].split(", le")
                        reviewer = raw_reviewer[0]
                        match = re.search(r'(\d+/\d+/\d+)', raw_reviewer[1])
                        date = match.group(1)

                        review = GKReview(title=title, reviewer=reviewer, review_link=review_link,
                                          rating=rating,
                                          date=date)
                        gk_reviews.append(review)
                except:
                    print("Failed to parse test from list")
                    print(article.prettify())
                    print "Unexpected error:", sys.exc_info()[0]
                    pass
            nb_try = 3
        except urllib2.HTTPError:
            print("Entire page skipped due to server error")
            if nb_try < 3:
                print("Retrying...")

    return gk_reviews


def fetch_parse_nth_first_page(nb_page, force_download, cache):
    """
    Spaghetti code retrieving a list of reviews for the n-th last page of tests
    :param nb_page: number of page to process
    :param force_download:
    :param cache: true if cache allowed
    :return: list of reviews
    """
    reviews = []
    # Fetch test listing if needed
    if not os.path.isfile(db_file) or force_download:
        page = 1
        condition = True
        while condition:
            url = "http://www.gamekult.com/jeux/test-jeux-video.html?p=%d" % page
            fetched = fetch_parse_page(url)
            reviews = reviews + fetched
            print("Processed page %s" % page)
            page += 1
            condition = len(fetched) > 0 and page <= nb_page
        if cache:
            with open(db_file, 'wb') as output:
                pickle.dump(reviews, output, protocol=pickle.HIGHEST_PROTOCOL)
    elif os.path.isfile(db_file):
        with open(db_file, 'r') as data_in:
            reviews = pickle.load(data_in)

    return reviews


def image_url_fetcher(url):
    response = urllib.urlopen(url)
    content = response.read()
    outf = open("tmp-mask", 'wb')
    outf.write(content)
    outf.close()
    d = path.dirname(__file__)
    return image_fetcher(path.join(d, "tmp-mask"))


def image_fetcher(filepath):
    return np.array(Image.open(filepath))


def fetch_parse_full_tests(force_download, cache, nb_page):
    """
    Fetch & Parse both lists and content
    :param force_download:
    :param cache: true if cache allowed
    :param nb_page:
    :return: list of reviews
    """
    reviews = []
    # Fetch tests content if needed
    if not os.path.isfile(db_file2) or force_download:
        print("Fetching data..")
        reviews = fetch_parse_nth_first_page(nb_page, force_download=force_download, cache=cache)
        for index, review in enumerate(reviews):
            review.content = fetch_parse_test_content(review.link)
            print("%d/%d" % (index + 1, len(reviews)))
        if cache:
            with open(db_file2, 'wb') as output:
                pickle.dump(reviews, output, protocol=pickle.HIGHEST_PROTOCOL)
    elif os.path.isfile(db_file2):
        print("Nothing to fetch, data loaded from disk.")
        with open(db_file2, 'r') as data_in:
            reviews = pickle.load(data_in)
    return reviews

'''
def fetch_translation(reviews):

    for review in reviews:
        try:
            params = {"lang": "fr-en", "text": review.content,
                      "key": "my_key",
                      'format': "plain"}
            url = "https://translate.yandex.net/api/v1.5/tr.json/translate?%s" % (urllib.urlencode(params))
            data = urllib2.urlopen(url).read()
            review.translation = data
        except:
            print("A translation error happened.")
            pass
    return reviews
'''


# For manual testing purpose
def main():
    reviews = fetch_parse_nth_first_page(10)
    for review in reviews:
        print review.link
        review.content = fetch_parse_test_content(review.link)
        print(review.content)
        break

if __name__ == "__main__":
    main()
