
from github import Github, RateLimitExceededException, GithubException
from collections import defaultdict
import sqlite3
from datetime import datetime
import time
import requests
import logging
from contextlib import closing


class popular_gits():
    """Popular Gits - you know who you are.
    
    Objects of this class encapsulate a Github repo and its "stargazers": 
    those Github users who have "starred" the repo indicating their positive interest in it:
    those repos are popular.

    The theory is that the *other* repos these people have starred are likely to be of
    interest to the other starrers of the repo.  The *most* starred should be of most interest.

    This code creates a database table
    || Org || Repo || Count ||
    so that repo http://github.com/{Org}/{Repo} will have {Count} starrers of the original repo.
    """

    page_size = 30

    def __init__(self, db_name, github_key, repo_org, repo_name):
        """Set up a repo to find its popular gits
        
        db_name: the name of the SQLite database that will be created (or accessed)
        github_key: the Github Access Token that will be used to run the Github API functions
        repo_org: the 'repo_org' part of https://github.com/{repo_org}/{repo_name}
        repo_name: the 'repo_name' part
        """
        self.db_name = db_name
        self.repo_org = repo_org
        self.repo_name = repo_name
        g = Github(github_key)
        self.repo = g.get_repo(self.repo_id)

        self.gits = defaultdict(int)
        self.con = sqlite3.connect(f'{self.db_name}.db')
        self.__setup_db()
    
    def __setup_db(self):
        with closing(self.con.cursor()) as cur:
            cur.execute('create table if not exists users (login text PRIMARY KEY, date text)')
            cur.execute('create table if not exists gits (org text UNIQUE, repo text UNIQUE, count int)')
            self.con.commit()
            logging.info(f"Database {self.db_name} with tables 'users' and 'gits' exists")

    def reset(self):
        """Remove all the data in the database and set it up again"""
        with closing(self.con.cursor()) as cur:
            cur.execute("drop table users")
            cur.execute("drop table gits")
            self.con.commit()
        self.__setup_db()
        logging.info(f"Recreated database {self.db_name}")

    @property
    def repo_id(self):
        return f"{self.repo_org}/{self.repo_name}"

    def get_gits(self):
        """Extract the existing set of starry gits from the database into a dictionary"""
        cur = self.con.cursor()
        with closing(self.con.cursor()) as cur:
            cur.execute("select * from gits")
            while f := cur.fetchmany():
                for o, rp, c in f:
                    self.gits[(o,rp)]=c

    def populate_user_gits(self, u):
        """Given a user, find all their starry gits and put them in the database
           
           It will only commit if there's no failure
        """
        new_gits = defaultdict(int)
        starred = u.get_starred()
        # Exclude those who star more than 1000 repos - this couldn't be done thoughtfully
        if starred.totalCount > 1000:
            page_count = 0
            logging.info(f"Excluded user {u.login} because they starred {starred.totalCount} repos")
        else:
            page_count = starred.totalCount
        for spage in (starred.get_page(i) for i in range(0, page_count//popular_gits.page_size+1)):
            for s in spage:
                o, rp = s.full_name.split('/')
                self.gits[(o,rp)]+=1
                new_gits[(o,rp)] = self.gits[(o,rp)]
        with closing(self.con.cursor()) as cur:
            cur.execute("insert into users values(?, ?)", (u.login, datetime.today().strftime('%Y-%m-%d')))
            for (o, rp), c in new_gits.items():
                cur.execute("replace into gits (org, repo, count) values(?, ?, ?)", (o, rp, c))
            self.con.commit()

    def accumulate_gits(self):
        """For all the repo's stargazers, if their repos haven't already been accumulated, do it now"""
        self.get_gits()
        with closing(self.con.cursor()) as cur:
            paged = self.repo.get_stargazers()
            pages = (paged.get_page(i) for i in range(0, paged.totalCount//popular_gits.page_size+1))
            for page in pages:
                for u in page:
                    cur.execute("select * from users where login=:login", {"login": u.login})
                    if not cur.fetchone(): # No such user yet
                        self.populate_user_gits(u)

    def run(self):
        """Tolerate the various "normal exceptions" """
        while(True):  # After each exception have another go until finished or interrupt
            try:
                self.accumulate_gits()
                return
            except KeyboardInterrupt:
                logging.info("Interrupted - pausing")
                break
            except requests.exceptions.ReadTimeout as rto:
                logging.warning(f"Timeout {rto=}, {type(rto)=}.  Sleeping for 1 minute")
                time.sleep(60)
            except RateLimitExceededException as ree:
                rate_limit = int(ree.headers['x-ratelimit-limit'])
                reset_seconds = int(ree.headers['x-ratelimit-reset']) - int(time.time())
                logging.warning(f"Rate Limit {rate_limit} breeched.  Resetting in {reset_seconds + 5} seconds")
                time.sleep(reset_seconds + 5)
            except GithubException as ge:
                logging.warning(f"Github exception {ge=}, {type(ge)=}.  Sleeping for 1 minute")
                time.sleep(60)
            except BaseException as err:
                logging.error(f"Error {err=}, {type(err)=}.  Exiting")
                break