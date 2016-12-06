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

Quick install commands for Ubuntu based system:
```sh
$ pip install beautifulsoup4 plotly numpy pickle
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
usage: GKAnalysis.py visualize [-h] [-R [reviewers]] [-G by] [-M metric]
                               [-Y year]
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
  -Y year, --filter-by-year year
                        Visualize data for a particular year
```
### Output examples

Section not finished yet.

### Development
Want to contribute or fork? That's great, go ahead but be remember this is some nice Spaghetti coding ;) ! (i.e Quick & Dirty)

### Todos
 - Write Tests (someday hopefully?)
 - More data visualization
 - Bag of word analysis
 - Deep learning analysis
 - Multiple outputs (ASCII table, CSV support)
 - Group by reviewer AND year at the same time

This project could also support other websites but that's not really what I am personally interested in (I will still welcome PR though).

### License
----

MIT
