
# gk-analysis

Simple python 2 tool designed to analyse game reviews produced by the French website [Gamekult](http://www.gamekult.com/).

[![N|Solid](https://www.python.org/static/img/python-logo.png)](https://nodesource.com/products/nsolid)

gk-analysis is able to fetch data from the Gamekult website and then process everything to make interesting graphs.

# Table of content
* [gk-analysis](#gk-analysis)
     * [Output examples](#output-examples) <- probably what you are looking for
     * [Online Demo](#online-demo) (not yet available)
     * [Installation](#installation)
     * [Dependencies](#dependencies)
     * [Usage](#usage)
        * [General usage](#general-usage)
        * [Fetch data](#fetch-data)
        * [Visualize data](#visualize-data)
        * [Analyse data](#analyse-data)
     * [Development](#development)
     * [Todos](#todos)
     * [License](#license)


### Output examples

Note: most of the graph are interactive so you will not experience the true power of this program by having a look at pictures...

Thanks to machine learning, you can display the most meaningful words for a list of reviewers given that the rating is less or equals to 3.
```sh
$ python  GKAnalysis.py  analyse  words  --rating-le 3 -R "Stoon"
```

[![N|Solid](http://reho.st/medium/self/a2717ca486d8f6fb9a85221770278131edebd2d2.png)](http://reho.st/view/self/a2717ca486d8f6fb9a85221770278131edebd2d2.png)


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

The tool also support mask system for the word cloud, a customizable background and color set

```sh
$ python GKAnalysis.py analyse words --mask-url \
 https://pre00.deviantart.net/4ae0/th/pre/f/2015/208/e/4/batman_logo_simple_by_animedark2-d933xx7.jpg \
 --nb_words 200 --word-cloud-bg black \
 --word-cloud-color-scheme whatever --rating-le 3

```

[![N|Solid](http://reho.st/medium/self/f6b6db5184452c40d46281fe53256c6e7c8ec29f.png)](http://reho.st/view/self/f6b6db5184452c40d46281fe53256c6e7c8ec29f.png)


Previous word cloud, all GK reviews were included (at least the 20 last page of tests), on the next one only Stoon's for comparison.

```sh
$ python GKAnalysis.py analyse words --mask-url \
 https://pre00.deviantart.net/4ae0/th/pre/f/2015/208/e/4/batman_logo_simple_by_animedark2-d933xx7.jpg \
 --nb_words 200 --word-cloud-bg black --word-cloud-color-scheme whatever \
 --rating-le 3 -R "Stoon"

```

[![N|Solid](http://reho.st/medium/self/3eb89e267e6299cea2e6c413b6bc98e17803608d.png)](http://reho.st/view/self/3eb89e267e6299cea2e6c413b6bc98e17803608d.png)


You can also write a review (or just some text) and it will tell you the most probable GK reviewer that could have written this review

```sh
$ python GKAnalysis.py analyse prediction reviewer ./path-to-file -N 1000
```

In this example the file contained a review from Gameblog, sorry Gautoz :/

[![N|Solid](http://reho.st/medium/self/78c18f7dbe7bb51d3883cdaeb83cbddc6a0d48ba.png)](http://reho.st/view/self/78c18f7dbe7bb51d3883cdaeb83cbddc6a0d48ba.png)


Let's see how this review would have been rated on Gamekult.

```sh
$ python GKAnalysis.py analyse prediction rating ./path-to-file -N 1000
```


[![N|Solid](http://reho.st/medium/self/463ef20dff80b968229d1f7b7d14f48f328ec9e5.png)](http://reho.st/view/self/463ef20dff80b968229d1f7b7d14f48f328ec9e5.png)

7 wow. But rest assured it's probably because it's an extract of a Deus Ex MD review which was well rated on GK.

----

It's also possible to display a scatter plot of reviews


```sh
$ python GKAnalysis.py analyse visualize scatter
```


[![N|Solid](http://reho.st/medium/self/bf74b50e74493ed2dfa3d68527dd86e6f62b66ac.png)](http://reho.st/view/self/bf74b50e74493ed2dfa3d68527dd86e6f62b66ac.png)

Interactive version: [https://cdn.rawgit.com/arthurdk/gk-analysis/master/examples/scatter_rating_date.html](https://cdn.rawgit.com/arthurdk/gk-analysis/master/examples/scatter_rating_date.html)


And it is still possible to use filter !


```sh
$ python GKAnalysis.py analyse visualize scatter -R "Stoon"
```


[![N|Solid](http://reho.st/medium/self/36a95b10ec73481a7ae61f982fb867296c13ea40.png)](http://reho.st/view/self/36a95b10ec73481a7ae61f982fb867296c13ea40.png)


Double group by features.


```sh
$ python GKAnalysis.py visualize variance -G "reviewer_year" --metric rating
```


[![N|Solid](http://reho.st/medium/self/51f2e4ab13a5c8e3b68c4885026d98c0b1607de5.png)](http://reho.st/view/self/51f2e4ab13a5c8e3b68c4885026d98c0b1607de5.png)

Interactive version: [https://cdn.rawgit.com/arthurdk/gk-analysis/master/examples/double_group_by.html](https://cdn.rawgit.com/arthurdk/gk-analysis/master/examples/double_group_by.html)

### Online Demo

Soon !

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
 - nltk (not for now)
 - pandas
 - sklearn

Quick install commands for Ubuntu based system:
```sh
$ pip install beautifulsoup4 plotly numpy pandas nltk stop_words wordcloud image sklearn matplotlib
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

usage: GKAnalysis.py visualize [-h] [-R [reviewers]] [--year-le year]
                               [--year-ge year] [--year-eq year]
                               [--rating-le rating] [--rating-ge rating]
                               [--rating-eq rating] [-G [by]] [-M metric]
                               command [command ...]

positional arguments:
  command               List of available visualization commands:
                        - variance
                        - mean
                        - scatter

optional arguments:
  -h, --help            show this help message and exit
  -R [reviewers], --reviewers [reviewers]
                        List of reviewers to visualize
                        Example: "Stoon,Gautoz"
  --year-le year        Filter review being less recent or of the given year
  --year-ge year        Filter review being more recent or of the given year
  --year-eq year        Filter review being the given year
  --rating-le rating    Filter review having ratings less or equals than the given one
  --rating-ge rating    Filter review having ratings greater or equals than the given one
  --rating-eq rating    Filter review having a rating equals to the given one
  -G [by], --group-by [by]
                        Determine how to group by data (Default: data grouped by reviewer)
                        List of options:
                        - reviewer
                        - year
                        - reviewer_year
                        - year_reviewer
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

usage: GKAnalysis.py analyse [-h] [-R [reviewers]] [--year-le year]
                             [--year-ge year] [--year-eq year]
                             [--rating-le rating] [--rating-ge rating]
                             [--rating-eq rating] [-G [by]]
                             {words,prediction} ...

positional arguments:
  {words,prediction}    Available analyse commands
    words               See words help for more information
    prediction          See prediction help for more information

optional arguments:
  -h, --help            show this help message and exit
  -R [reviewers], --reviewers [reviewers]
                        List of reviewers to visualize
                        Example: "Stoon,Gautoz"
  --year-le year        Filter review being less recent or of the given year
  --year-ge year        Filter review being more recent or of the given year
  --year-eq year        Filter review being the given year
  --rating-le rating    Filter review having ratings less or equals than the given one
  --rating-ge rating    Filter review having ratings greater or equals than the given one
  --rating-eq rating    Filter review having a rating equals to the given one
  -G [by], --group-by [by]
                        Determine how to group by data (Default: data grouped by reviewer)
                        List of options:
                        - reviewer
                        - year
                        - reviewer_year
                        - year_reviewer



```

##### Words

This command allows to produce a word cloud of the most important words in selected reviews.

```sh
$ python GKAnalysis.py analyse  words --help
```


```
usage: GKAnalysis.py analyse words [-h] [-R [reviewers]] [--year-le year]
                                   [--year-ge year] [--year-eq year]
                                   [--rating-le rating] [--rating-ge rating]
                                   [--rating-eq rating] [-G [by]]
                                   [-N [nb_words]] [--word-cloud-bg color]
                                   [--word-cloud-color-scheme color_scheme]
                                   [--mask-url url | --mask-path path-to-file]

optional arguments:
  -h, --help            show this help message and exit
  -R [reviewers], --reviewers [reviewers]
                        List of reviewers to visualize
                        Example: "Stoon,Gautoz"
  --year-le year        Filter review being less recent or of the given year
  --year-ge year        Filter review being more recent or of the given year
  --year-eq year        Filter review being the given year
  --rating-le rating    Filter review having ratings less or equals than the given one
  --rating-ge rating    Filter review having ratings greater or equals than the given one
  --rating-eq rating    Filter review having a rating equals to the given one
  -G [by], --group-by [by]
                        Determine how to group by data (Default: data grouped by reviewer)
                        List of options:
                        - reviewer
                        - year
                        - reviewer_year
                        - year_reviewer
  -N [nb_words], --nb_words [nb_words]
                        Number of best ranked words to select (Default: 100)
  --word-cloud-bg color
                        Background color for the word cloud Example: black
  --word-cloud-color-scheme color_scheme
                        Color scheme for the word cloud (anything only grey is supported for now)
  --mask-url url        URL of a mask for the wordcloud
  --mask-path path-to-file
                        Path to a mask for the wordcloud



```


##### Prediction of your text

This command allows to predict the rating, of the GK reviewer of a text (input)

```

usage: GKAnalysis.py analyse predict [-h] [-R [reviewers]] [--year-le year]
                                        [--year-ge year] [--year-eq year]
                                        [--rating-le rating]
                                        [--rating-ge rating]
                                        [--rating-eq rating] [-G [by]]
                                        [-N [nb_words]]
                                        prediction filepath

positional arguments:
  predict               Choose which element do you want to make prediction on
                        List of options:
                        - reviewer
                        - rating
  filepath              Path to the review to analyse

optional arguments:
  -h, --help            show this help message and exit
  -R [reviewers], --reviewers [reviewers]
                        List of reviewers to visualize
                        Example: "Stoon,Gautoz"
  --year-le year        Filter review being less recent or of the given year
  --year-ge year        Filter review being more recent or of the given year
  --year-eq year        Filter review being the given year
  --rating-le rating    Filter review having ratings less or equals than the given one
  --rating-ge rating    Filter review having ratings greater or equals than the given one
  --rating-eq rating    Filter review having a rating equals to the given one
  -G [by], --group-by [by]
                        Determine how to group by data (Default: data grouped by reviewer)
                        List of options:
                        - reviewer
                        - year
                        - reviewer_year
                        - year_reviewer
  -N [nb_words], --nb_words [nb_words]
                        Number of best ranked words to select (Default: 100)


```

### Development
Want to contribute or fork? That's great, go ahead but be remember this is some nice Spaghetti coding ;) ! (i.e Quick & Dirty)

### Todos
 - Write Tests (someday hopefully?)
 - Always more way to visualize data
 - Bag of word analysis (finish the implementation)
 - Deep learning analysis
 - Multiple outputs (ASCII table, CSV support)
 - Group by ratings and display who given the most of each one (or at least display the propotion)
 - Sentiment analysis by reviewer (need translation for optimality :/)
 - Make the code more generic (as of now it more a script than a program)
 - Use data structure instead of list of list for clarity...

This project could also support other websites but that's not really what I am personally interested in (I will still welcome PR though).

### License
----

MIT
