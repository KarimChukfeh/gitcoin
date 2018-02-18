import random
import pygithub3
import git
from git import Repo
import os
import re
from pygithub3 import Github
#from github3 import GitHub

VERIFIED_NODES = ['https://github.com/karimchukfeh', 'https://github.com/youssefe', 'https://github.com/osfalos', 'https://github.com/sanaknaki']

def getLocalGitUser():
    return "karimchukfeh"

def clone_repo_from_random_node():
    random_node = random.choice(VERIFIED_NODES)
    if not os.path.isdir("Node"):
        os.makedirs("Node")
        git.Git("Node").clone('https://github.com/karimchukfeh/gitcoin')
        broadcast_to_random_nodes('NewNodeNotification', )


def remote_node_exists(organization, no_forks=True):
    gh = None
    username = raw_input()
    password = raw_input()
    auth = dict(login=username, password=password)
    gh = Github(**auth)
    repo_name = 'gitcoin'
    octocat = gh.users.get()
    print octocat
    get_user = gh.users.get()
    gh.repos.create(dict(name='gitcoin', description='desc'))
    #repos = gh.create_repo(repo_name)
    cloneUrl='https://github.com/karimchukfeh/gitcoin.git'
    localRepopath = 'clonetest/'
    repo = Repo.clone_from(cloneUrl, localRepopath)
    another_url = 'https://github.com/osfalos/gitcoin.git'
    remote = repo.create_remote('gitcoin', url=another_url)
    remote.push()


#if __name__ == '__main__':
    #print "hi"
    # clone_repo_from_random_node()


remote_node_exists("karimchukfeh")
