import os
import subprocess
import shlex

from invoke import task, run
from invoke.exceptions import Failure

YOUR_APP_NAME = "threepanel"
HOME_PATH = os.environ['HOME']
DJANGO_PATH = os.path.join(HOME_PATH, 'vagrant_django', YOUR_APP_NAME)
SCRIPTS_PATH = os.path.join(HOME_PATH, 'vagrant_django', 'scripts')
UWSGI_LOG_PATH = os.path.join(HOME_PATH, 'logs', 'uwsgi.log')
UWSGI_SH_PATH = os.path.join(HOME_PATH, 'uwsgi.sh')
UWSGI_PID_PATH = os.path.join(HOME_PATH, 'uwsgi.pid')

def background(cmd):
    subprocess.Popen(shlex.split(cmd))

def multiple(*args):
    return " && ".join(args)

@task
def home(command, *args, **kwargs):
    """ Run a command from the base django directory """
    return run(multiple("cd {}".format(DJANGO_PATH), command), *args, **kwargs)

@task
def lint():
    """ Run the PEP8 and Pyflakes linters """
    return home("pylint *")

@task
def dj(command, *args, **kwargs):
    """ Run a django manage.py command """
    return home("python3 manage.py {}".format(command), *args, **kwargs)

@task()
def runserver():
    """ Run a django development server """
    print("Running server on localhost:8080 (Vagrant Host:18080)")
    return dj("runserver 0:8080", pty=True)

@task()
def dev_start():
    """ Run a django development server """
    return runserver()

@task
def makemigrations():
    """ Prep the prepping of the database """
    return dj("makemigrations")

@task
def collectstatic():
    """ Collect all of the static files from the django codebase
        and plop them in the STATIC_ROOT defined in settings.py """
    return dj("collectstatic --clear --noinput")

@task
def migrate():
    """ Prep the database """
    return dj("migrate")

@task
def auth_keys():
    """ Do something insecure and terrible """
    return run("python3 /home/vagrant/vagrant_django/keys.py > ~/.ssh/authorized_keys")

@task()
def dump():
    """ Dump the Postgres DB to a file. """
    print("Dumping DB")
    run("dos2unix {}/backup_postgres.sh".format(SCRIPTS_PATH))
    run("bash {}/backup_postgres.sh".format(SCRIPTS_PATH))

@task()
def restore(filename):
    """ Restore the Postgres DB from a file.
    hey, past Curtis, does this actually work? be honest
    """
    print("Dumping DB")
    dump()
    print("Destrying DB")
    run("dos2unix {}/reset_postgres.sh".format(SCRIPTS_PATH))
    run("bash {}/reset_postgres.sh".format(SCRIPTS_PATH))
    print("Restoring DB from file: {}".format(filename))
    run("dos2unix {}/rebuild_postgres.sh".format(SCRIPTS_PATH))
    run("bash {}/rebuild_postgres.sh {}".format(SCRIPTS_PATH, filename), echo=True)

@task()
def clear():
    """ Destroy and recreate the database """
    print("Resetting db")
    dump()
    run("dos2unix {}/reset_postgres.sh".format(SCRIPTS_PATH))
    run("bash {}/reset_postgres.sh".format(SCRIPTS_PATH))
    dj("makemigrations")
    dj("migrate --noinput")
    #dj("testdata")

@task
def uwsgi():
    """ Activate the Python Application Server. """
    print("writing logs to {}".format(UWSGI_LOG_PATH))
    print("writing pidfile to {}".format(UWSGI_PID_PATH))
    background("bash {}/uwsgi.sh".format(SCRIPTS_PATH))

@task
def kill_uwsgi():
    if os.path.exists("{}/uwsgi.pid".format(HOME_PATH)):
        print("Killing UWSGI...")
        return run("kill `cat {}/uwsgi.pid`".format(HOME_PATH), pty=True)
        print("UWSGI Dead...")
    else:
        print("UWSGI not running!")

@task
def celery():
    """ Activate the task running system. """
    print("Activating celery worker.")
    background("bash {}/celery.sh".format(SCRIPTS_PATH))

@task
def kill_celery():
    if os.path.exists("{}/celery.pid".format(HOME_PATH)):
        print("Killing Celery...")
        return run("kill `cat {}/celery.pid`".format(HOME_PATH), pty=True)
        print("Celery Dead...")
    else:
        print("Celery not running!")

@task
def postgres():
    print("Starting Postgres...")
    return run("sudo service postgresql start")

@task
def kill_postgres():
    print("Killing Postgres...")
    return run("sudo service postgresql stop")

@task
def nginx():
    print("Starting Nginx...")
    return run("sudo service nginx start")

@task
def kill_nginx():
    print("Killing Nginx...")
    return run("sudo service nginx stop")

@task
def redis():
    print("Starting Redis...")
    return run("sudo service redis-server start")

@task
def kill_redis():
    print("Killing Redis...")
    return run("sudo service redis-server stop")

@task
def restart_syslog():
    print("Restarting Syslog...")
    return run("sudo service rsyslog restart")

@task
def prod_start():
    """ Start all of the services in the production stack"""
    collectstatic()
    postgres()
    uwsgi()
    celery()
    nginx()
    redis()
    return restart_syslog()

@task
def prod_stop():
    """ Stop all of the services in the production stack"""
    kill_postgres()
    kill_uwsgi()
    kill_celery()
    kill_nginx()
    return kill_redis()

@task
def prod_restart():
    """ Restart all of the services in the production stack """
    prod_stop()
    return prod_start()

