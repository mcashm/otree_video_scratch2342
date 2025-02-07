import jwt
import json
from cryptography.hazmat.primitives import serialization
import uuid
import time
import os
#from .jaas_secrets import KEY_PATH, KID, APP_ID

#TODO: WARNING - UNDOCUMENTED INTERNALS
from otree.common2 import url_of_static
def get_session_from_code(code):
    from otree.models import Session
    #WARNING: Undocumented Internals
    session = Session.objects_get(code=code)
    return session

def prepare_rsa_key():
    # read and load the key
    private_key = os.environ['JAAS_PRIVATE_KEY']
    key = serialization.load_pem_private_key(private_key.encode(), password=None)
    return key

KEY = None
KID = None
APP_ID = None
try:
    KEY = prepare_rsa_key()
    KID = os.environ['KEY_ID']
    APP_ID = os.environ['JAAS_APP_ID']
except:
    print("Environment variables for 8x8 subscription not set. You will not be able to launch a video conference.")
    raise


# This method will create an appropriate JWT for 8x8 jaas
# 
# params:
#   display_name: the name that will display in the jitsi videoconference for the associated user
#   moderator: whether or not the user assigned this token will be granted moderator powers
#              in the jitsi video conference.  Defaults to false.
#   valid_for: a time in minutes for which the key is valid for. Defaults to 1 hour
#   key: a pem format private key for signing.  The public key must be uploaded to the 8x8 api 
#        console and the corresponding kid included in the header so 8x8 can identify the key 
#        to use for verifying the claims
#   kid: the kid from the 8x8 api admin section corresponding to the key
#   appId: the 8x8 api AppID from the 8x8 api console

def generate_jwt(display_name, key=KEY, kid=KID, app_id=APP_ID, moderator=False, valid_for=60, session=None, groups=[]):

    if KID is None:
        return "errorin8x8config"
    

    id = str(uuid.uuid4())
    
    expiry = int(time.time()) + valid_for * 60
    print(session)


    valid_for_rooms = []

    #if moderator:
    #    valid_for_rooms = "*"
    #else:
    #    valid_for_rooms.append(f"session-{session}")
    #    for group_room in groups:
    #        valid_for_rooms.append(f"group-{group_room}")

    print("jwt valid_for_rooms:") 
    print(valid_for_rooms) 
    payload_data = {
      "aud": "jitsi",
      "context": {
        "user": {
          "id": id,
          "name": display_name,
          # "email": "john.doe@company.com",
          "moderator": moderator
        },
        "features": {
          "livestreaming": "false",
          "outbound-call": "false",
          "transcription": "false",
          "recording": "false"
        },
        "room": {
          "regex": False
        }
      },
      "exp": expiry,
      "iss": "chat",
      "nbf": time.time(),
      "room": "*", #json.dumps(valid_for_rooms),
      "sub": app_id
    }
    

    if moderator == True:
        payload_data['context']['user']['avatar'] = f"{get_session_from_code(session).config.get('server_host')}/{url_of_static('open_video_lab/experimenter-avatar.png')}"

    new_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256',
        headers = {'kid': kid}
    )
    
    return new_token
