STARTUP:
    1: cd/djangoDocker
    2: sudo npm install
    3: npm start
        Wait for webpack to successfully compile, it may take several minutes.
    4: run the django server using the command 'runDjango' via the start/play button in the center of the top toolbar.
        In the new terminal created by this will have a 'preview' line. Click this to enter the server.
        
FAQ:
    - Why is the host I am using disallowed?
        in djangoDocker/djangoDocker/settings/base.py there is an array which contains all allowed hosts.
        Unfortunately codenvy uses different nodes, so every time a new one is chosen for us we must add it to the list.
        In the terminal for the 'runDjango' command, copy the preview URL (ie http://node23.codenvy.io:33186) and add it to the list in the following format:
            http://node23.codenvy.io
    - What does 'no such table: ...' mean?
        The table in the database doesn't exist. Run python manage.py migrate --run-syncdb
    - What can I currently test?
        As of 7/6/2017 the only working apps are "accounts" and "swaggerapp"
        <host>/accounts/[login||logout||signup]
        <host>/swaggerapp
    - local.py/local_base.py is missing?
        Copy and paste local.py.example into django/Docker/djangoDocker/settings with a new named called 'local.py'
        
CURRENT APPS:
    userapi:
        Demonstration of django-rest-framework being used
    swaggerapp:
        Demonstration of django-rest-swagger being used
        
--------------------------------------------------------------------------------------------------
Tools used:
    django-react-boilerplate
        React, for interactive UI development
        django-js-reverse, for generating URLs on JS
        Bootstrap 4, for responsive styling
        Webpack, for bundling static assets
        Celery, for background worker tasks
        WhiteNoise with brotlipy, for efficient static files serving
    
    django-rest-swagger
    
    allauth (https://github.com/pennersr/django-allauth)

SETUP, REACT boilerplate:
    1: Import the REACT boilerplate from https://github.com/vintasoftware/django-react-boilerplate
    2: add "django-rest-swagger" to requirements-to-freeze.txt
    3: pip install -r requirements-to-freeze.txt
    4: pip freeze > requirements.txt
    5: npm update --save
        These 3 commands may require sudo to activate properly
    6: npm outdated
    8: create a file named '.env' in the project directory, which will contain the following:
        DJANGO_SETTINGS_MODULE="{{project_name}}.settings.local"
    9: create a file named 'local.py' in project/project/settings, which will be a copy of local.py.example
    7: Make sure your intended HOST is applied to /projectname/projectname/settings/base.py
    
SETUP, REST swagger:
    1: If needed, install rest framework via 'pip install django-rest-framework' (may require sudo previleges)
        1.1: add 'rest_framework', to INSTALLED_APPS in project/project/settings/base.py
        
    2: If needed, install swagger via 'pip install django-rest-swagger' (may require sudo priveleges)
        2.1: add 'rest_framework_swagger', to INSTALLED_APPS in project/project/settings/base.py
        
    3: https://github.com/marcgibbons/django-rest-swagger/tree/master/example_app will give an example as to how django-rest-swagger is used
    
DOCKER STARTUP:
    1: ensure that directories are up to date
    2: go to root of Project
    3: "docker-compose build" to build the image
    4: "docker-compose up -d" to do first time run of three containers (nginx, django, and postgres)
    5: "docker-compose stop" to stop all containers
    6: "docker-compose start" to start them all again
    7: any changes should be rebuilt by typing "docker-compose build" again
    8 (optional): delete orphaned image by typing "docker rmi <image ID>"