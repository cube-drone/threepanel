from invoke import task, run
from invoke.exceptions import Failure

def multiple(*args):
    return " && ".join(args)

@task
def vagrant(command):
    try:
        return run("vagrant {}".format(command))
    except Failure:
        return None

@task
def up():
    return vagrant("up")

@task
def ssh():
    return vagrant("ssh")

@task
def sshc(command):
    result = vagrant("ssh -c \"{}\"".format(command))
    if not result or result.failed:
        return run(command)
    else:
        return result

@task(up)
def install():
    sshc("bash /home/vagrant/synced/install.sh")

@task
def devfolder(command):
    return sshc(multiple("cd /home/vagrant/synced/threepanel/",
                  command))

@task
def lint():
    return devfolder(multiple("pep8 */*.py --ignore=\"E128,E501,E402\"",
                       "pyflakes */*.py"))

@task
def watchlint():
    from watchie import Watchie
    w = Watchie()
    w.watch(path=".",
            result_fn=lint)
    w.start()

@task
def dj(command):
    return devfolder("python3 manage.py {}".format(command))

@task()
def runserver():
    print("Running server on localhost:8000")
    return dj("runserver 0:8000")
