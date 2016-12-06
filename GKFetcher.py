from bs4 import BeautifulSoup
import urllib2
from GKReview import *
import pickle
import os.path
import re
db_file = "gk-list.db"
db_file2 = "gk-full.db"


# Spaghetti code retrieving content from a single test
def fetch_parse_test(url):
    content = ""
    try:
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find("div", {"id": "articleId"}).getText()
        # conclusion = soup.find("div", {"id": "story-conclusion"}).getText()
        # summary = soup.find("div", {"class": "summary"}).getText() # Pro and Cons
    except AttributeError:
        print("An error happened, review (content) skipped.")
        pass
    return content


# Spaghetti code retrieving a list of reviews
def fetch_parse_page(url):
    gk_reviews = []
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    for article in soup.find_all('article'):
        try:
            review_content = article.findAll("div", {"class": "review-content"})
            rating = article.findAll("div", {"class": "rating"})[0].getText()
            if len(review_content) > 0:
                review_soup = review_content[0]
                info_div = review_soup.findAll("p", {"class": "title"})[0]
                review_link = "http://www.gamekult.com" + info_div.findAll("a")[0].get('href')
                title = info_div.getText()

                # Shitty regex hack
                raw_reviewer = review_soup.findAll("p", {"class": "byline"})[0].getText()
                raw_reviewer = raw_reviewer.split("Par ")[1].split(", le")
                reviewer = raw_reviewer[0]
                match = re.search(r'(\d+/\d+/\d+)', raw_reviewer[1])
                date = match.group(1)

                review = GKReview(title=title, reviewer=reviewer, review_link=review_link, rating=rating, date=date)
                gk_reviews.append(review)
        except:
            print("An error happened :(.")
            pass
    return gk_reviews


# Spaghetti code retrieving a list of reviews for the n-th last page of tests
def fetch_parse_nth_first_page(nth, force_download, cache):
    # Fetch test listing if needed
    if not os.path.isfile(db_file) or force_download:
        reviews = []
        page = 1
        condition = True
        while condition:
            url = "http://www.gamekult.com/jeux/test-jeux-video.html?p=%d" % page
            fetched = fetch_parse_page(url)
            reviews = reviews + fetched
            print("Processed page %s" % page)
            page += 1
            condition = len(fetched) > 0 and page <= nth
        if cache:
            with open(db_file, 'wb') as output:
                pickle.dump(reviews, output, protocol=pickle.HIGHEST_PROTOCOL)
    elif os.path.isfile(db_file):
        with open(db_file, 'r') as data_in:
            reviews = pickle.load(data_in)

    return reviews


# Fetch & Parse both lists and content
def fetch_parse_full_tests(force_download, cache, nb_page):
    reviews = []
    # Fetch tests content if needed
    if not os.path.isfile(db_file2) or force_download:
        print("Fetching data..")
        reviews = fetch_parse_nth_first_page(nb_page, force_download=force_download, cache=cache)
        for index, review in enumerate(reviews):
            review.content = fetch_parse_test(review.link)
            print("%d/%d" % (index + 1, len(reviews)))
        if cache:
            with open(db_file2, 'wb') as output:
                pickle.dump(reviews, output, protocol=pickle.HIGHEST_PROTOCOL)
    elif os.path.isfile(db_file2):
        print("Nothing to fetch, data loaded from disk.")
        with open(db_file2, 'r') as data_in:
            reviews = pickle.load(data_in)
    return reviews


# For manual testing purpose
def main():
    reviews = fetch_parse_nth_first_page(10)
    for review in reviews:
        # review.print_review()
        print review.link
        review.content = fetch_parse_test(review.link)
        print(review.content)
        break

if __name__ == "__main__":
    main()
