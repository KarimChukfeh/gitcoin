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

VERIFIED_NODES = ['karimchukfeh', 'youssefe', 'osfalos', 'sanaknaki']

def getLocalGitUser():
    return "karimchukfeh"

def clone_repo_from_random_node():
    random_node = random.choice(VERIFIED_NODES)
    if not os.path.isdir("Node"):
        os.makedirs("Node")
        git.Git("Node").clone('https://github.com/'+ random_node + '/gitcoin.git')


def remote_node_exists(organization, no_forks=True):
    gh = None
    gh = pygithub3.Github(token='3ec8183955c53ad0acfbf3fdccbe874e561b4acd')
    all_repos = gh.repos.list(user=organization).all()
    for repo in all_repos:
        if no_forks and repo.fork:
            continue
        if re.split('/', repo.clone_url)[-1] == "gitcoin.git":
            return True
    return False

def new_node_table_exists():
    numberOfNodes = len(VERIFIED_NODES)
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    query = "SELECT * FROM information_schema.tables WHERE TABLE_TYPE = 'BASE TABLE'"
    cursor.execute(query, (db_config['database']))
    result = cursor.fetchall()
    for table in result:
        if table[2] not in VERIFIED_NODES:
            VERIFIED_NODES.append(table[2])


def create_git_repo_init():
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
    create_new_node_table(username)
    return True

def create_new_node_table(username):
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    tableName = username.encode('utf8', 'replace')
    query = "CREATE TABLE " + username + " (`transaction_id` VARCHAR(100) NOT NULL, `sender` VARCHAR(100) NULL, `reciever` VARCHAR(100) NULL, `amount` INT(100) NULL, `status` VARCHAR(45) NULL DEFAULT 'broadcasted', PRIMARY KEY (`transaction_id`));"
    cursor.execute(query, (tableName))
    db_connection.close()
    return True


if __name__ == '__main__':
    print "hi"
    # clone_repo_from_random_node()
    # remote_node_exists("karimchukfeh")
    new_node_table_exists()
    # create_new_node_table("sanaknaki")
