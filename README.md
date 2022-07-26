# Popular Gits

You know who you are.

Those popular people in high-school who most students tended to have mixed relationships with.  
As irritating as it was, you had to keep on their good sides and keep up with what they were doing.

Looking back, well, they weren't so bad.  Good on 'em really!  I would've if I could've.

This repo is is dedicated to the popular gits.

## How it works

In [Github](https://github.com) when you open a repo (like [popular-gits](https://github.com/profitviews/popular-gits)) 
in the top-right of your screen you will see a star glyph and the word "Star":

![Star example](/assets/images/github_top_right.png)

Click it - you've now "starred" the repo.  It's now be in _your_ list of stars.

These lists are accessible via the [Github API](https://docs.github.com/en/rest) and there is a [Python interface](https://github.com/PyGithub/PyGithub).

The idea of Popular Gits is that if a group of people like a particular repo, they probably have similar interests.
What if you listed _all_ the repos they like and worked out which are _most_ liked?
That's what we've done by looking at all the starred repos of everyone who starred that _particular_ repo.
We give the examples of [QuantLib](/Quantlib.md) and [ccxt](/ccxt.md).

**Note**: IT'S SLOW!  Due to the limitations on HTTP REST interfaces and understandable throttling by Github, 
a significant source repo of hundreds or thousands of stars will take a long time to run - 
typically many hours or a few days.

## Implementation

We use:
* the [Github API](https://docs.github.com/en/rest) and [PyGithub](https://github.com/PyGithub/PyGithub)
* [Sqlite](https://www.sqlite.org/index.html) with the [sqlite3](https://docs.python.org/3/library/sqlite3.html) Python package

## Installation

This is tested with Ubuntu Linux 22.04.  It should work with little effort on other Linuxen, MacOS and Windows.

1. Install [sqlite3](https://www.sqlite.org/download.html)
1. Install [Python](https://www.python.org/)
1. `pip install PyGithub`
1. Get a [Github account](https://github.com).  This is free and very easy.
   Once done, get a [Personal Access Token](https://github.com/settings/tokens).
1. To experiment with Popular Gits, install [Jupyter Lab](https://jupyter.org/install) and then use [our notebook](/popular_gits.ipynb) to start.
1. To use this notebook as-is, put your Personal Access Token in environment variable `GITHUB_KEY` via

   ```shell
   export GITHUB_KEY="<your Personal Access Token>"
   ```

   you might put this in your `~/.bashrc` or similar.


It will also be useful to install [SQLite Database Browser](https://sqlitebrowser.org/) so 
that you can easily create `.csv` files.

## Command Line

Use `pg.py` to run Poplular Gits on the command line (set it executable first):

```shell
chmod +x pg.py
./pg.py --github_key=<your key> pvcppdb profitviews cpp_crypto_algos
```

Other options are available.  Run `./pg.py --help`:

```
usage: pg.py [-h] [--reset]
             [--log {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
             [--github_key GITHUB_KEY] [--csv CSV_FILE]
             db_name org repo

positional arguments:
  db_name               Root name of SQLite database to be created or used
  org                   Github organization name
  repo                  Github repo name, i.e. github.com/org/repo

options:
  -h, --help            show this help message and exit
  --reset, -r           Erase the database on start if it exists
  --log {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, -l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Specify the log level. Default is WARNING
  --github_key GITHUB_KEY, -k GITHUB_KEY
                        Specify your GitHub key. Otherwise it will look at
                        $GITHUB_KEY
  --csv CSV_FILE, -c CSV_FILE
                        Output data as CSV file
```

## Examples

We at [ProfitView](https://profitview.net) have run this code on a couple or repos, and here's some truncated results:
* [QuantLib](/Quantlib.md)
* [ccxt](/ccxt.md)

We also have [a blog](https://profitview.net/blog/open-source-trading-projects) on this process.

## Categorised Lists

While there may be some algorithmic ways to associate the repos, there's some value in checking their READMEs
and assigning a category.  We have done this for the [top 150 of the QuantLib set](/QuantlibStarredGithubs_Top150.csv) producing [QuantlibPopularLists.csv](/QuantlibPopularLists.csv).  This is useful for extracting "Top 10" lists and similar


