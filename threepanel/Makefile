install:
	echo 'python tools'
	apt-get install -y python3-pip python-dev sqlite3
	echo 'necessary for bcrypt'
	apt-get install -y libffi-dev
	echo 'pip'
	pip3 install ../deps
	echo 'foundation'
	apt-get install -y git npm nodejs-legacy python-dev
	npm install -g bower grunt-cli
	gem install foundation compass

run:
	python3 manage.py runserver 0:8000

build:
	compass compile foundation

watch:
	compass watch foundation
