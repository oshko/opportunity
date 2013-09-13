=====================
PaaS
=====================

This django-based web application is based on a lot of standard open
source projects. It can run a wide variety of PaaS. However, there is
some work to get it to run on each. This page documents issues
encountered along the way. 

Heroku
=====================

At the root level, you'll see three Heroku specific files. 
* Procfile - invoke the webserver.
* requirements.txt - This is a well-known filename for pip. Heroku expects to see it at the root. 
* runtime.txt - Heroku specific file which defines python runtime.

At the time of writing, there are some quirks to getting static files
served up correctly. Heroku expects to see a static at in the project
directory. To force this to exist, I have created
opportunity/static/readme.txt.  
