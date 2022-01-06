from flask import Response, jsonify
import json


def send_200(data={}, location='/'):
  return Response(
      json.dumps(data),
      status=200,
      mimetype='application/json',
      headers={
          "location": location
      }
  )


def send_400(errors=["Invalid Payload"], fields=[], location='/'):
  return Response(
      json.dumps([
          {
              'error': each_error,
              'field': fields[index]
          } if index < len(fields)
          else {
              'error': each_error
          }
          for index, each_error in enumerate(errors)
      ]),
      status=400,
      mimetype='application/json',
      headers={
          "location": location
      }
  )


def send_404(location='/'):
  return Response(
      json.dumps([{
          'error': 'Entity not found'
      }]),
      status=404,
      mimetype='application/json',
      headers={
          "location": location
      }
  )


def send_401(error='Unauthorized', location='/'):
  return Response(
      json.dumps([{
          'error': error
      }]),
      status=401,
      mimetype='application/json',
      headers={
          'location': location
      }
  )
