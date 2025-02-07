from otree.api import *
from .models import *
from .pages import *
from .ExperimenterToDo import *
from .admin import *
#from .jaas_secrets import *


doc = """
Your app description
"""
add_admin_websocket_route()
print("admin websocket route initialised")
