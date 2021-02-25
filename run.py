
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
from docopt import docopt
from github import Github
from dotenv import load_dotenv
import datetime as dt
import logging
from helpers import setup_logging
import csv
from repo_info import RepoInfo
from configuration import config


load_dotenv()


def write_file(filename, data_list):
    with open(filename, "w", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(["Repository", "Language", "Created", "Last modified", "Private", "Stars", "Team", "Potential archive"])
        for d in data_list:
            csv_writer.writerow([d.url, d.language, d.created, d.last_modified, d.is_private(), d.stars, d.team, d.potential_archive])


def get_repos(gh, org):
    rep = []
    all_orgs = gh.get_user().get_orgs()
    for o in all_orgs:
        if o.login == org:
            repos = o.get_repos()
            print(f'number of repos {repos.totalCount}')
            for r in repos:
                rep.append(RepoInfo(r, config))
    return rep


if __name__=='__main__':
    arguments = docopt(__doc__, version=__version__)
    token = arguments['-t'] or os.environ['GITHUB_TOKEN'] # OAuth token from GitHub
    org = arguments['-o'].strip()
    setup_logging( f"{org}_metrics.log")
    # print(f"token {token}, organization {org}")

    gh = Github(token)
    logging.info(f'Reading {org} repositories metadata (lazy load)...')
    start_time = dt.datetime.now() 
    repos = get_repos(gh, org)
    file_name = f"{org}_repos.csv"
    logging.info(f'Writing data to {file_name}...')
    write_file(file_name, repos)
    end_time = dt.datetime.now() 
    duration = end_time - start_time
    logging.info(f'Done in {duration.total_seconds()}sec')



