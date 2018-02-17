import mysql.connector
from git import Repo

db_config = {
    'user' : 'bd40b5504b9f3e',
    'password' : '0e48730d',
    'database' : 'heroku_c5834a6e30a6592',
    'host' : 'us-cdbr-iron-east-05.cleardb.net',
    'port' : '3306'
}

def get_git_config_name():
    repo = Repo()
    conf_reader = repo.config_reader()
    return conf_reader.get_value('user', 'name')

def get_git_config_email():
    repo = Repo()
    conf_reader = repo.config_reader()
    return conf_reader.get_value('user','email')

db_connection = mysql.connector.connect(**db_config)

print get_git_config_name()
print get_git_config_email()

db_connection.close()