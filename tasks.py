from invoke import task, run
from invoke.exceptions import Failure

def multiple(*args):
    return " && ".join(args)

@task()
def install():
    run("chmod a+x /home/vagrant/synced/install.sh")
    run("chmod a+x /home/vagrant/synced/resetdb.sh")
    run("bash /home/vagrant/synced/install.sh")

@task
def dev(command):
    return run(multiple("cd /home/vagrant/synced/threepanel/", command))

@task
def lint():
    return dev(multiple("pep8 */*.py --ignore=\"E128,E501,E402\"",
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
    return dev("python3 manage.py {}".format(command))

@task()
def runserver():
    print("Running server on localhost:8080")
    return dj("runserver 0:8080")

@task()
def celery():
    print("Activating celery worker")
    return dev("celery --app=threepanel worker -l info")

@task()
def beat():
    print("We love the beat we love the beat... we love the beat!")
    return dev("celery --app=threepanel beat")

@task()
def clear():
    dj("clear_cache")

@task()
def reset():
    print("Resetting db")
    #absolutely remove these lines once you've deployed
    run("rm -rf /home/vagrant/synced/threepanel/comics/migrations/00*")
    run("rm -rf /home/vagrant/synced/threepanel/dashboard/migrations/00*")
    run("rm -rf /home/vagrant/synced/threepanel/publish/migrations/00*")

    run("bash /home/vagrant/synced/resetdb.sh")
    dj("makemigrations")
    dj("migrate --noinput")
    dj("testdata")

@task
def prod_restart():
    run("sudo service uwsgi restart")

@task
def prod_start()
    run("sudo service uwsgi start")

