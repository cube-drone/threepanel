from __future__ import print_function
import os
import sys

from invoke import run as silently_run
from invoke import task
from colorama import init as colorama_init
from colorama import Fore, Back, Style


colorama_init()
print(Fore.RED, file=sys.stderr)


REQUIRED_ENVIRONMENT_VARIABLES = ['DIGITALOCEAN_API_TOKEN',
                                  'DJANGO_PROJECT_SLUG',
                                  'DJANGO_DOMAIN',
                                  'DJANGO_ADMIN_NAME',
                                  'DJANGO_ADMIN_EMAIL',
                                  'POSTGRES_DB_PASSWORD',
                                  'MANDRILL_KEY',
                                  'DJANGO_SECRET_KEY',
                                  'PAPERTRAIL_SERVER']


def run(cmd, *args, **kwargs):
    """
    We're overwriting invoke's "run" to always
    print out the command it's running before it runs.
    It also does color things.
    """
    print(Fore.RED, file=sys.stderr)
    if not cmd:
        return
    print(Fore.GREEN + cmd)
    print(Style.RESET_ALL)
    print(Style.DIM)
    silently_run(cmd, *args, **kwargs)
    print(Style.RESET_ALL)


def environment_subset(keys):
    """
    Prepare a subset of the environment containing only the keys that
    are useful to deploy.
    """
    env = {}
    for key in keys:
        if key not in os.environ:
            print("Warning: {} not defined.".format(key), file=sys.stderr)
        else:
            env[key] = os.environ[key]
    return env


def environment_dict_to_string(env_dict):
    """
    Convert the environment dict into a string that can be passed as an
    argument to a shell command:
    ENV_VAR1="hello" ENV_VAR2="world"
    """
    env_list = ["{}=\"{}\"".format(key, env_dict[key]) for key in env_dict]
    return " ".join(env_list)


@task
def vagrant(command):
    return run("vagrant ssh -c '{}'".format(command))


@task
def vagrant_invoke(command):
    return run(vagrant("source django_environment/bin/activate && cd vagrant_django/threepanel && invoke {}".format(command)))


@task
def get_media():
    run("scp -r vagrant@threepanel.com:/home/vagrant/vagrant_django/media .")


@task
def get_current_db():
    db_password = os.environ['POSTGRES_DB_PASSWORD']
    run("ssh vagrant@threepanel.com \"sudo -u postgres pg_dump threepanel > /tmp/last.db_backup\"")
    run("scp vagrant@threepanel.com:/tmp/last.db_backup /tmp/last.db_backup")
    run("vagrant scp /tmp/last.db_backup /tmp/last.db_backup")
    vagrant("sudo -u postgres psql -d threepanel -f /tmp/last.db_backup".format(db_password))


@task
def run_python_install_script(production=False):
    install_path = "/home/vagrant/vagrant_django/configuration/install.py"
    environment_dict = environment_subset(REQUIRED_ENVIRONMENT_VARIABLES)
    environment_dict['DJANGO_DEBUG'] = str(not production)
    environment_string = environment_dict_to_string(environment_dict)
    cmd = "sudo {} python3 {}".format(environment_string, install_path)
    vagrant(cmd)


@task
def install(production=False):
    if not production:
        run("vagrant up --provider virtualbox")
        run_python_install_script(production=False)
    else:
        get_media()
        run("vagrant up --provider digital_ocean")
        run_python_install_script(production=True)
        vagrant_invoke("auth_keys")

    get_current_db()
    vagrant_invoke("makemigrations")
    vagrant_invoke("migrate")

    if production:
        vagrant_invoke("prod_restart")


@task
def clean():
    run("vagrant destroy -f")
    run("rm -rf vars.ini")
    run("rm -rf scripts")
    run("rm -rf __pycache__")
