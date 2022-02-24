## About

Based on this guide: https://realpython.com/token-based-authentication-with-flask/

Also thanks to:

https://github.com/smallwat3r/docker-nginx-gunicorn-flask-letsencrypt
https://citizix.com/how-to-run-mysql-8-with-docker-and-docker-compose/
https://nullonerror.org/2021/11/12/gunicorn-hot-reload-with-docker-compose/
https://stackoverflow.com/questions/43133670/getting-docker-container-id-in-makefile-to-use-in-another-command

## Deploying

### Start Docker Containers and Init Database

```
$ touch .env // fill this file out
$ make dc-start
```

This will start a Docker container for Nginx, the app, and MYSQL and create an initial
database with the tables. It will also run database migrations committed to git history
if the container is being restarted.

## Developing w/ Docker (Preferred)

### Edit `.env` File

Edit the `.env` file with the variables you want like DB name, user, etc.

### Start Containers and Database

Start containers and init database with

```
$ make dc-start-local
```

This will start a Docker container for the MYSQL instance and the application being served by Gunicorn. If you passed the `--reload` flag in your `.env` file, it will also hot reload the app when making changes to the directory without having to restart the container.

### Running Migrations

To run migrations after making DB changes (with the containers running):

```
make dc-migrate
```

This will `exec` into the Docker container and run the migrations. The `./migrations` directory is mounted as a volume so whatever migrations that are published to the container will reflect on your local machine.

## Developing w/out Docker and Instead w/ `venv`

### Install MySQL and Create MySQL User

```
$ brew install mysql
$ brew tap homebrew/services
$ brew services start mysql
$ mysql -u root -p
$ CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
$ GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
$ FLUSH PRIVILEGES;
```

### Edit `.env` File

Edit the `.env` file with the variables you want like DB name, user, etc.

### Set Up venv and Install Requirements

```
$ python3 -m venv ./
$ source bin/activate
$ pip install -r requirements.txt
```

### Run the Project

```
$ flask run
```

### Run Migrations If Needed

```
$ python manage.py db init
$ python manage.py db stamp heads
$ python manage.py db migrate
$ python manage.py db upgrade
```

### Endpoints

#### Register

Creates user and returns token

```
curl --request POST \
  --url http://localhost:5000/register \
  --header 'content-type: application/json' \
  --data '{
	"email": "hi@gmail.com",
	"username": "marty2",
	"password": "mypassword"
}'
```

#### Login

Logs user in and returns token

```
curl --request POST \
  --url http://localhost:5000/register \
  --header 'content-type: application/json' \
  --data '{
	"username": "marty2",
	"password": "mypassword"
}'
```

#### Profile

Gets user's profile

```
curl --request GET \
  --url http://localhost:5000/profile \
  --header 'Authorization: Bearer ${TOKEN_HERE}'
```

#### Logout

Blacklists the passed authorization token

```
curl --request POST \
  --url http://localhost:5000/logout \
  --header 'Authorization: Bearer ${TOKEN_HERE}'
```

## VSCode Settings

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
    },
  "python.formatting.provider": "autopep8",
  "python.formatting.autopep8Args": ["--ignore","E402"],
}
```

Workspace settings:

```json
{
  "editor.defaultFormatter": "ms-python.python",
  "python.pythonPath": "bin/python3",
  "python.linting.pylintArgs": ["--load-plugins", "pylint_flask_sqlalchemy", "pylint_flask"]
}
```
