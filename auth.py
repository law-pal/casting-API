import json
from flask import request, _request_ctx_stack, redirect, session
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from functools import wraps


AUTH0_DOMAIN = 'lawrencep.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'agency'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
   implements get_token_auth_header() method
   it should attempt to get the header from the request
   it should raise an AuthError if no header is present
   it should attempt to split bearer and the token
   it should raise an AuthError if the header is malformed
   return the token part of the header
'''
def get_token_auth_header():
    #Obtains token from header
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
            }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
            }, 401)

    elif len(parts) == 1:
         raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
            }, 401)

    elif len(parts) > 2:
         raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token'
            }, 401)

    token = parts[1]
    return token

'''
   implements check_permissions(permission, payload) method
    it should raise an AuthError if permissions are not included in the payload
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
   
    if payload.get('permissions'):
        token_scopes = payload.get('permissions')
        if (permission not in token_scopes):
            raise AuthError(
                {
                    'code': 'invalid_permissions',
                    'description': 'User does not have enough privileges'
                }, 401)
        else:
            return True
    else:
        raise AuthError(
            {
                'code': 'invalid_permissions',
                'description': 'User does not have any roles attached'
            }, 401)

'''
   implement verify_decode_jwt(token) method
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
'''
def verify_decode_jwt(token):
    #get public key from auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    #gets data in header
    unverified_header = jwt.get_unverified_header(token)

    #choose our key
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
            }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    #verifies key
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. please, check the audience and issuer.'
                }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'
                }, 400)


    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to parse authentication token.'
        }, 400)

'''
   implements @requires_auth(permission) decorator method
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Access denied due to invalid token.'
                    }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

def requires_signed_in(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'jwt_token' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated