from invoke import task, run

@task
def vagrant(command):
    run("vagrant {}".format(command))

@task
def up():
    vagrant("up")

@task
def ssh():
    vagrant("ssh")

@task
def sshc(command):
    vagrant("ssh -c \"{}\"".format(command))

@task
def devfolder(command):
    sshc("cd /home/vagrant/synced/threepanel/ && {}".format(command))

@task
def pep8():
    devfolder("pep8 */*.py --ignore=\"E128,E501,E402\"")

@task
def dj(command):
    devfolder("python3 manage.py {}".format(command))

@task()
def runserver():
    dj("runserver 0:8000")
