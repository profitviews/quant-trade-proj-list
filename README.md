# Popular Gits

We all know them - those dudes at high-school who were popular.  As irritating as it was, 
you had to keep on their good sides and keep up with what they were doing.
Looking back, well, they weren't so bad.  Good on em really!  I would've if I could've.

This repo is is dedicated to the popular gits.

## How it works

In [Github](https://github.com) when you open a repo (like [popular-gits](https://github.com/profitviews/popular-gits)) 
in the top-right of your screen you will see a star glyph and the word "Star":

![Star example](/assets/images/github_top_right.png)

Click it - you've now "starred" the repo.  It now be in your list of starred repos.

This list is accessible via the [Github API](https://docs.github.com/en/rest) and there is a [Python interface](https://github.com/PyGithub/PyGithub).

The idea of Popular Gits is that if a group of people like a particular repo, 
there's a good chance that others in that other repos they like will be liked by others in that group.

So we get that larger list and rank it by how frequently they are starred.

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
1. Put your Personal Access Token in environment variable `GITHUB_KEY` via

   ```shell
   export GITHUB_KEY="<your Personal Access Token>"
   ```

   you might put this in your `~/.bashrc` or similar.

1. To experiment with Popular Gits, install [Jupyter Lab](https://jupyter.org/install) and then use [our notebook](/popular_gits.ipynb) to start.

It will also be useful to install [SQLite Database Browser](https://sqlitebrowser.org/) so 
that you can easily create `.csv` files and similar.

## Examples

We at [ProfitView](https://profitview.net) have run this code on a couple or repos, and here's some truncated results:
* [QuantLib](/QuantLib.md)
* [ccxt](/ccxt.md)

We also have [a blog](https://profitview.net/blog/open-source-trading-projects) on this process.
