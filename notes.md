
sudo apt-get install python3-pip git npm nodejs-legacy
sudo npm install -g bower grunt-cli
sudo gem install foundation compass
alias dj="python3 /home/vagrant/synced/threepanel/manage.py"


python-social-auth?

I guess the first place to start is getting a user system up and running.

Do I even need a User model? It seems like that comes with the damn thing. 
How about just a UserProfile model to stick stuff like.. uh.. settings. 

We're still at Django 1.6, so we're going to need South, too. 

Oh, let's add a makefile so I don't have to type

    python3 manage.py runserver 0:8000 

a thousand times. 

Let's get this party started with an app! 

... christ, I don't know if I actually want the admin interface. 

Let's worry about that when we get to it.

Authentication
 - Use the built-in Django auth
 - All things are tied to the User object
 - Are you sure you want things tied to the user object? That's kinda
    restrictive down the line. 
 - What if we have an Account object, and it has an optional FK to 
    an auth user? That way we can tie things to the account, like
    settings and profile data and what-have you. 

Account
 - manytomany User
 - preferences JSONfield
 - Title ("Cube Drone")
 - slug ("cube_drone") 
 - FK Theme

Stream 
 - FK Account
 - preferences JSONfield
 - title ("Cube Drone Comics")
 - slug ("comics")
 - FK Theme
 - maxwidth int 

Article
 - Date
 - title
 - slug
 - visible
 - details JSONfield

Content
 - FK Article
 - order int
 - content text
 - details JSONfield
 - type char (choices=renderers)

Image 
 - FK Account
 - S3 Address
 - type (gif/png/jpg) 
 - slug ('awesome_image')
 - tags ('thing', 'thang', 'thingathang') 

Theme
 - manytomany Image

bcrypppppt

Let's get this login and registration thing all set up. 

Everybody starts with one account, which they need to name? 

Ugh. As I imagined, python-social-auth is not going to play nicely with 
a non-SSL localhost VM in dev mode. I'm going to prorogue complex auth 
for now and just say "fuck it, y'all sign in with a username and password 
    for now."

