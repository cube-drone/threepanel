from __future__ import print_function
import os
import sys

from invoke import run as silently_run
from invoke import task


REQUIRED_ENVIRONMENT_VARIABLES = ['DIGITALOCEAN_API_TOKEN',
                                  'DJANGO_PROJECT_SLUG',
                                  'DJANGO_DOMAIN',
                                  'DJANGO_ADMIN_NAME',
                                  'DJANGO_ADMIN_EMAIL',
                                  'POSTGRES_DB_PASSWORD',
                                  'AWS_ACCESS_KEY_ID',
                                  'AWS_SECRET_ACCESS_KEY',
                                  'DJANGO_SECRET_KEY',
                                  'PAPERTRAIL_SERVER']


def run(cmd, *args, **kwargs):
    """
    We're overwriting invoke's "run" to always
    print out the command it's running before it runs.
    It also does color things.
    """
    if not cmd:
        return
    print("====================================")
    print(cmd)
    print("====================================")
    silently_run(cmd, *args, **kwargs)


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
def get_media(media=None):
    if not media:
        run("mkdir -p nginx")
        run("scp -r vagrant@threepanel.com:/home/vagrant/vagrant_django/nginx/media ./nginx/media")
        run("cp -r nginx /tmp/last_nginx")
    else:
        run("cp -r {} media".format(media))


@task
def get_current_db(db=None):
    db_password = os.environ['POSTGRES_DB_PASSWORD']
    if not db:
        run("ssh vagrant@threepanel.com \"sudo -u postgres pg_dump threepanel > /tmp/last.db_backup\"")
        run("scp vagrant@threepanel.com:/tmp/last.db_backup /tmp/last.db_backup")
        run("vagrant scp /tmp/last.db_backup /tmp/last.db_backup")
        vagrant("sudo -u postgres psql -d threepanel -f /tmp/last.db_backup".format(db_password))
    else:
        run("vagrant scp {} /tmp/last.db_backup".format(db))
        vagrant("sudo -u postgres psql -d threepanel -f /tmp/last.db_backup".format(db_password))


@task
def run_python_install_script(vagrant_hostname="default", production=False):
    install_path = "/home/vagrant/vagrant_django/configuration/install.py"
    environment_dict = environment_subset(REQUIRED_ENVIRONMENT_VARIABLES)
    environment_dict['DJANGO_DEBUG'] = str(not production)
    environment_dict['VAGRANT_HOSTNAME'] = vagrant_hostname
    environment_string = environment_dict_to_string(environment_dict)
    cmd = "sudo {} python3 {}".format(environment_string, install_path)
    vagrant(cmd)


@task
def environment():
    e_dict = environment_subset(REQUIRED_ENVIRONMENT_VARIABLES)
    print(environment_dict_to_string(e_dict))

@task
def install(production=False, name="vagrant-devbox", db=None, media=None):
    if not production:
        run("VAGRANT_HOSTNAME={} vagrant up --provider virtualbox".format(name))
        run_python_install_script(vagrant_hostname=name, production=False)
    else:
        get_media(media)
        run("VAGRANT_HOSTNAME={} vagrant up --provider digital_ocean".format(name))
        run_python_install_script(vagrant_hostname=name, production=True)
        vagrant_invoke("auth_keys")

    get_current_db(db)
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
