from otree.api import *
#WARNING: Undocumented Internals
from otree.models.participant import Participant
from .__init__ import Subsession, Group, Player
import time


def get_participant_from_code(participant_code):
    #WARNING: Undocumented Internals
    participant = Participant.objects_get(code=participant_code)
    return participant

def get_subsession_from_participant_code(participant_code):
    participant = get_participant_from_code(participant_code)
    #WARNING: Undocumented Internals
    subsession = Subsession.objects_get(id=participant.vars['ovl_subsession_id']) 
    return subsession
    


class ExperimenterToDo(ExtraModel):
    _participant_code = models.StringField() #either player or participant code required
    _subsession = models.Link(Subsession) # required
    _player = models.Link(Player) #either player or participant code required

    todo_type = models.StringField()
    title = models.StringField()
    content = models.StringField()
    timestamp = models.IntegerField()
    finished = models.BooleanField(default=False)
    
    def mark_as_completed(self):
        self.finished = True


    def __json__(self):
        apparently_not_a_dict = dict(self.__dict__)
        apparently_not_a_dict.pop("_sa_instance_state", None)
        apparently_not_a_dict.pop("_subsession", None)
        
        import json
        from pprint import pprint
        pprint(apparently_not_a_dict)
        return json.dumps(apparently_not_a_dict)

    @property
    def session(self):
        return self.subsession.session

    @property
    def participant(self):
        if _player:
            return player.participant
        elif _participant_code:
            for p in self.subsession.get_players():
                if p.participant.code == _participant_code:
                    return p.participant
        else:
            return None

    @staticmethod
    def find(subsession, **kwargs): #have to include subsession this because ExtraModel.filter has to have a model as one of its arguments
        filtered_todos = ExperimenterToDo.filter(_subsession=subsession)
        for arg in kwargs:
            filtered_todos = [todo for todo in filtered_todos if getattr(todo, arg) == kwargs[arg] ]
        return filtered_todos

    @staticmethod
    async def mark_as_completed(todo_id):
        #WARNING: Undocumented Internals
        print("MARK AS COMPLETED - STATIC METHOD RUNNING")
        todo = ExperimenterToDo.objects_get(id=todo_id)
        todo.finished = True
        if todo.todo_type == "raised_hand":
            from .admin import send_to_admin_todo_list
            data =  {"data": {"type": "admin_lowered_hand", "participant_code": todo._participant_code}, "participant_code": "admin"} 

            get_participant_from_code(todo._participant_code).vars['ovl_hand_raised'] = False

            await send_to_admin_todo_list(todo._subsession, data)
            
        
    @staticmethod
    async def raise_hand(player=None, participant_code=None):
        print(f"creating raised hand.  got args: player {player}, participant_code {participant_code}")
        if player is not None:
            participant_code = player.participant.code
            participant = player.participant
        if participant_code is not None:
            subsession = get_subsession_from_participant_code(participant_code)
            participant = get_participant_from_code(participant_code)

            data = { 
                   "todo_type": "raised_hand",
                   "title": "A participant has their hand raised",
                   "message": f"Participant {participant_code} has their hand raised, \
                                            <button type=\"button\" class=\"create_breakout btn btn-primary\" data-participant_code={participant_code}>Click here</button> to move them into a breakout room to talk with them",
                    }
            extant_hands = ExperimenterToDo.find(subsession, _participant_code = participant_code, todo_type="raised_hand")
            hand = None
            if extant_hands:
                hand = extant_hands[0]
                hand.finished = False
            else:
                hand = ExperimenterToDo.create_message(participant_code=participant_code, **data)

            get_participant_from_code(participant_code).vars['ovl_hand_raised'] = True

            from .admin import send_to_admin_todo_list
            await send_to_admin_todo_list(get_subsession_from_participant_code(participant_code), {"type": "new_todo", "data": hand.__json__()} )
        else: 
            raise ValueError("ExperimenterToDo.create_raised_hand requires either player or participant_code to be set")

    @staticmethod
    async def lower_hand(player=None, participant_code=None):
        if player is not None:
            participant_code = player.participant.code
        if participant_code is None:
            raise ValueError("ExperimenterToDo.create_raised_hand requires either player or participant_code to be set")


        subsession = get_subsession_from_participant_code(participant_code)
        extant_hands = ExperimenterToDo.find(subsession, _participant_code = participant_code, todo_type="raised_hand")
        if extant_hands:
            hand = extant_hands[0]
            hand.finished = True

        get_participant_from_code(participant_code).vars['ovl_hand_raised'] = False

        from .admin import send_to_admin_todo_list
        await send_to_admin_todo_list(subsession, {"type": "lower_hand", "data": {"participant_id": participant_code}} )
    

    @staticmethod
    def sync_code_exchange(player=None, participant_code=None):
        code_exchange_todo = ExperimenterToDo.code_exchange_internal(player=player, participant_code=participant_code)
        from .admin import sync_send_to_admin_todo_list
        sync_send_to_admin_todo_list(get_subsession_from_participant_code(participant_code), {"type": "new_todo", "data": code_exchange_todo.__json__()} )

    @staticmethod
    async def code_exchange(player=None, participant_code=None):
        code_exchange_todo = ExperimenterToDo.code_exchange_internal(player=player, participant_code=participant_code)
        from .admin import send_to_admin_todo_list
        await send_to_admin_todo_list(get_subsession_from_participant_code(participant_code), {"type": "new_todo", "data": code_exchange_todo.__json__()} )

    @staticmethod
    def code_exchange_internal(player=None, participant_code=None):
        if player is not None:
            participant_code = player.participant.code
        if participant_code is not None:
            subsession = get_subsession_from_participant_code(participant_code)
            participant = get_participant_from_code(participant_code)
        else: 
            raise ValueError("ExperimenterToDo.code_exchange requires either player or participant_code to be set")


        extant_item = ExperimenterToDo.find(subsession, _participant_code = participant_code, todo_type="code_exchange")
        if extant_item:
            extant_item.delete()

        code_exchange_todo = ExperimenterToDo.create_message(participant_code = participant_code,
                                        todo_type = "code_exchange",
                                        title = "A participant is ready for the code exchange",
                                        message = f"Code participant should give: <span class=\"fw-bold\">{participant.vars['p_code']}</span><br/>\
                                                Code participant needs: <span class=\"fw-bold\">{participant.vars['e_code']}</span><br/>\
                                                <button type=\"button\" class=\"create_breakout btn btn-primary\" data-participant_code={participant_code}>Click here</button> to move them into a breakout room to talk with them")
        
                                        
        print("created code_exchange_todo. sending to the websocket")
        return code_exchange_todo
        

        
    @staticmethod
    def create_message(title, message, player=None, participant_code=None, todo_type=None):
        created_message = None
        if player is not None:
            created_message = ExperimenterToDo.create(_subsession=player.subsession, 
                                      _player=player,
                                      title=title,
                                      content=message,
                                      todo_type=todo_type,
                                      timestamp=time.time())
        elif participant_code is not None:
            subsession = get_subsession_from_participant_code(participant_code)
            created_message = ExperimenterToDo.create(_subsession=subsession, 
                                      _participant_code=participant_code,
                                      title=title,
                                      content=message,
                                      todo_type=todo_type,
                                      timestamp=time.time())
        else: 
            raise ValueError("ExperimenterToDo.create_message requires either player or participant_code to be set")
        print("message_created")
        print(created_message)
        return created_message
