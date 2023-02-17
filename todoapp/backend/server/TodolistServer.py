import jwt
import datetime


def encode_auth_token(user_info):
  """
  Generates the Auth Token
  :return: string
  """
  try:
    payload = {
      'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
      'iat': datetime.datetime.utcnow(),
      'sub': user_info
    }
    return jwt.encode(
      payload,
      key='\xcfj\xc8\x04[x\xbc\xb8\x9d7\xa7\xe7\xff\xf9r\x15w\xf4j\xda-\x13F\xaa',
      algorithm='HS256'
    )
  except Exception as e:
    return e



def decode_auth_token(auth_token):
  """
  Decodes the auth token
  :param auth_token:
  :return: integer|string
  """
  try:
    payload = jwt.decode(auth_token, '\xcfj\xc8\x04[x\xbc\xb8\x9d7\xa7\xe7\xff\xf9r\x15w\xf4j\xda-\x13F\xaa', algorithms='HS256')
    return (200,payload['sub'])
  except jwt.ExpiredSignatureError:
    return (400,'Signature expired. Please log in again.')
  except jwt.InvalidTokenError:
    return (401,'Invalid token. Please log in again.')


# token = encode_auth_token('zuqiang')
# print(token)

a = decode_auth_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzY0NTM3MTAsImlhdCI6MTY3NjQ1MzcwNSwic3ViIjoienVxaWFuZyJ9.Vkptg-8WyhugUWhzLKphPF7GavaSmbCtOvYMhQpCaZg')
print(a)
