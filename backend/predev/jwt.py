import jwt
# import base64


payload = {'school': 'udacity'}
algo = 'HS256'
secret = 'learning'

encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
print(encoded_jwt)

decoded_jwt = jwt.decode(encoded_jwt, secret, verify=True)
print(decoded_jwt)
