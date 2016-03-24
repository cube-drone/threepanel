from string import Template
import sys
import subprocess
import os


HOME_PATH = os.environ['HOME']
VAGRANT_DJANGO_PATH = os.path.join(HOME_PATH, 'vagrant_django')
VIRTUALENV_PATH = os.path.join(HOME_PATH, 'django_environment')
CONF_PATH = os.path.join(VAGRANT_DJANGO_PATH, 'configuration')
SCRIPTS_PATH = os.path.join(VAGRANT_DJANGO_PATH, 'scripts')
DOS2UNIX_ENABLED = 'DOS2UNIX_ENABLED' in os.environ and os.environ['DOS2UNIX_ENABLED'] != "False"


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
    if DOS2UNIX_ENABLED:
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
    print("Installing postgres configuration to /etc/postgresql/9.4/main/postgresql.conf")
    try:
        write_config_template_to_location(template='template.postgresql.conf',
                                          arguments=environment_dict,
                                          destination='/etc/postgresql/9.4/main/postgresql.conf')
    except IOError:
        print("PostgreSQL 9.4 not present on server? Maybe there's another version of postgres here.")

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

    dest = os.path.join(SCRIPTS_PATH, 'remote_syslog.sh')
    print("Installing remote_syslog.sh to {}".format(dest))
    write_config_template_to_location(template='template.remote_syslog.sh',
                                      arguments=environment_dict,
                                      destination=dest,
                                      executable=True)


def defaults(environment_dict):
    """
    Set a bunch of default variables so that we can still install this
    even if everything isn't set
    """
    if not 'VAGRANT_HOSTNAME' in environment_dict:
        environment_dict['VAGRANT_HOSTNAME'] = 'unknown_vm'
    if not 'DJANGO_PROJECT_SLUG' in environment_dict:
        environment_dict['DJANGO_PROJECT_SLUG'] = 'threepanel'
    if not 'DJANGO_DEBUG' in environment_dict:
        environment_dict['DJANGO_DEBUG'] = 'True'
    if not 'DJANGO_DOMAIN' in environment_dict:
        environment_dict['DJANGO_DOMAIN'] = 'localhost'
    if not 'DJANGO_ADMIN_NAME' in environment_dict:
        environment_dict['DJANGO_ADMIN_NAME'] = 'Test Admin'
    if not 'DJANGO_ADMIN_EMAIL' in environment_dict:
        environment_dict['DJANGO_ADMIN_EMAIL'] = 'test@sample.org'
    if not 'MANDRILL_KEY' in environment_dict:
        environment_dict['MANDRILL_KEY'] = 'None'
    if not 'DJANGO_SECRET_KEY' in environment_dict:
        environment_dict['DJANGO_SECRET_KEY'] = '7'
    if not 'POSTGRES_DB_PASSWORD' in environment_dict:
        environment_dict['POSTGRES_DB_PASSWORD'] = 'testpass'
    if not 'PAPERTRAIL_SERVER' in environment_dict:
        environment_dict['PAPERTRAIL_SERVER'] = 'localhost'
        environment_dict['PAPERTRAIL_HOST'] = 'localhost'
        environment_dict['PAPERTRAIL_PORT'] = '514'
    else:
        host, port = environment_dict['PAPERTRAIL_SERVER'].split(":")
        environment_dict['PAPERTRAIL_HOST'] = host
        environment_dict['PAPERTRAIL_PORT'] = port
    if not 'AWS_ACCESS_KEY_ID' in environment_dict:
        environment_dict['AWS_ACCESS_KEY_ID'] = ''
    if not 'AWS_SECRET_ACCESS_KEY' in environment_dict:
        environment_dict['AWS_SECRET_ACCESS_KEY'] = ''
    if not 'VIRTUALENV_PATH' in environment_dict:
        if 'VIRTUALENV' in environment_dict:
            environment_dict['VIRTUALENV_PATH'] = environment_dict['VIRTUALENV']
        else:
            environment_dict['VIRTUALENV_PATH'] = VIRTUALENV_PATH
    return environment_dict

def install(environment_dict):
    """
    Install everything!
    Takes a dictionary of environment variables that must include... various things laid
    out in the README.
    """

    # if we're running on a TRAVIS box, we only need django_settings
    if 'TRAVIS_JOB_NUMBER' in os.environ:
        install_django_settings(environment_dict)
        install_postgres(environment_dict)
        return

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
    env_dict = defaults(env_dict)
    env_dict["DJANGO_PATH"] = os.path.join(VAGRANT_DJANGO_PATH, env_dict["DJANGO_PROJECT_SLUG"])
    for key in env_dict:
        print("{}: {}".format(key, env_dict[key]))
    install(env_dict)

