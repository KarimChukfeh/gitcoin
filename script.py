import random
import pygithub3
import git
from git import Repo
import os
import re
import threading
import mysql.connector
import time



db_config = {
    'user' : 'bd40b5504b9f3e',
    'password' : '0e48730d',
    'database' : 'heroku_c5834a6e30a6592',
    'host' : 'us-cdbr-iron-east-05.cleardb.net',
    'port' : '3306'
}


def get_verified_nodes():
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    query = "SELECT * FROM information_schema.tables WHERE TABLE_TYPE = 'BASE TABLE'"
    cursor.execute(query, (db_config['database']))
    result = cursor.fetchall()
    out = []
    for table in result:
        out.append(table[2])
    return out

VERIFIED_NODES = get_verified_nodes()

def get_local_git_user():
    if not os.path.isdir('.git'):
        bare_repo = Repo.init('start',bare=True)
    repo = Repo('start')
    conf_reader = repo.config_reader()
    return conf_reader.get_value('user', 'name')

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
    print "enter your username"
    username = raw_input()
    print "enter your password"
    password = raw_input()
    auth = dict(login=username, password=password)
    if not os.path.isdir("start/Node"):
        os.makedirs("start/Node")
        username = get_local_git_user()
        gh = pygithub3.Github(**auth)
        repo_name = 'gitcoin'
        gh.repos.create(dict(name=repo_name, description='desc'))
        #repos = gh.create_repo(repo_name)
        random_node = random.choice(VERIFIED_NODES)
        cloneUrl='https://github.com/'+ random_node +'/gitcoin.git'
        localRepopath = 'start/Node/'
        repo = Repo.clone_from(cloneUrl, localRepopath)
        another_url = 'https://github.com/'+username+'/gitcoin.git'
        remote = repo.create_remote(repo_name, url=another_url)
        remote.push()
        create_new_node_table(username)
    return True

def transaction_verification():
    resp = null
    while(resp == null):
        resp = get_new_transaction_query()
    if(verify_sender(resp[1],resp[3]) and verify_receiver(resp[2])):
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()
        query = "UPDATE "+ get_local_git_user() +"status = confirmed WHERE transaction_id = "+resp[0]
        cursor.execute(query, (db_config['database']))
        db_connection.close()
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
    if(not(verif_commit_clone(repo,repo_clone))):
        return False
    if(not(verify_amount(amount,repo_clone))):
        return False
    return True

def verify_amount(amount,repo):
    commits = list(repo.iter_commits())
    commits = [commit for commit in commits if user_name in commit.message]
    if len(commits) > 0:
        #Make sure all transactions involving current user add up
        #and there are enough funds for the transaction to be made
        sum = 0
        transactions = []
        for commit in commits:
            if commit.message != '':
                arr = commit.message.split('-')
                if user_name in arr[0]:
                    sum -= int(arr[2])
                    transactions.append(commit)
                elif user_name in arr[1]:
                    sum += int(arr[2])
    if(amount>sum):
        return False
    return True

def verify_receiver(reciever):
    repo_clone =  clone_repo(reciever,"receiver_verif")
    repo = Repo()
    if(not(verif_commit_clone(repo,repo_clone))):
        return False
    return True

def verif_commit_clone(repo,repo_clone):
    commits_repo = list(repo.iter_commits('master'))
    print(len(commits_repo))
    commits_cloned_repo = list(repo_clone.iter_commits('master'))
    print(len(commits_cloned_repo))
    for commit in range(len(commits_repo, -1)):
        for commit_compare in range(len(commits_cloned_repo, -1)):
            if(not(commits_repo[commit].hexsha  == commits_cloned_repo[commit_compare].hexsha)):
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


def create_new_node_table(username):
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    tableName = username.encode('utf8', 'replace')
    query = "CREATE TABLE " + username + " (`transaction_id` VARCHAR(100) NOT NULL, `sender` VARCHAR(100) NULL, `reciever` VARCHAR(100) NULL, `amount` INT(100) NULL, `status` VARCHAR(45) NULL DEFAULT 'broadcasted', PRIMARY KEY (`transaction_id`));"
    cursor.execute(query, (tableName))
    db_connection.close()
    return True

def node_broadcast():
    repo = Repo()
    user_name = get_local_git_user()
    commits = list(repo.iter_commits())

    commits = [commit for commit in commits if user_name in commit.message]

    if len(commits) > 0:
        #Make sure all transactions involving current user add up
        #and there are enough funds for the transaction to be made
        sum = 0
        transactions = []
        for commit in commits:
            if commit.message != '':
                arr = commit.message.split('-')
                if user_name in arr[0]:
                    sum -= int(arr[2])
                    transactions.append(commit)
                elif user_name in arr[1]:
                    sum += int(arr[2])

        if sum < 0:
            print "Not Enough Funds for Transaction"
        else:
            for transaction in transactions:
                f = open('log', 'a+')
                #checks if the commit has already been broadcast
                if ('BROADCASTING: ' + transaction.hexsha) not in f.read():
                    db_connection = mysql.connector.connect(**db_config)
                    cursor = db_connection.cursor()
                    tableName = username.encode('utf8', 'replace')
                    f.write('BROADCASTING: ' + transaction.hexsha + '\n')
                    split_transaction = transaction.message.split('-')
                    broadcast_targets = []
                    #broadcast to all nodes
                    for node in VERIFIED_NODES:
                        if node != split_transaction[0] or node != split_transaction[1]:
                            target_nodes.push(node)
                            query = 'INSERT INTO ' + node + ' (transaction_id, sender, reciever, amount) VALUES (`{0}`, `{1}`, `{2}`, `{4}`)'.format(transaction.hexsha, split-commit[0], split-commit[1], split_transaction[2])
                            cursor.execute(query, (tableName))
                    #wait for all nodes to confirm broadcast
                    confirmed_by_all = False
                    while len(broadcast_targets) > 0:
                        for target in broadcast_targets:
                            query = 'SELECT status FROM ' + target + 'WHERE transaction_id = ' + transaction.hexsha
                            cursor.execute(query, (tableName))
                            result = cursor.fetchall()
                            for status in result:
                                if status != 'broadcasted':
                                    del broadcast_target[target]
                        time.sleep(30)
                    cursor.close()
                    db_connection.close()
                    f.close()


threads = []
if __name__ == '__main__':
    print "hi"
    create_new_node_table(get_local_git_user())
    t1 = threading.Thread(target = node_broadcast())
    t2 = threading.Thread(target = transaction_verification())
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()
