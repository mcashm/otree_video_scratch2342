# Before you start

Follow the instructions in the [Installation and Usage section](INSTALLATION_AND_USAGE.md).

# Create a session

Sessions can be created using any of the usual methods within oTree - demo sessions from the homepage, regular sessions via the Sessions tab, or in Rooms.

> [!NOTE]
> The waiting room at the start of a session based in a Room is not currently compatible with the video lab.  You can still run a session in a room
> but the video lab will not appear for participants until the session has been created. 

# Before you distribute the link to participants

Open the 'Report' tab within the session admin interface.   

> [!IMPORTANT]
> This is necessary to activate the queue for the 'todo' list.  If you do not have this page open from the start of the session, you might miss messages from participants.

> [!WARNING]
> TODO: 
> - move the todo list from a simple live list held in the browser into an `ExtraModel` that can persist, and the experimenter can tick things off as they need

Open the video conferencing windows.

> [!IMPORTANT]
> Automatically moving new participants into waiting rooms requires a moderator (i.e. an oTree admin) to be in the main room.  If you do not have a window open when participants start joining, they will join directly into the main room.

# Verifying Participants

When a participant first joins, they will automatically be moved into a private breakout room, where they can make sure their microphone and camera are working properly with the Jitsi Videoconferencing window.  There is some initial guidance for the participants to help themselves solve any problems, and a raise hand button to ask for experimenter assistance at this stage.

Once a participant confirms their own camera and microphone is working in the videochat window, they will be shown an individual code word to give to the experimenter, so that the experimenter can verify that they can hear the participant.  In turn, the experimenter will have a code word to give back to the participant to ensure that the participant's speakers/headset are working and that they can hear the participant.  The participant needs to enter this code word into the oTree experiment window in order to progress with the experiment.  Once the participant has successfully done this, the participant can be moved back to the main room to wait for the rest of the participants.

> [!WARNING]
> TODO:
> - use the jitsi api to verify the camera and microphone is working, and only show the next button from the initial joining page once we can confirm that there is a functioning camera and microphone

# If a participant needs help or wants to ask a question

Particiants have a 'Raise Hand' button that creates an entry in the experimenter's ToDo list.  By default, participants do not have the ability to speak in the main videoconference room of the session.  If the participant has a question or needs help from the experimenter, they therefore either need to be moved into a breakout room to talk privately with them, or given permission to speak in the main room (not recommended). 

The experimenter interface has a dropdown menu to create a breakout room (if needed), and move the participant and extra experimenter view into the room. The experimenter's view of the main room will have their camera switched off and their microphone muted so as not to confuse the remaining participants as to why they can't hear the experimenter.  When the breakout room is closed, the camera and microphone should be muted in the extra view (see 'Caution' note below) and activated again in the main experimenter view. 

> [!Caution]
> Known issue: when a breakout room is closed, the automatic muting of the extra experimenter view of the video conference is not reliable.  You may need to manually mute the second window.


# If a participant is being disruptive

Experimenters have full moderator powers within the video conference.  This allows you to disable their camera, mute their microphone, or entirely kick them out of the video conference.

> [!Caution]
> Kicking a participant out will not prevent them from rejoining and causing further disruption. Only kick them out of the video conference as a last resort

> [!WARNING]
> TODO: Store a flag on a participant if they have been kicked out, and check it before having the participant's window connect to Jitsi.

# Breakout Rooms

If you need breakout rooms for groups within a session, you will have to manually create the rooms and assign participants to them via the jitsi interface.  Instructions on doing that can be in the [jitsi documentation](https://jitsi.support/how-to/jitsi-breakout-rooms/)
