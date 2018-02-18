import random
import pygithub3
import git
from git import Repo
import os
import re
import mysql.connector


db_config = {
    'user' : 'bd40b5504b9f3e',
    'password' : '0e48730d',
    'database' : 'heroku_c5834a6e30a6592',
    'host' : 'us-cdbr-iron-east-05.cleardb.net',
    'port' : '3306'
}

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
    gh = pygithub3.Github(token='3ec8183955c53ad0acfbf3fdccbe874e561b4acd')
    all_repos = gh.repos.list(user=organization).all()
    for repo in all_repos:
        # Don't print the urls for repos that are forks.
        if no_forks and repo.fork:
            continue
        if re.split('/', repo.clone_url)[-1] == "gitcoin.git":
            return True
    return False

def listen_for_new_node():
    numberOfNodes = len(VERIFIED_NODES)

    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    query = "SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s;"

    cursor.execute(query, (db_config['database']))
    result = cursor.fetch()
    print result
    db_connection.close()



if __name__ == '__main__':
    print "hi"
    # clone_repo_from_random_node()
    # remote_node_exists("karimchukfeh")
    listen_for_new_node()
