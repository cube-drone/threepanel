Threepanel Continuous Integration Edition
-----------------------------------------

1. Requirements:
 * python3
 * vagrant
 * virtualbox

2. `vagrant plugin install vagrant-scp`

3. `vagrant plugin install vagrant-digitalocean`

2. `pyvenv ./threepenv`

3. `source threepenv/bin/activate`

4. `pip install --upgrade pip`

5. `pip install -r requirements.txt`

6. Set environment variables. You might add these to your `.bashrc` or `.bash_profile`
```
    export DIGITALOCEAN_API_TOKEN="digitalooooocean"
    export DJANGO_PROJECT_SLUG="threepanel"
    export DJANGO_DEBUG="True"
    export DJANGO_DOMAIN="threepanel.com"
    export DJANGO_ADMIN_NAME="Curtis Lassam"
    export DJANGO_ADMIN_EMAIL="curtis@lassam.net"
    export MANDRILL_KEY="maaaaandriiiiiilllll"
    export DJANGO_SECRET_KEY="seeeecreeeet"
    export POSTGRES_DB_PASSWORD="daaaaatabaaaaaaase"
```
8. The server that threepanel.com points to is going to change a lot, so add this to your ssh config:
```
Host threepanel.com
    StrictHostKeyChecking no
```
7. `invoke install`
