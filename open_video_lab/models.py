from otree.api import *
from .JaasJWT import generate_jwt


doc = """

Authors: Matthew Cashman, Ty Hayes

This Otree app is designed to provide a video conferencing lab on top of oTree
while filtering out respondents who do not have a good grasp of American English.

It simply measures how quickly the respondent can complete a series of well-known phrases

"""



class C(BaseConstants):
    NAME_IN_URL = 'open_video_lab'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    codes_list = [
        'MONITOR',
        'WALLPAPER',
        'DECKING',
        'RAILROAD',
        'AIRPLANE',
        'OCEAN',
        'MOUNTAIN',
        'DOORBELL',
        'RAINCLOUD',
        'BASKET',
        'LIGHTNING',
        'CASTLE',
        'WINDOW',
        'AUTOMOBILE',
        'HARDWOOD',
        'FIREPLACE',
        'TINSEL',
        'PAINT',
        'GLAZING',
        'UMBRELLA',
        'LAMP',
        'CODING',
        'COOKING',
        'TEDDY',
        'PLANK',
        'WASH',
        'BURLAP',
        'RUNNING',
        'CARVING',
        'BOOK',
        'FENCE',
        'ROOF',
        'CEILING',
        'BOAT',
        'MAGAZINE',
        'SAFETY',
        'BOND',
        'PLANT',
        'SHAVE',
        'TOASTER',
        'CALENDAR',
        'ROCKET',
        'TRUCK',
        'BANANA',
        'CLOUD',
        'DRINK',
        'MENU',
        'RACING',
        'HOTDOG',
        'FARMING',
        'FLYING',
        'CROSSWORD',
        'ELEPHANT',
        'TIGER',
        'CAMEL',
        'COFFEE',
        ]


    codes_dict = {
                    'AIRPLANE': 'DECKING',
                    'AUTOMOBILE': 'AIRPLANE',
                    'BANANA': 'LAMP',
                    'BASKET': 'DOORBELL',
                    'BOAT': 'BOAT',
                    'BOND': 'BURLAP',
                    'BOOK': 'ELEPHANT',
                    'BURLAP': 'CAMEL',
                    'CALENDAR': 'OCEAN',
                    'CAMEL': 'WASH',
                    'CARVING': 'BASKET',
                    'CASTLE': 'CARVING',
                    'CEILING': 'WALLPAPER',
                    'CLOUD': 'MAGAZINE',
                    'CODING': 'RAINCLOUD',
                    'COFFEE': 'FARMING',
                    'COOKING': 'CODING',
                    'CROSSWORD': 'COOKING',
                    'DECKING': 'BOOK',
                    'DOORBELL': 'SHAVE',
                    'DRINK': 'FLYING',
                    'ELEPHANT': 'CROSSWORD',
                    'FARMING': 'SAFETY',
                    'FENCE': 'LIGHTNING',
                    'FIREPLACE': 'HOTDOG',
                    'FLYING': 'TOASTER',
                    'GLAZING': 'TRUCK',
                    'HARDWOOD': 'CASTLE',
                    'HOTDOG': 'PLANK',
                    'LAMP': 'FIREPLACE',
                    'LIGHTNING': 'MOUNTAIN',
                    'MAGAZINE': 'MENU',
                    'MENU': 'RUNNING',
                    'MONITOR': 'UMBRELLA',
                    'MOUNTAIN': 'HARDWOOD',
                    'OCEAN': 'MONITOR',
                    'PAINT': 'RAILROAD',
                    'PLANK': 'CLOUD',
                    'PLANT': 'PAINT',
                    'RACING': 'BANANA',
                    'RAILROAD': 'CALENDAR',
                    'RAINCLOUD': 'TINSEL',
                    'ROCKET': 'RACING',
                    'ROOF': 'FENCE',
                    'RUNNING': 'BOND',
                    'SAFETY': 'AUTOMOBILE',
                    'SHAVE': 'DRINK',
                    'TEDDY': 'TIGER',
                    'TIGER': 'COFFEE',
                    'TINSEL': 'CEILING',
                    'TOASTER': 'WINDOW',
                    'TRUCK': 'ROCKET',
                    'UMBRELLA': 'PLANT',
                    'WALLPAPER': 'ROOF',
                    'WASH': 'TEDDY',
                    'WINDOW': 'GLAZING'
                    }



class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    for player in subsession.get_players():
        #TODO:  move most of this to the extramodel?
        player.jwt_token = generate_jwt(f"Participant {player.participant.code}", session=subsession.session.code, groups=[], valid_for=180) # 3 hour validity
        player.participant.vars['jwt_token'] = player.jwt_token
        player.participant.vars['ovl_subsession_id'] = subsession.id
        player.participant.vars['session_ovl_room_link'] = f"{subsession.session.config['magic_cookie']}/session-{subsession.session.code}"
        player.participant.vars['private_ovl_room_link'] = f"{subsession.session.config['magic_cookie']}/participant-{player.participant.code}"
        player.participant.vars['group_ovl_room_link'] = player.participant.vars['session_ovl_room_link']
        player.participant.vars['current_ovl_room_link'] = player.participant.vars['session_ovl_room_link']
        player.participant.vars['p_code'] = ""
        player.participant.vars['e_code'] = ""
        player.participant.vars['cam_checked'] = -9
        player.participant.vars['ovl_hand_raised'] = False
        player.participant.vars['cam_checked'] = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    jwt_token = models.StringField(blank=True)

    jitsi_screen_url = models.StringField()
    camera = models.BooleanField(
            label="Do you have a working video camera on your computer?",
            choices=[
                [0, 'No'],
                [1, 'Yes'],
                ],
            widget=widgets.RadioSelect
        )
    useCamera = models.BooleanField(
            label="Are you willing to use your computer\'s video camera during your participation in this survey? \
            Please note, the session may be recorded.",
            choices=[
                [0, 'No'],
                [1, 'Yes'],
                ],
            widget=widgets.RadioSelect
        )

    age = models.IntegerField(
            label="How old are you?",
            min=18,
            max=109
            )
    
    p_code = models.StringField()
    e_code = models.StringField()
    code_input_camera_check = models.StringField(
        label="please input the code the researcher gave you here. click next when you've finished talking",
    )

    cam_checked = models.BooleanField()

    cam_consent = models.BooleanField()


    def ready_for_camera_check(self):
        from .ExperimenterToDo import ExperimenterToDo
        ExperimenterToDo.sync_code_exchange(player=self, participant_code=self.participant.code)

    def cam_checkeds(self):
       from otree.channels.utils import channel_utils
       from .admin import session_report_group_name 
       content = {"type": "passed_checks",
                   "participant": self.participant.code}
       channel_utils.sync_group_send(group=session_report_group_name(subsession.session.code), data=content) 




