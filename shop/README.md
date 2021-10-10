# TEST FRONT

## Get started
### Clone the repository

    git clone https://github.com/Yariquezz/test_front.git
    cd test_front

### Create virtualenv

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    cd test_front
    pip install -r requirements.txt


### Install databases

By default, I am using Postgresql, but you can use whatever you want!

    sudo apt install postgresql
    sudo -u postgres psql
    postgres=# create database awesome;
    postgres=# create user user1 with encrypted password 'password';
    postgres=# grant all privileges on database awesome to user1;

To exit from postgresql:

    postgres=# \q

### Make migrations

    cd test_front/awesome
    python manage.py makemigrations
    python manage.py migrate

### Run the sample server
    
    python3 manage.py runserver 8000

Open your favorite browser and follow the link http://127.0.0.1:8000/

# Voila! It's works!



