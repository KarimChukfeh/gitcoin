import random
import pygithub3
import git
from git import Repo
import os
import re


VERIFIED_NODES = ['https://github.com/karimchukfeh', 'https://github.com/youssefe', 'https://github.com/osfalos', 'https://github.com/sanaknaki']

def clone_repo_from_random_node():
    random_node = random.choice(VERIFIED_NODES)
    if not os.path.isdir("Node"):
        os.makedirs("Node")
        git.Git("Node").clone('https://github.com/karimchukfeh/gitcoin')


def remote_node_exists(organization, no_forks=True):
    gh = None
    gh = pygithub3.Github(token='3ec8183955c53ad0acfbf3fdccbe874e561b4acd')
    all_repos = gh.repos.list(user=organization).all()
    for repo in all_repos:
        # Don't print the urls for repos that are forks.
        if no_forks and repo.fork:
            continue
        if re.split('/', repo.clone_url)[-1] == "gitcoin.git":
            return True
    return False



if __name__ == '__main__':
    # clone_repo_from_random_node()
