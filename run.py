
'''
Usage:
    run -o <organisation> [-t <github_token>]

Options:
    -t <github_token>       OAuth token from GitHub
    -o <organisation>       company organization name
    --version               Short version
'''

__version__ = "0.1.1"

import os
from typing import NamedTuple, no_type_check_decorator
from docopt import docopt
from github import Github
from dotenv import load_dotenv
import datetime as dt
import logging
from helpers import setup_logging
import csv

load_dotenv()

def write_file(filename, data_list):
    with open(filename, "w", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(["Repository", "Language", "Created", "Last modified", "Private", "Stars"])
        for d in data_list:
            csv_writer.writerow([d.url, d.language, d.created, d.last_modified, 'True' if d.is_private() else 'False', d.stars])

class RepoInfo:
    def __init__(self, r):
        self.gh_r = r

    def get_name(self):
        return self.gh_r.name

    def get_html_url(self):
        return self.gh_r.html_url

    def get_lang(self):
        return self.gh_r.language
    
    def is_private(self):
        return self.gh_r.private

    def get_pushed_date(self):
        return self.gh_r.pushed_at

    def get_created_at(self):
        return self.gh_r.owner.created_at

    def get_created_at_str(self):
        return self.get_created_at().strftime("%m/%d/%Y")

    def get_last_modified_str(self):
        # return self.gh_r.owner.last_modified
        return self.get_pushed_date().strftime("%m/%d/%Y")

    def get_watchers_count(self):
        return self.gh_r.watchers_count

    def get_stars(self):
        return self.gh_r.stargazers_count

    def get_stats(self):
        statistics = [] 
        stats = self.gh_r.get_stats_contributors()
        for stat in stats:
            author = str(stat.author)
            author = (author.replace('NamedUser(login="', "")).replace('")', "")
            for week in stat.weeks:
                
                if week.c != 0:
                    date = str(week.w)
                    date = date[:10]
                    statistics.append({
                        "author": author,
                        "date": date,
                        "added": week.a,
                        "deleted": week.d,
                        "changed": week.c
                    })
        return statistics


    name = property(get_name)
    url = property(get_html_url)
    language = property(get_lang)
    last_modified = property(get_last_modified_str)
    created = property(get_created_at_str)
    stars = property(get_stars)
    stats = property(get_stats)

def get_repos(gh, org):
    rep = []
    all_orgs = gh.get_user().get_orgs()
    for o in all_orgs:
        if o.login == org:
            repos = o.get_repos()
            print(f'number of report {repos.totalCount}')
            for r in repos:
                rep.append(RepoInfo(r))
    return rep

if __name__=='__main__':
    arguments = docopt(__doc__, version=__version__)
    token = arguments['-t'] or os.environ['GITHUB_TOKEN'] # OAuth token from GitHub
    org = arguments['-o'].strip()
    setup_logging( f"{org}_metrics.log")
    print(f"token {token}, organization {org}")

    gh = Github(token)
    repos = get_repos(gh, org)
    write_file(f"{org}_repos.csv", repos)




