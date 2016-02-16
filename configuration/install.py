from string import Template
import sys
import subprocess
import os


HOME_PATH = os.environ['HOME']
VAGRANT_DJANGO_PATH = os.path.join(HOME_PATH, 'vagrant_django')
VIRTUALENV_PATH = os.path.join(HOME_PATH, 'django_environment')
CONF_PATH = os.path.join(VAGRANT_DJANGO_PATH, 'configuration')
SCRIPTS_PATH = os.path.join(VAGRANT_DJANGO_PATH, 'scripts')


if not sys.version_info > (3, 0):
    sys.stderr.write("You're using python2. Use python3 or higher.")
    exit()


def write_config_template_to_location(template, arguments, destination, executable=False):
    """
    Poof! It's the entire template engine in one function.

    We use python's String.template language. Read the template from
    a file, apply the arguments to the template, and then
    write that file to a destination.

    template: the name of the file in CONF_PATH that contains a python
        string.Template style template to render.
    arguments: a dictionary of arguments to pass to the template.
    destination: the place in the filesystem to write this file to.
    """
    print("Writing to {}".format(destination))
    with open(os.path.join(CONF_PATH, template), 'r') as template_file:
        template = Template(template_file.read())
        rendered_template = template.substitute(arguments)
    with open(destination, 'w') as target_file:
        target_file.write(rendered_template)
    # Sometimes we're running this from unix and all of our line endings
    #   show up borked.
    subprocess.call("dos2unix {}".format(destination).split())
    if executable:
        subprocess.call("chmod a+x {}".format(destination).split())



def install_bashrc(environment_dict):
    """
    We add some convenience methods to the .bashrc, like 'dj' and 'in'
    as well as all of the environment variables used to build this VM.
    """
    bashrc_path = os.path.join(HOME_PATH, '.bashrc')
    print("Installing bashrc to {}".format(bashrc_path))
    write_config_template_to_location(template='template.bashrc',
                                      arguments=environment_dict,
                                      destination=bashrc_path)


def install_django_settings(environment_dict):
    """
    Django's settings.py depends on a lot of variables we set when
    running this installation script.
    """
    settings_path = os.path.join(environment_dict['DJANGO_PATH'],
                                 environment_dict['DJANGO_PROJECT_SLUG'],
                                 'settings.py')
    print("Installing django's settings.py to {}".format(settings_path))
    write_config_template_to_location(template='template.settings.py',
                                      arguments=environment_dict,
                                      destination=settings_path)


def install_nginx(environment_dict):
    # Put NGINX configuration in place
    nginx_config_path = '/etc/nginx/sites-available/{}'.format(environment_dict['DJANGO_PROJECT_SLUG'])
    nginx_enabled_path = '/etc/nginx/sites-enabled/{}'.format(environment_dict['DJANGO_PROJECT_SLUG'])
    print("Installing nginx configuration to {}".format(nginx_config_path))
    write_config_template_to_location(template='template.nginx.conf',
                                      arguments=environment_dict,
                                      destination=nginx_config_path)
    subprocess.call("ln -s {} {}".format(nginx_config_path, nginx_enabled_path).split())


def install_redis(environment_dict):
    print("Installing redis configuration to /etc/redis/redis.conf")
    subprocess.call("mv /etc/redis/redis.conf /etc/redis/redis.conf.backup".split())
    write_config_template_to_location(template='template.redis.conf',
                                      arguments=environment_dict,
                                      destination='/etc/redis/redis.conf')


def install_postgres(environment_dict):
    scripts = ['template.create_postgres.sh',
               'template.backup_postgres.sh',
               'template.rebuild_postgres.sh',
               'template.reset_postgres.sh']
    for script in scripts:
        filename = script[9:]
        dest = os.path.join(SCRIPTS_PATH, filename)
        print("Installing {} to {}".format(script, dest))
        write_config_template_to_location(template=script,
                                          arguments=environment_dict,
                                          destination=dest,
                                          executable=True)

    # Create PostgreSQL Database
    postgres_call = "bash {}/create_postgres.sh".format(SCRIPTS_PATH)
    subprocess.call(postgres_call.split())


def install_uwsgi(environment_dict):
    dest = os.path.join(SCRIPTS_PATH, 'uwsgi.sh')
    print("Installing uwsgi.sh to {}".format(dest))
    write_config_template_to_location(template='template.uwsgi.sh',
                                      arguments=environment_dict,
                                      destination=dest,
                                      executable=True)


def install_celery(environment_dict):
    dest = os.path.join(SCRIPTS_PATH, 'celery.sh')
    print("Installing celery.sh to {}".format(dest))
    write_config_template_to_location(template='template.celery.sh',
                                      arguments=environment_dict,
                                      destination=dest,
                                      executable=True)


def install_papertrail(environment_dict):
    """
    If we're in production, we also want to send all of our logs to the papertrail server.
    """
    if environment_dict['DJANGO_DEBUG'] == "False":
        print("Installing papertrail server to /etc/rsyslog.conf ")
        with open("/etc/rsyslog.conf", "a") as conf:
            conf.write("*.*          @{}".format(environment_dict['PAPERTRAIL_SERVER']))


def install(environment_dict):
    """
    Install everything!
    Takes a dictionary of environment variables that must include... various things laid
    out in the README.
    """
    install_bashrc(environment_dict)
    install_django_settings(environment_dict)
    install_nginx(environment_dict)
    install_redis(environment_dict)
    install_postgres(environment_dict)
    install_uwsgi(environment_dict)
    install_celery(environment_dict)
    install_papertrail(environment_dict)


if __name__ == '__main__':
    env_dict = dict(os.environ)
    env_dict["DJANGO_PATH"] = os.path.join(VAGRANT_DJANGO_PATH, env_dict["DJANGO_PROJECT_SLUG"])
    env_dict["VIRTUALENV_PATH"] = VIRTUALENV_PATH
    for key in env_dict:
        print("{}: {}".format(key, env_dict[key]))
    install(env_dict)

