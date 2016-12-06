
# gk-analysis

Simple python 2 tool designed to analyse game reviews produced by the French website [Gamekult](http://www.gamekult.com/).

[![N|Solid](https://www.python.org/static/img/python-logo.png)](https://nodesource.com/products/nsolid)

gk-analysis is able to fetch data from the Gamekult website and then process everything to make interesting graphs.

# Table of content
* [gk-analysis](#gk-analysis)
     * [Installation](#installation)
     * [Dependencies](#dependencies)
     * [Usage](#usage)
        * [General usage](#general-usage)
        * [Fetch data](#fetch-data)
        * [Visualize data](#visualize-data)
        * [Analyse data](#analyse-data)
     * [Output examples](#output-examples) <- probably what you are looking for
     * [Online Demo](#online-demo) (not yet available)
     * [Development](#development)
     * [Todos](#todos)
     * [License](#license)


### Installation

```sh
$ git clone https://github.com/arthurdk/gk-analysis.git
```
or
```sh
$ wget https://github.com/arthurdk/gk-analysis/archive/master.zip
```

### Dependencies
List of dependencies: (there are way too much I know)
 - beautifulsoup4
 - plotly
 - numpy
 - pickle
 - matplotlib
 - image
 - wordcloud
 - stop_words
 - ntlk
 - pandas

Quick install commands for Ubuntu based system:
```sh
$ pip install beautifulsoup4 plotly numpy pandas nltk stop_words wordcloud image matplotlib
```
### Usage

#### General usage

```sh
$ python GKAnalysis.py --help
```

```
Usage: GKAnalysis.py [-h] [--force-dl] [--no-cache] {visualize,fetch} ...

Perform analysis on Gamekult reviews.

positional arguments:
  {visualize,fetch}  Available commands
    visualize        See visualiation help for more information
    fetch            Fetch data from Gamekult

optional arguments:
  -h, --help         show this help message and exit
  --force-dl         Force download even if there is cache (default: false)
  --no-cache         Disable data caching (default: false)
```
#### Fetch data

```sh
$ python GKAnalysis.py fetch --help
```

```
usage: GKAnalysis.py fetch [-h] [-N [nb_page]]

optional arguments:
  -h, --help            show this help message and exit
  -N [nb_page], --nb_page [nb_page]
                        Number of page containing reviews to fetch (Default: 10)

```

#### Visualize data

```sh
$ python GKAnalysis.py visualize --help
```

```
usage: GKAnalysis.py visualize [-h] [-R [reviewers]] [-Y year]
                               [--rating-le rating] [--rating-ge rating]
                               [--rating-eq rating] [-G by] [-M metric]
                               command [command ...]

positional arguments:
  command               List of available visualization commands:
                        - variance
                        - mean

optional arguments:
  -h, --help            show this help message and exit
  -R [reviewers], --reviewers [reviewers]
                        List of reviewers to visualize
                        Example: "Stoon,Gautoz"
  -Y year, --filter-by-year year
                        Visualize data for a particular year
  --rating-le rating    Filter review having ratings less or equals than the given one
  --rating-ge rating    Filter review having ratings greater or equals than the given one
  --rating-eq rating    Filter review having a rating equals to the given one
  -G by, --group-by by  Determine how to group by data (Default: data grouped by reviewer)
                        List of options:
                        - reviewer
                        - year
  -M metric, --metric metric
                        Determine which metric to analyze (Default: Rating)
                        List of options:
                        - rating
                        - length
                        - wordcount
```

#### Analyse data

```sh
$ python GKAnalysis.py analyse --help
```


```

usage: GKAnalysis.py analyse [-h] [-R [reviewers]] [-Y year]
                             [--rating-le rating] [--rating-ge rating]
                             [--rating-eq rating] [-G by] [-N [nb_words]]
                             command [command ...]

positional arguments:
  command               List of available analysing commands: - words -
                        sentiment

optional arguments:
  -h, --help            show this help message and exit
  -R [reviewers], --reviewers [reviewers]
                        List of reviewers to visualize Example: "Stoon,Gautoz"
  -Y year, --filter-by-year year
                        Visualize data for a particular year
  --rating-le rating    Filter review having ratings less or equals than the
                        given one
  --rating-ge rating    Filter review having ratings greater or equals than
                        the given one
  --rating-eq rating    Filter review having a rating equals to the given one
  -G by, --group-by by  Determine how to group by data (Default: data grouped
                        by reviewer) List of options: - reviewer - year
  -N [nb_words], --nb_words [nb_words]
                        Number of best ranked words to select (Default: 100)


```
### Output examples


You can display the most meaningful words for a list of reviewers given that the rating is less or equals to 5.
```sh
$ python  GKAnalysis.py  analyse --rating-le 5 words --reviewers "Stoon"
```
[![N|Solid](http://reho.st/preview/self/0daea958e847382e80ff4a7b469aac6f92072536.png)](http://reho.st/view/self/0daea958e847382e80ff4a7b469aac6f92072536.png)

You can also display the variance of ratings by reviewer
```sh
$ python  GKAnalysis.py  visualize  variance --group-by reviewer
```
[![N|Solid](http://reho.st/preview/self/0d454af889ec835fd79a4ec13ca2c2c92f913b4f.png)](http://reho.st/view/self/0d454af889ec835fd79a4ec13ca2c2c92f913b4f.png)

Let's zoom on one in particular

```sh
$ python  GKAnalysis.py  visualize  variance --group-by year -R "Stoon"
```
[![N|Solid](http://reho.st/preview/self/9c3a3e911f0c9edf1824adfe49334962cbb8290d.png)](http://reho.st/view/self/9c3a3e911f0c9edf1824adfe49334962cbb8290d.png)

Ever increasing variance interesting.

Other metrics are available, for example you can have a look at wordcount

```sh
$ python  GKAnalysis.py  visualize  mean --metric wordcount --group-by reviewer
```

[![N|Solid](http://reho.st/medium/self/c0b18bf8d857bb80cc57fcf389ec3e49bb01169c.png)](http://reho.st/view/self/c0b18bf8d857bb80cc57fcf389ec3e49bb01169c.png)


### Online Demo

Soon !

### Development
Want to contribute or fork? That's great, go ahead but be remember this is some nice Spaghetti coding ;) ! (i.e Quick & Dirty)

### Todos
 - Write Tests (someday hopefully?)
 - Always more way to visualize data
 - Bag of word analysis (finish the implementation)
 - Deep learning analysis
 - Multiple outputs (ASCII table, CSV support)
 - Group by reviewer AND year at the same time
 - Group by ratings and display who given the most of each one (or at least display the propotion)
 - Sentiment analysis by reviewer (need translation for optimality :/)

This project could also support other websites but that's not really what I am personally interested in (I will still welcome PR though).

### License
----

MIT
