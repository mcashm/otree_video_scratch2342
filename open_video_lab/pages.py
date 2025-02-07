from otree.api import *
from .models import *
import random, string
from importlib import import_module

class Camera_check(Page):
    @staticmethod
    def live_method(player, data):
        player.participant.vars['message_to_admin'] = data
        print(f"saved message to admin: {data}")

    @staticmethod
    def vars_for_template(player):
        strings = import_module(f"..lang.en.Camera_check_strings", __name__)

        return {'ovl_show_hide_meeting': "hide",
                'i18n' : strings
                }

    def before_next_page(player: Player, timeout_happened):
        player.p_code = random.choice(C.codes_list)
        player.e_code = C.codes_dict[player.p_code]
        player.participant.vars['p_code'] = player.p_code
        player.participant.vars['e_code'] = player.e_code
        #TODO: WARNING, UNDOCUMENTED API, ASSUMES INTERNALS
        player.ready_for_camera_check()




class Camera_questions(Page):
    # def is_displayed(player: Player):
    #     return player.session.config['video'] == True


    form_model = 'player'
    form_fields = ['camera', 'useCamera', 'age',]

    def before_next_page(player: Player, timeout_happened):
        if not all([ (player.camera == 1), (player.useCamera == 1), (player.age >= 26), ]):
            player.cam_consent = 0
            player.participant.vars['cam_consent'] = 0
        else:
            player.cam_consent = 1
            player.participant.vars['cam_consent'] = 1

    
    #def app_after_this_page(player, upcoming_apps):
    #    if not all([ (player.camera == 1), (player.useCamera == 1), (player.age >= 26), ]):
    #        return "Did_not_qualify"
    @staticmethod
    def vars_for_template(player):
        strings = import_module(f"..lang.en.Camera_questions_strings", __name__)
        return {'ovl_show_hide_meeting': "hide",
                'i18n': strings
                }

class Code_exchange(Page):
    form_model = 'player'
    form_fields = [ 'code_input_camera_check',]

    
    def error_message(player: Player, values):
        print('code word entered: ', values)
        player_answer = values['code_input_camera_check']
        # POSSIBLY USE LEVENSHTEIN
        # remove non-letter chars
        for character in string.punctuation:
            player_answer = player_answer.replace(character, '')
        # remove spaces
        player_answer = player_answer.replace(" ", "")
        # make all upper case
        player_answer = player_answer.upper()

        if not ((player_answer == player.e_code) or (player_answer == 'NOVIDEOCHECK')):
            return 'Sorry, the code you entered is not correct. If you cannot get the code please enter: NOVIDEOCHECK'

    def before_next_page(player: Player, timeout_happened):
                #trim and uppercase all player code answers
                #TRIM SPACES HERE
        player_answer = player.code_input_camera_check
        # POSSIBLY USE LEVENSHTEIN
        # remove non-letter chars
        for character in string.punctuation:
            player_answer = player_answer.replace(character, '')
        # remove spaces
        player_answer = player_answer.replace(" ", "")
        # make all upper case
        player_answer = player_answer.upper()

        if player_answer == 'NOVIDEOCHECK':
            player.cam_checked = 0
            player.participant.vars['cam_checked'] = 0
        elif player_answer == player.e_code:
            player.cam_checked = 1
            player.participant.vars['cam_checked'] = 1



        player.participant.vars['condition'] = 99

        
    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars['cam_checked'] == 0:
            return "Did_not_qualify"

    @staticmethod
    def vars_for_template(player):
        strings = import_module(f"..lang.en.Code_exchange_strings", __name__)
        return {'ovl_show_hide_meeting': "show",
                'i18n': strings,
                }

page_sequence = [
                Camera_questions,
                Camera_check,
                Code_exchange,
                ]

ovl_pages_to_blur = [Camera_questions,]
