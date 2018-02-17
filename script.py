import random
import pygithub3
from git import repo

VERIFIED_NODES = ['karimchukfeh', 'youssefe', 'osfalos', 'sanaknaki']

def clone_repo_from_random_node():
    random_node = random.choice(VERIFIED_NODES)
    print random_node

clone_repo_from_random_node()

# gh = None
#
#
# def gather_clone_urls(organization, no_forks=True):
#     all_repos = gh.repos.list(user=organization).all()
#     for repo in all_repos:
#
#         # Don't print the urls for repos that are forks.
#         if no_forks and repo.fork:
#             continue
#
#         yield repo.clone_url
#
#
# if __name__ == '__main__':
#     gh = pygithub3.Github()
#
#     clone_urls = gather_clone_urls("karimchukfeh")
#     for url in clone_urls:
#         print url
