import random
import pygithub3
import git
from git import Repo
import os
import re
import threading

VERIFIED_NODES = ['https://github.com/karimchukfeh', 'https://github.com/youssefe', 'https://github.com/osfalos', 'https://github.com/sanaknaki']

def get_git_user():
    repo = Repo()
    conf_reader = repo.config_reader()
    return conf_reader.get_value('user', 'name')

def clone_repo_from_random_node():
    random_node = random.choice(VERIFIED_NODES)
    if not os.path.isdir("Node"):
        os.makedirs("Node")
        git.Git("Node").clone('https://github.com/karimchukfeh/gitcoin')
        broadcast_to_random_nodes('NewNodeNotification', )


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

def creat_git_repo_init():
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
    return True

def node_broadcast_thread():
    #update commit history
    repo = Repo()
    user_name = get_git_user()
    commits = list(repo.iter_commits())

    commits = [commit for commit in commits if user_name in commit.meesage]

    if len(commits) > 0:
        #Make sure all transactions involving current user add up
        #and there are enough funds for the transaction to be made
        sum = 0
        for commit in commits:
            if commit.message != '':
                arr = commit.message.split('-')
                if user_name in arr[0]:
                    sum -= int(arr[2])
                elif user_name in arr[1]:
                    sum += int(arr[2])
        if sum < 0
            print "Not Enough Funds for Transaction"

        latest-commit = commits[-1]

        f = open('log', 'a+')

        #checks if the latest commit has already been broadcast
        if latest-commit.message not in f.read():
            f.write('BROADCASTING: ' + latest-commit.message + "\n")
            
            split-commit = latest-commit.split('-')
            for node in VERIFIED_NODES:
                if node != split-commit[0] or node != split-commit[1]:
                    #hash send receiver amount status
                    

        f.close()

def await_transaction_verification(commit_hash):


if __name__ == '__main__':
    print "hi"
    # clone_repo_from_random_node()
    # remote_node_exists("karimchukfeh")
