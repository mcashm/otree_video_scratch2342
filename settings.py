from os import environ

try:
    from secrets import OTREE_ADMIN_PASSWORD, DATABASE_URL
    environ['DATABASE_URL'] = DATABASE_URL
    environ['OTREE_ADMIN_PASSWORD'] = OTREE_ADMIN_PASSWORD
    environ['OTREE_AUTH_LEVEL'] = "DEMO"
    DEBUG=False
except ImportError:
    environ['OTREE_ADMIN_PASSWORD'] = "demo"

environ['OTREE_REST_KEY'] = "demo"

SESSION_CONFIGS = [
    dict(
        name='guess_two_thirds',
        display_name="Guess 2/3 of the Average",
        app_sequence=['guess_two_thirds', 'payment_info'],
        num_demo_participants=3,
    ),
    dict(
        name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    ),

    { "name": "jisti_initial_test",
      "display_name": "Initial 8x8 jitsi test",
      "app_sequence": ["open_video_lab", "public_goods_modified"],
      "num_demo_participants": 3,
      "magic_cookie": environ['JAAS_APP_ID'], # TODO: this is not actually a magic cookie, but is an 'AppId'
      "server_host": "https://otree.ludwig.wbs.ac.uk",
      "blurred_pages": ["open_video_lab/Camera_check","public_goods_modified/Results"]
    },
#    { "name": "dummy",
#      "display_name": "dummy to force otree to update the javascript file",
#      "app_sequence": ["open_video_lab",],
#      "num_demo_participants": 1,
#    },

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)


DEBUG=False

PARTICIPANT_FIELDS = ['jwt_token', 'current_ovl_room', 'main_ovl_room', 'private_ovl_room', 'group_ovl_room']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='wbs3005',
        display_name='wbs3005',
        participant_label_file='_rooms/WBS3005.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '4948265342335'

INSTALLED_APPS = ['otree']



