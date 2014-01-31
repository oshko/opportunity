opportunity
===========

a web application dedicated to help people find jobs

Installation
============

You can check out the source code from https://github.com/kern3020/opportunity.git.

You'll need a database. I'm using Postgres. On ubuntu 12.04 LTS. 

       sudo apt-get install postgresql
       sudo apt-get install pgadmin3
       sudo apt-get install postgresql-server-dev-9.1
       sudo apt-get install python-dev

If you want to use a different database, it should be straight
forward. You'll need to figure how to install the driver for the
database of your choice.

I recommend the creation and activiation of a virtualenv. Then install
these python modules.

      sudo pip install -r requirements.txt 

To populate the database....      

	./manage.py syncdb 
	./manage.py migrate tracker
	./manage.py runserver
