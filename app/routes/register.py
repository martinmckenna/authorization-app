from flask import Flask, request, jsonify, Blueprint
from app.utils.respond import send_400, send_200
from app.utils.check_missing_keys import check_missing_keys
from app.utils.encode_token import encode_auth_token
from app import bcrypt, db, app
from app.models.users import User

register = Blueprint('register', __name__)


@register.route('/register', methods=['POST'])
def register_user():
  payload = None
  try:
      payload = request.get_json()
  except:
      # payload is prob empty
      return send_400('Payload invalid.')

  keys = [
      'username',
      'email',
      'password'
  ]

  # Check against the list of required keys and see if the user sent all them up
  missing_keys = check_missing_keys(keys, payload)
  if len(missing_keys) > 0:
    return send_400(f'Missing {missing_keys[0]} key.', missing_keys[0])

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

      token = encode_auth_token(user.id, app.config.get('SECRET_KEY'))

      return send_200({
          'email': payload.get('email'),
          'username': payload.get('username'),
          'token': token.decode()
      })
    except:
      return send_400('idk man something went wrong')
  else:
    # User already exists
    return send_400('User already exists.')
