install:
	echo 'python tools'
	apt-get install -y python3-pip python-dev sqlite3
	echo 'necessary for bcrypt'
	apt-get install -y libffi-dev
	echo 'pip'
	pip3 install ../deps
	echo 'dev tools'
	apt-get install -y ack-grep
	echo 'foundation'
	apt-get install -y git npm nodejs-legacy python-dev
	npm install -g bower grunt-cli
	gem install foundation compass

run:
	python3 manage.py runserver 0:8000

create_db:
	rm db.sqlite3
	echo "no" | python3 manage.py syncdb
	python3 manage.py streams_test_data

build:
	compass compile foundation

watch:
	compass watch foundation
