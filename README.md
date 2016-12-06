# gk-analysis

Simple python 2 tool designed to analyse game reviews produced by the French website [Gamekult](http://www.gamekult.com/).

[![N|Solid](https://www.python.org/static/img/python-logo.png)](https://nodesource.com/products/nsolid)

gk-analysis is able to fetch data from Gamekult website and then allows:

  - to perform Magic


### Installation

```sh
$ git clone https://github.com/arthurdk/gk-analysis.git
```
or
```sh
$ wget https://github.com/arthurdk/gk-analysis/archive/master.zip
```

### Dependencies
List of dependencies:
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
$ pip install beautifulsoup4 plotly numpy pickle pandas ntlk stop_words wordcloud image matplotlib
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

Section not finished yet.

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
