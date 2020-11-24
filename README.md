## Developing

### Set Up venv

```
$ python3 -m venv auth-test
$ source bin/activate
$ pip install -r requirements.txt
```

### Run the Project

```
$ flask run
```

### Endpoints

#### Register

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

```json
{
  "python.pythonPath": "bin/python3",
  "python.linting.pylintArgs": ["--load-plugins", "pylint_flask_sqlalchemy", "pylint_flask"]
}
```
