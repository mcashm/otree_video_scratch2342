from otree.api import *
#from .models import Subsession, Group, Player
from open_video_lab.JaasJWT import generate_jwt

from starlette.routing import WebSocketRoute as WSR
from otree.channels.consumers import _OTreeAsyncJsonWebsocketConsumer
import otree.channels.utils as channel_utils

#WARNING:  THIS WHOLE FILE IS FULL OF UNDOCUMENTED INTERNALS


def session_report_group_name(session_code):
    return f'session-report-{session_code}'


class WSSessionReport(_OTreeAsyncJsonWebsocketConsumer):
    def group_name(self, code):
        return session_report_group_name(code)

    async def post_connect(self, code):
        print(f"connection made to custom ws code : {code}")

    async def post_receive_json(self, data, **kwargs ):
        from .ExperimenterToDo import ExperimenterToDo
        print(data)
        if data['data']['type'] == "raise_hand":
            await ExperimenterToDo.raise_hand(participant_code=data['participant_id'])
            return
        if data['data']['type'] == "lower_hand":
            await ExperimenterToDo.lower_hand(participant_code=data['participant_id'])
            return
        if data['data']['type'] == "todo_done":
            from pprint import pprint
            print("received todo_done with data:")
            pprint(data)
            await ExperimenterToDo.mark_as_completed(data['data']['id'])
            return
        if data['data']['type'] == "query_new_ppt":
            from .ExperimenterToDo import get_participant_from_code
            participant = get_participant_from_code(data['data']['participant_id'])
            print("relaying response:")
            data = {
                     "type": "query_new_ppt_response",
                      "participant_id": data['data']['participant_id'],
                      "checks_completed": False if participant.vars.get("cam_checked", False) == -9 else participant.vars.get("cam_checked", False)
                        }
            print(data)

            await self.relay_message({"data": data,
                                        "participant_code": "admin"
                                     })
            return
        #  This is handled by pages.py in the normal flow of the experiment
        #if data['data']['type'] == "ppt_passed_checks":
        #    from .ExperimenterToDo import get_participant_from_code
        #    participant = get_participant_from_code(data['participant_id'])
        #    participant.vars["checks_completed"] = True
        #    return
        if data['data']['type'] == "admin_lowered_hand":
            await self.relay_message(data)
            return
        #otherwise just relay it
        for group in self.groups:
            print("ws received some unhandled content: ")
            print(data)
            await self.relay_message(data)

    async def relay_message(self, data):
        for group in self.groups:
            print("relaying message on websocket")
            await channel_utils.group_send(group=group, data=data) 
        
def add_admin_websocket_route():
    # We need a livemethod like function that will work regardless of current progres
    from otree.asgi import app
    from starlette.routing import Mount
    from starlette.responses import HTMLResponse
    app.add_websocket_route('/AdminReport/{code}', WSSessionReport)


async def send_to_admin_todo_list(subsession, content):
    await channel_utils.group_send(group=session_report_group_name(subsession.session.code), data=content) 


def sync_send_to_admin_todo_list(subsession, content):
    channel_utils.sync_group_send(group=session_report_group_name(subsession.session.code), data=content) 

def vars_for_admin_report(subsession):

    players = []
    for p in subsession.get_players():
        players.append({'model': p,
                        'participant': p.participant,
                        'code': p.participant.code,
                        'private_ovl_room_link': p.participant.vars['private_ovl_room_link'],
                        'session_ovl_room_link': p.participant.vars['session_ovl_room_link'],
                        'group_ovl_room_link': p.participant.vars['group_ovl_room_link'],
                        'current_ovl_room_link': p.participant.vars['current_ovl_room_link'],
                        })

    from .ExperimenterToDo import ExperimenterToDo

    return {"players": players,
            "session_ovl_room_link": f"{subsession.session.config['magic_cookie']}/session-{subsession.session.code}",
            "main_room_jwt": generate_jwt("Experimenter", moderator=True, session=subsession.session.code),
            "private_room_jwt": generate_jwt("Extramenter ", moderator=True, session=subsession.session.code),
            "todo_list": ExperimenterToDo.filter(_subsession=subsession, finished=False),

            }


