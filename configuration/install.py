from string import Template
import sys
import subprocess
import os
import configparser
from uuid import uuid4


HOME_PATH = os.environ['HOME']
VAGRANT_DJANGO_PATH = os.path.join(HOME_PATH, 'vagrant_django')
VIRTUALENV_PATH = os.path.join(HOME_PATH, 'django_environment')
CONF_PATH = os.path.join(VAGRANT_DJANGO_PATH, 'configuration')
SCRIPTS_PATH = os.path.join(VAGRANT_DJANGO_PATH, 'scripts')


if not(sys.version_info > (3, 0)):
    sys.stderr.write("You're using python2. Use python3 or higher.")
    exit()


def write_config_template_to_location(template, arguments, destination):
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


def default_input(question, default):
    """
    Just like raw_input, but with a default that gets selected
    if the user just hits enter.
    """
    returnval = input(question + " [{}]: ".format(default))
    if returnval.strip() == "":
        returnval = default
    return returnval.strip()


def is_a_django_directory(path):
    """
    Try to guess if this directory is a valid Django directory
    by checking if it contains 'manage.py'
    """
    manage_py_location = os.path.join(VAGRANT_DJANGO_PATH, path, 'manage.py')
    return os.path.exists(manage_py_location)

def guess_django_path():
    dir_contents = os.listdir(VAGRANT_DJANGO_PATH)
    defaults = ['.git', '.vagrant', 'configuration', '__pycache__']
    candidate_directories = [path for path in dir_contents
                                if os.path.isdir(path)
                                and path not in defaults
                                and is_a_django_directory(path)]
    if len(candidate_directories) > 0:
        return candidate_directories[0]
    else:
        return None

def write_ini_file(config_args):

    ini_file_path = os.path.join(VAGRANT_DJANGO_PATH, 'vars.ini')
    config = configparser.ConfigParser()
    config['config_args'] = config_args

    with open(ini_file_path, 'w') as configfile:
        config.write(configfile)

def read_ini_file():

    ini_file_path = os.path.join(VAGRANT_DJANGO_PATH, 'vars.ini')
    config = configparser.ConfigParser()
    config.read(ini_file_path)

    config_args = {}
    for key in ['home', 'debug', 'project_slug', 'domain', 'admin_name',
                'admin_email', 'mandrill_key', 'secret_key', 'db_password',
                'django_path', 'virtualenv_path']:
        config_args[key] = config.get('config_args', key)
    return config_args

def read_config_from_environment():
    print("Attempting to read config from environment")
    config = {}
    if 'DJANGO_DEBUG' in os.environ:
        config['debug'] = os.environ['DJANGO_DEBUG']
    else:
        print("DJANGO_DEBUG not in environment!")
    if 'DJANGO_PROJECT_SLUG' in os.environ:
        config['project_slug'] = os.environ['DJANGO_PROJECT_SLUG']
        config['django_path'] = os.path.join(VAGRANT_DJANGO_PATH, config['project_slug'])
        config['virtualenv_path'] = VIRTUALENV_PATH
    else:
        print("DJANGO_PROJECT_SLUG not in environment!")
    if 'DJANGO_DOMAIN' in os.environ:
        config['domain'] = os.environ['DJANGO_DOMAIN']
    else:
        print("DJANGO_DOMAIN not in environment!")
    if 'DJANGO_ADMIN_NAME' in os.environ:
        config['admin_name'] = os.environ['DJANGO_ADMIN_NAME']
    else:
        print("DJANGO_ADMIN_NAME not in environment!")
    if 'DJANGO_ADMIN_EMAIL' in os.environ:
        config['admin_email'] = os.environ['DJANGO_ADMIN_EMAIL']
    else:
        print("DJANGO_ADMIN_EMAIL not in environment!")
    if 'MANDRILL_KEY' in os.environ:
        config['mandrill_key'] = os.environ['MANDRILL_KEY']
    else:
        print("MANDRILL_KEY not in environment")
    if 'DJANGO_SECRET_KEY' in os.environ:
        config['secret_key'] = os.environ['DJANGO_SECRET_KEY']
    else:
        print("DJANGO_SECRET_KEY not in environment.")
    if 'POSTGRES_DB_PASSWORD' in os.environ:
        config['db_password'] = os.environ['POSTGRES_DB_PASSWORD']
    else:
        print("POSTGRES_DB_PASSWORD not in environment.")
    if 'HOME' in os.environ:
        config['home'] = os.environ['HOME']
    else:
        print("HOME not in environment.")
    if not config:
        print("Could not read config from environment.")
    return config

def prompt_for_ini_vars():

    default_django_path = guess_django_path()
    if not default_django_path:
        sys.stderr.write("I can't find a Django project anywhere in {}".format(VAGRANT_DJANGO_PATH))
        exit()

    config_args = {}
    config_args['home'] = HOME_PATH
    config_args['debug'] = default_input('Is this a debug instance? True or False?',
                                         default='True').capitalize().strip()
    if config_args['debug'] != 'True' and config_args['debug'] != 'False':
        sys.stderr.write('Do they speak english in {}? I said True or False!'.format(config_args['debug']))
        exit()

    config_args['project_slug'] = default_django_path

    default_domain = "{}.com".format(config_args['project_slug'])
    config_args['domain'] = default_input('What domain will this site be located at?',
                                          default=default_domain)

    config_args['admin_name'] = default_input("What's your name?",
                                              default="Andy Wontshutup")

    config_args['admin_email'] = default_input("What's your e-mail address?",
                                               default="andy@morg.org")

    config_args['mandrill_key'] = default_input("Go to mandrill.com and make an account. Then type your API key in here.",
                                            default="Nope")

    config_args['secret_key'] = str(uuid4())
    config_args['db_password'] = str(uuid4())

    config_args['django_path'] = os.path.join(VAGRANT_DJANGO_PATH, config_args['project_slug'])
    config_args['virtualenv_path'] = VIRTUALENV_PATH

    return config_args


def configure_the_motherfucker(config_args):
    manage_path = os.path.join(config_args['django_path'], 'manage.py')

    # Modify bashrc with helpers
    bashrc_path = os.path.join(HOME_PATH, '.bashrc')
    write_config_template_to_location(template='template.bashrc',
                                      arguments=config_args,
                                      destination=bashrc_path)

    # Put settings.py in place
    settings_path = os.path.join(config_args['django_path'],
                                 config_args['project_slug'],
                                 'settings.py')
    local_settings_path = os.path.join(config_args['django_path'],
                                       config_args['project_slug'],
                                       'local_settings.py')
    write_config_template_to_location(template='template.settings.py',
                                      arguments=config_args,
                                      destination=settings_path)
    if not os.path.exists(local_settings_path):
        write_config_template_to_location(template='template.local.settings.py',
                                          arguments=config_args,
                                          destination=local_settings_path)

    # Put NGINX configuration in place
    nginx_config_path = '/etc/nginx/sites-available/{}'.format(config_args['project_slug'])
    nginx_enabled_path = '/etc/nginx/sites-enabled/{}'.format(config_args['project_slug'])
    write_config_template_to_location(template='template.nginx.conf',
                                      arguments=config_args,
                                      destination=nginx_config_path)
    subprocess.call("ln -s {} {}".format(nginx_config_path, nginx_enabled_path).split())

    # Make a scripts path exist
    subprocess.call("mkdir -p {}".format(SCRIPTS_PATH).split())

    # Put UWSGI configuration in place
    write_config_template_to_location(template='template.uwsgi.sh',
                                      arguments=config_args,
                                      destination='{}/uwsgi.sh'.format(SCRIPTS_PATH))
    subprocess.call("chmod a+x {}/uwsgi.sh".format(SCRIPTS_PATH).split())


    # Put Redis configuration in place
    subprocess.call("mv /etc/redis/redis.conf /etc/redis/redis.conf.backup".split())
    subprocess.call("ln -s {}/template.redis.conf /etc/redis/redis.conf".format(CONF_PATH).split())

    # Put all scripts in place
    scripts = ['template.create_postgres.sh',
               'template.backup_postgres.sh',
               'template.rebuild_postgres.sh',
               'template.reset_postgres.sh']
    for script in scripts:
        filename = script[9:]
        dest = os.path.join(SCRIPTS_PATH, filename)
        write_config_template_to_location(template=script,
                                          arguments=config_args,
                                          destination=dest)
        subprocess.call("dos2unix {}".format(dest).split())

    # Create PostgreSQL Database
    postgres_call = "bash {}/create_postgres.sh".format(SCRIPTS_PATH)
    subprocess.call(postgres_call.split())


if __name__ == '__main__':
    try:
        config_args = read_ini_file()
    except configparser.NoSectionError:
        config_args = read_config_from_environment()
        if not config_args:
            config_args = prompt_for_ini_vars()
        write_ini_file(config_args)

    print(config_args)
    configure_the_motherfucker(config_args)

