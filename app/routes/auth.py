from flask import Flask, request, jsonify, Blueprint
from app.utils.respond import send_400, send_200
from app.utils.check_missing_keys import check_missing_keys
from app.utils.encode_token import encode_auth_token
from app import bcrypt, db, app
from app.models.users import User
from app.models.blacklist import BlacklistToken
from app.decorators.with_auth import with_auth

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register_user():
  payload = None
  try:
      payload = request.get_json()

      if not payload:
        return send_400(['Payload invalid.'])
  except:
      # payload is prob empty
      return send_400(['Payload invalid.'])

  keys = [
      'username',
      'email',
      'password'
  ]

  # Check against the list of required keys and see if the user sent all them up
  missing_keys = check_missing_keys(keys, payload)
  errors = [
      f'Missing {each_key}.'
      for index, each_key in enumerate(missing_keys)
  ]
  if len(missing_keys) > 0:
    return send_400(errors, missing_keys)

  # Does this user already exist?
  maybe_user = User.query.filter_by(email=payload.get('email')).first()

  if not maybe_user:
    # user doesn't exist in the DB
    try:

      user = User(
          email=payload.get('email'),
          username=payload.get('username'),
          password=payload.get('password'),
      )

      db.session.add(user)
      db.session.commit()

      user_id = User.query.filter_by(email=payload.get('email')).first().id

      token = encode_auth_token(user_id, app.config.get('SECRET_KEY'))
      decoded_token = token.decode()

      return send_200({
          'email': user.email,
          'username': user.username,
          'token': decoded_token,
          'registered_on': user.registered_on
      })
    except:
      return send_400(['idk man something went wrong'])
  else:
    # User already exists
    return send_400(['User already exists.'])


@auth.route('/login', methods=['POST'])
def login_user():
  payload = None
  try:
      payload = request.get_json()

      if not payload:
        return send_400(['Payload invalid.'])
  except:
      # payload is prob empty
      return send_400(['Payload invalid.'])

  keys = [
      'username',
      'password'
  ]

  # Check against the list of required keys and see if the user sent all them up
  missing_keys = check_missing_keys(keys, payload)
  errors = [
      f'Missing {each_key}.'
      for index, each_key in enumerate(missing_keys)
  ]
  if len(missing_keys) > 0:
    return send_400(errors, missing_keys)

  # Does this user already exist?
  maybe_user = User.query.filter_by(username=payload.get('username')).first()

  if maybe_user:
    # user doesn't exist in the DB
    try:

      if bcrypt.check_password_hash(
          maybe_user.password, payload.get('password')
      ):
        token = encode_auth_token(maybe_user.id, app.config.get('SECRET_KEY'))

        return send_200({
            'email': maybe_user.email,
            'username': maybe_user.username,
            'token': token.decode(),
            'registered_on': maybe_user.registered_on
        })
      else:
        return send_400(['Invalid password.'], ['password'])
    except:
      return send_400(['idk man something went wrong'])
  else:
    # User already exists
    return send_400(['Username does not exist.'], ['username'])


@auth.route('/profile', methods=['GET'])
@with_auth(app.config.get('SECRET_KEY'))
def get_profile(user):
  if user:
    return send_200({
        'username': user.username,
        'email': user.email,
        'registered_on': user.registered_on
    })
  else:
    return send_400(["User not found."])


@auth.route('/logout', methods=['POST'])
@with_auth(app.config.get('SECRET_KEY'))
def logout(user):
  # mark the token as blacklisted
  auth_token = request.headers['Authorization'].split(" ")[1]
  blacklist_token = BlacklistToken(token=auth_token)
  try:
    # insert the token
    db.session.add(blacklist_token)
    db.session.commit()
    return send_200()
  except:
    return send_400()
