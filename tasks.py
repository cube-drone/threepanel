from invoke import task, run

def multiple(*args):
    return " && ".join(args)

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
def install():
    sshc(multiple("sudo apt-get install -y python3 python3-pip",
                  "sudo pip3 install -r /home/vagrant/synced/requirements.txt --upgrade"))


@task
def devfolder(command):
    sshc(multiple("cd /home/vagrant/synced/threepanel/",
                  command))

@task
def lint():
    devfolder(multiple("pep8 */*.py --ignore=\"E128,E501,E402\"",
                       "pyflakes */*.py"))

@task
def dj(command):
    devfolder("python3 manage.py {}".format(command))

@task()
def runserver():
    dj("runserver 0:8000")
