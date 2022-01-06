## About

Based on this guide: https://realpython.com/token-based-authentication-with-flask/

## Developing

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

### Set Up venv

```
$ python3 -m venv ./
$ source bin/activate
$ pip install -r requirements.txt
```

### Run the Project

```
$ flask run
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

## Run Migrations

```
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
```
