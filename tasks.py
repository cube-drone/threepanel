from __future__ import print_function
import os
import sys

from invoke import run, task

def runprint(cmd, *args, **kwargs):
    """
    like run, but it prints out the thing it's running first
    """
    print(cmd)
    run(cmd, *args, **kwargs)

@task
def env_to_string():
    keys = ['DIGITALOCEAN_API_TOKEN',
            'DJANGO_PROJECT_SLUG',
            'DJANGO_DEBUG',
            'DJANGO_DOMAIN',
            'DJANGO_ADMIN_NAME',
            'DJANGO_ADMIN_EMAIL',
            'POSTGRES_DB_PASSWORD',
            'MANDRILL_KEY',
            'DJANGO_SECRET_KEY']
    for key in keys:
        if key not in os.environ:
            print("Warning: {} not defined.".format(key), file=sys.stderr)
    env_variables = {"{}=\"{}\"".format(key,os.environ[key]) for key in
                     os.environ if key in keys}
    string = " ".join(env_variables)
    return string

@task
def vagrant(command):
    runprint("vagrant ssh -c '{}'".format(command))

@task
def invoke(command):
    runprint(vagrant("source django_environment/bin/activate && cd vagrant_django/threepanel && invoke {}".format(command)))

@task
def runserver():
    invoke("runserver")

@task
def stall(*args, **kwargs):
    return install(*args, **kwargs)

@task
def install(production=False):
    if not production:
        runprint("vagrant up --provider virtualbox")
        install_path = "/home/vagrant/vagrant_django/configuration/install.py"
        cmd = "sudo {} python3 {}".format(env_to_string(), install_path)
        vagrant(cmd)
        invoke("migrate")
    else:
        print("This isn't done yet")


@task
def clean(production=False):
    if not production:
        runprint("vagrant destroy -f")
        runprint("rm -rf vars.ini")
        runprint("rm -rf scripts")
        runprint("rm -rf __pycache__")
    else:
        print("This isn't done yet")
