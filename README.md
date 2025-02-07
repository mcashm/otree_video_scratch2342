# About

This app is an extension for oTree that integrates video-conferencing into oTree sessions. This brings
benefits to conducting behavioural experiments online, allowing experimenters to:
- have confidence that participants are real individuals and are not bots
- improve participant belief that they are interacting with other real participants
- interact with participants in real time, answering any questions they may have about
the experiment or its instructions
- ensure common knowledge by reading instructions live, as is standard practice in an
experimental laboratory
- run synchronous interactive experiments such as normal form economic games, 
where participant decisions and/or outcomes rely on prompt input from other participants
- monitor engagement with the experiment, ensuring that participants do not get distracted by their
surroundings leading to delays and/or poor quality data

It currently only supports video conferening using Jitsi as a service (JAAS), as provided by 8x8.com. 
To use this extension, you will need your own account with 8x8. See [the 8x8 JAAS website](https://jaas.8x8.vc/) 
for details and pricing.

# Features

- **Window-in-window video laboratory**.  The video conference for participants is displayed in the same
browser tab as the normal participant view of an experiment.
- **Experimenter View**. Integrated into the admin view of an oTree session as an 'admin report'. The
video conference window itself launches as a pop-up window, allowing the experimenter to use other
sections of the session admin interface without leaving the video conference.
- **Additional experimenter view for private conversations**.  If an experimenter needs to talk privately
to a participant, there is a separate window for that so they do not disturb the rest of the participants
- **Integrated checking of camera and video**. (Requires manual experimenter intervention).  A code exchange process
where participants are given a randomised code word to give to the experimenter to prove their microphone is properly
functioning, and the experimenter gives them a different code word to type in in order to progress in order to 
guarantee speakers/headphones are working and set to a reasonable volume.
- **Video Chat Moderation Tools**. Full moderation tools of the video chat platform are available to experimenters,
allowing them to assign and remove speaking rights, turn off participants' cameras, or kick disruptive participants
out of the video lab.
- **Breakout rooms**.  (Requires manual experimenter intervention).  The video conference platform's breakout rooms
functionality is available, allowing experimenters to assign participants into groups that may communicate with 
each other for experiments requiring live communication.

# Documentation

For instructions on how to install the software, modify your oTree experiment in order to use it, and run a session
including a video lab, see the [Documentation](open_video_lab/docs/).



# Credits

Conceptualisation and design by Ty Hayes, Matthew Cashman, Sean Enderby, Andrea Isoni

Code by Ty Hayes, Matthew Cashman


# License 

This software is offered under a modified MIT license, that imposes the additional obligation of citing the following
article in all publications in which results of experiments conducted with the software are published:

[To follow]

