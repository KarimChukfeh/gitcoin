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

def get_local_git_user():
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

def listen_for_new_node():
    numberOfNodes = len(VERIFIED_NODES)

    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    query = "SELECT * FROM information_schema.tables WHERE TABLE_TYPE = 'BASE TABLE'"

    cursor.execute(query, (db_config['database']))
    result = cursor.fetchall()
    db_connection.close()
    print len(result)


def create_git_repo_init():
    gh = None
    #print "enter your username"
    #username = raw_input()
    #print "enter your password"
    #password = raw_input()
    #auth = dict(login=username, password=password)
    username = get_local_git_user()
    print(username)
    gh = pygithub3.Github(token="793a78550d17324ec385ec16d8b76ec6575b83c4")
    repo_name = 'gitcoin'
    gh.repos.create(dict(name=repo_name, description='desc'))
    #repos = gh.create_repo(repo_name)
    cloneUrl='https://github.com/karimchukfeh/gitcoin.git'
    localRepopath = 'clonetest/'
    repo = Repo.clone_from(cloneUrl, localRepopath)
    another_url = 'https://github.com/'+username+'/gitcoin.git'
    remote = repo.create_remote(repo_name, url=another_url)
    remote.push()
    return True

def transaction_verification():
    resp = null
    while(resp == null):
        resp = get_new_transaction_query()
    if(verify_sender(resp[0],resp[2]) and verify_receiver(resp[1])):
        #call broadcast
        return True
    else:
        return False

def clone_repo(clone_username,type):
    dir_name = "clone_"+type+"_"+clone_username
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    cloneUrl="https://github.com/"+str(clone_username)+"/gitcoin.git"
    localRepopath = dir_name+"/"
    repo = Repo.clone_from(cloneUrl, localRepopath)
    return repo

def verify_sender(sender, amount):
    repo_clone = clone_repo(sender,"sender_verif")
    repo = Repo()
    if((verif_commit_clone(repo,repo_clone))):
        return False
    return True

def verify_receiver(reciever):
    repo_clone =  clone_repo(reciever,"receiver_verif")
    repo = Repo()
    if((verif_commit_clone(repo,repo_clone))):
        return False
    return True

def verif_commit_clone(repo,repo_clone):
    commits_repo = list(repo.iter_commits('master'))
    print(len(commits_repo))
    commits_cloned_repo = list(repo_clone.iter_commits('master'))
    print(len(commits_cloned_repo))
    for commit in commits_repo:
        for commit_compare in commits_cloned_repo:
            if(not(commit.hexsha  == commit_compare.hexsha)):
                return False
    return True

def get_new_transaction_query():
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    query = "SELECT * FROM "+ db_config['database'] + "." + get_local_git_user()
    cursor.execute(query, (db_config['database']))
    result = cursor.fetchall()
    db_connection.close()
    # TODO exec query get result
    last = result[-1]
    if last[-1] == 'broadcasted':
        db_connection.close()
        return last
    else:
        db_connection.close()
        return null


    # clone_repo_from_random_node()
    # remote_node_exists("karimchukfeh")
#listen_for_new_node()
#create_git_repo_init()
print(verify_sender("osfalos","25"))
print(verify_receiver("osfalos"))
