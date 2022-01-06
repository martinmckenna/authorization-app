from flask import request
from functools import wraps
from app.utils.respond import send_401
from app.utils.encode_token import decode_auth_token

from app.models.users import User
from app.models.blacklist import BlacklistToken


def with_auth(secret_key):
    def decorator(f):
      @wraps(f)
      def wrapper(*args, **kwargs):
        if not 'Authorization' in request.headers:
          return send_401("Authorization token is missing.")

        token = request.headers['Authorization']

        try:
          prefix, token = token.split(" ")
          if prefix != 'Bearer':
            return send_401('Invalid authorization token.')
        except:
          return send_401('Invalid authorization token.')

        if not token:
          return send_401('Invalid authorization token.')

        try:
          # Abort if user is trying a blacklisted auth token
          if BlacklistToken.check_blacklist(token):
            return send_401('Token already revoked. Please try again.')

          data = decode_auth_token(token, secret_key)

          # if the decoded token is a string, it means it's an invalid token error
          if isinstance(data, str):
            return send_401(data)

          maybe_user = User.query.filter_by(id=data).first()

          """
          not really sure how current_user ends up as none but need to document how to replicate
          """
          if maybe_user is None:
            return send_401('Invalid authorization token.')
        except:
            return send_401('Invalid authorization token.')

        return f(maybe_user, *args, **kwargs)
      return wrapper
    return decorator
