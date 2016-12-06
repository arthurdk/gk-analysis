# gk-analysis

Simple python 2 tool designed to analyse game reviews produced by the French website [Gamekult](http://www.gamekult.com/).

[![N|Solid](https://www.python.org/static/img/python-logo.png)](https://nodesource.com/products/nsolid)

gk-analysis is able to fetch data from Gamekult website and then allows:

  - to perform Magic


### Installation

```sh
$ git clone <project url>
```

### Dependencies
List of dependencies:
 - python-tk
 - beautifulsoup4
 - matplotlib
 - numpy
 - pickle

Quick install commands for Ubuntu based system:
```sh
$ apt install python-tk
$ pip install beautifulsoup4 matplotlib numpy pickle
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
usage: GKAnalysis.py fetch [-h] [nb_page]

positional arguments:
  nb_page     Number of page containing reviews to fetch (Default: 10)

optional arguments:
  -h, --help  show this help message and exit

```

#### Visualize data

```sh
$ python GKAnalysis.py visualize --help
```

```
usage: GKAnalysis.py visualize [-h] command [command ...]

positional arguments:
  command     List of available visualization commands:
              - variance
              - mean

optional arguments:
  -h, --help  show this help message and exit
```
### Output examples

Section not finished yet.

### Development
Want to contribute or fork? That's great, go ahead :) !

### Todos
 - Write Tests (someday hopefully?)
 - More data visualization
 - Bag of word analysis
 - Deep learning analysis

This project could also support other websites but that's not really what I am personally interested in (I will still welcome PR though).

### License
----

MIT
