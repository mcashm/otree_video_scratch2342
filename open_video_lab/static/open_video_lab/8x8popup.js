
let api;
let main_room;
let extramenter;
let joined_participants = new Set();
let room_created_callback_is_set = false;
let main_window_audio_mute_state;
let main_window_video_mute_state;

window.addEventListener("message", (e) => { if (e.origin == "https://8x8.vc"){return;}; console.warn("message received via postMessage:"); console.warn(e)}, false)


function getMainExperimenterParticipantId(){

    //WARNING: UNDOCUMENTED INTERNALS   
    return api._myUserID

    //getRoomsInfo
    //then iterate over rooms 
    // iterate over ppts in room
    // if username matches Experimenter Username, save that participant ID into
    //experimenter_participant_id
    api.getRoomsInfo().then(rooms => {
        roomLoop:
        for (let room in rooms){
            for (let p in rooms[room].participants){
              if (rooms[room].participants[p].displayName == "Experimenter")
                {
                   // experimenter_participant_id = p
                    api.executeCommand('setLargeVideoParticipant', p) 
                    break roomLoop
                }
            }
        }
    })
}

function pinMainExperimenter(){
        if (!api._myUserID){
           return setTimeout(pinMainExperimenter, 500)
        }
        console.log("Pinning Main Experimenter:")
        console.log(api._myUserID)
        //api.pinParticipant(api._myUserID) // this one only affects local meeting
        api.executeCommand('setLargeVideoParticipant', api._myUserID) //FFS JITSI - This one also seems to only affect the local meeting.  How do we make sure people are actually watching the meeting host when they're supposed to be?!
        

    /*
    api.getRoomsInfo().then(rooms => {
        roomLoop:
        for (let room in rooms){
            participantLoop:
            for (let p in rooms[room].participants){
              if (rooms[room].participants[p].displayName == "Experimenter")
                {
                    experimenter_participant_id = p
                    console.warn(`found experimenter id: ${p} - pinning that participant`)
                    api.pinParticipant(experimenter_participant_id)
                    break roomLoop;
                }
            }
        }

        if (experimenter_participant_id){
            console.log("found main experimenter. they should be pinned")
        }
        else {
            console.log("didn't find main experimenter in rooms:")
            console.log(rooms)
        }
    
 

    })
    */
}

function initMessageCallback(event) 
{
    if (event.origin == "https://8x8.vc"){return;}; //message from jitsi. ignore

    if (event.data.type != "init") {
        return
    }

    console.log("initMessageCallback event.data:")
    console.log(event.data)

    init(event.data.magic_cookie,
        event.data.room,
        event.data.jwt,
        event.data.is_main_room,
        event.data.target_participant ?? "none"
        )

    window.removeEventListener("message", initMessageCallback)
    console.log("conference init message received")
}

window.addEventListener("message",
                        initMessageCallback,
                        false
                        )


function queryNewParticipantCallback(event){
    if (event.origin == "https://8x8.vc"){return;}; //message from jitsi. ignore
    if (event.data.type != "query_new_ppt_response"){
        return
    }
    if (event.data.checks_completed){
       joined_participants.add(event.data.participant_id)
    }
    else
    {
        console.warn(`running startPrivateConference(${event.data.participant_id}, false)`)
        startPrivateConference(event.data.participant_id, false)
    }

 }

window.addEventListener("message",
                        queryNewParticipantCallback,
                        false
                        )
function messageStartPrivateConferenceCallback(event){
    if (event.origin == "https://8x8.vc"){return;}; //message from jitsi. ignore
    if (event.data.type != "startPrivateConference")
    {
        return
    }

    startPrivateConference(event.data.participantCode, true)
    
    console.warn("startPrivateConferenceMessage reached window")
}

window.addEventListener("message",
                        messageStartPrivateConferenceCallback,
                        false
                        )

function connectToJitsi(room, target_id, jwt, width, height){
   console.log(room)

    let api = new JitsiMeetExternalAPI("8x8.vc", {
      roomName: room,
      parentNode: document.querySelector(target_id),
      jwt: jwt,
      width: width,
      height: height,    
      configOverwrite: {
        constraints: {
            video: {
                height: {
                   ideal: 180,
                   max: 180,
                   min: 180,
                    },
            },
          },
	  resolution: 180,
	  maxFullResolutionParticipants: 1,
          prejoinPageEnabled: false,
          startWithAudioMuted: true,
          lobby: {
              autoKnock: true,
              enableChat: false
            }
           }              
      })



    window.setTimeout(function(){
                api.executeCommand('setVideoQuality',180)
				console.info("setting video quality to 180")
                api.executeCommand('toggleModeration', true, "audio")
				console.info("setting audio moderation")
                
    				}, 20*1000)
    return api
  }

function init(magic_cookie, room, jwt, is_main_room, target_participant="none")
{
    var script = document.createElement('script');
    script.onload = function () {
        api = init_callback(room, jwt, is_main_room, target_participant)
        console.log(`init -> script.onload api: ${api}`)
    };
    script.src = `https://8x8.vc/${magic_cookie}/external_api.js`;

    document.head.appendChild(script);

    main_room = is_main_room

    if (!is_main_room){
        var close_button = document.createElement("button"); //works with any HTML5 element
        close_button.type = "button"
        close_button.id = "btn-close-private-chat"
        close_button.classList.add("btn")
        close_button.classList.add("btn-danger")
        close_button.classList.add("d-none")
        close_button.innerText = "Close Private Room" //Make sure to add button text if you don't want an empty button!!
        document.querySelector("#button-container").appendChild(close_button);    
    }
}

function init_callback(room, jwt, is_main_room, target_participant="none"){

    api = connectToJitsi(room,'#jaas-container', jwt, "90%", "90vh")

    console.log(`init_callback api:`)
    console.log(api)
    pinMainExperimenter()
    console.warn(`init callback running: is_main_room: ${is_main_room}, target_participant: ${target_participant}`)
    if (!is_main_room){
       console.log(`target_participant: ${target_participant}, adding roomCreatedCallback`)
        if (target_participant != "none"){
            startPrivateConference(target_participant, true)
       //     api.listBreakoutRooms().then( rooms => { roomCreatedCallback(rooms, target_participant) } ) 
        }
        return api
    }

    api.addListener('participantJoined', function(e)
        {

            if ( joined_participants.has(e.id) )
            {
                return
            }
            if (e.displayName == "Extramenter")
            {
                //TODO:  If the experimenter has muted themself
                // manually in the main conference, we should respect
                // that.  So we probably need to track that manually
                unmuteThisConference()
                return
            }

        let participant_code = e.displayName.split(" ")[1]
        window.opener.postMessage({"type": "query_new_ppt", "participant_id": participant_code})
    });


   return api
}


function passRoomInfoToPrivateChatWindow(room_id, ppt_id){


   console.warn("privateConferenceInitialised")
    let data = {
                "type": "privateConferenceInitialised",
                "room_id": room_id,
                "ppt_id": ppt_id,

                }

    console.warn("privateConferenceInitialised message sent to admin console")
    window.opener.postMessage(data, window.location.origin)
}


function startPrivateConference(participant_code, move_extramenter){

    
    let target_room = undefined;
    let target_ppt = undefined;


    api.listBreakoutRooms().then( rooms => {
        roomCreatedCallback(rooms, participant_code, move_extramenter )} 

    ) 

}

function roomCreatedCallback(response, participant_code, move_extramenter){

        let rooms;
        let target_room;
        let target_ppt;
        let skip_ppt_move = false;
        let extramenter_id;

        console.log(`running roomCreatedCallback(${response}, ${participant_code}, ${move_extramenter}`)

        // because why would the api have the "breakoutRoomsChanged" event
        // provide a list in the same format at the "listBreakoutRooms" function?
        if (response.hasOwnProperty("rooms")){
            rooms = response.rooms
        }
        else
        {
            rooms = response
        }

        for (let room in rooms){
            console.log(rooms)
            if (rooms[room].name == `Participant ${participant_code}`){
                target_room = room
            }
            if (Object.keys(rooms[room].participants).length == 0)
            {
                continue
            }
            for (let p in rooms[room].participants){
              if (rooms[room].participants[p].displayName == `Participant ${participant_code}`)
                {
                    target_ppt = p
                    if (room == target_room)
                        {
                        skip_ppt_move = true;
                        }
                }
              if (rooms[room].participants[p].displayName == "Extramenter")
                {
                    extramenter_id = p
                }
            }
            if (target_room && target_ppt && extramenter_id) 
            {
                break
            }
            else
            {
                if (!target_room){
                   console.warn("no target_room")
                }
                if (!target_ppt){
                   console.warn("no target_ppt")
                }
            }
        }


        if (target_room && target_ppt){
           console.warn("target_ppt and target_room both exist")

            function roomExistsCallback(){ 

                console.warn(`move_extramenter = ${move_extramenter}`)
                console.warn(`extramenter_id = ${extramenter_id}`)

                if (target_room){

                    api.removeListener('breakoutRoomsUpdated', roomCreatedCallback)
                    if(target_ppt){
                        if (!skip_ppt_move){
                            api.executeCommand('sendParticipantToRoom', target_ppt, target_room)
                        }
                        if (move_extramenter){
                            api.executeCommand('sendParticipantToRoom', extramenter_id, target_room)
                        }

                        passRoomInfoToPrivateChatWindow(target_room, target_ppt)

                        if (main_room){
                            muteThisConference()
                            } 

                    }

                }
            }

            roomExistsCallback()

        }
        else
        {

            //api.addListener('breakoutRoomsUpdated', function(e) { roomCreatedCallback(e, participant_code, move_extramenter) });
            //TODO:  UNDOCUMENTED API, or rather api hinted at insofar as Jitsi implements EventEmitter API
            api.once('breakoutRoomsUpdated', function(e) { roomCreatedCallback(e, participant_code, move_extramenter) });
            if (target_room == undefined){
                api.executeCommand('addBreakoutRoom', `Participant ${participant_code}`)
            }

        }
}





function muteThisConference(){
            console.warn("muting this window")
            api.isAudioMuted().then( (muted) => {
                   main_window_audio_mute_state = muted;
                   if(!muted){ 
                    api.executeCommand('toggleAudio');
                   }
                })

            api.isVideoMuted().then( (muted) => { 
                   main_window_video_mute_state = muted;
                   if(!muted){ 
                    api.executeCommand('toggleVideo');
                   }
        })
        }

function unmuteThisConference(){
            console.warn("unmuting this window")
            api.isAudioMuted().then( (muted) => {
                   if(muted != main_window_audio_mute_state){ 
                    api.executeCommand('toggleAudio');
                   }
                })

            api.isVideoMuted().then( (muted) => { 
                   if(muted != main_window_video_mute_state){ 
                    api.executeCommand('toggleVideo');
                   }
        })
}

function privateConferenceInitialisedCallback(event) 
{
    if (event.data.type != "privateConferenceInitialised") {
        return
    }

    if (main_room){
        //this callback should only be running in the private rooms window
        return
    }


    console.log("privateConferenceIniialisedCallback happening")

    let target_room = event.data.room_id

    //unmuteThisConference()

    jQuery('#btn-close-private-chat').removeClass('d-none')

    function closePrivateRoom(){
            muteThisConference()

            api.executeCommand('closeBreakoutRoom', target_room);
            //jQuery('#private-conference-container').addClass('hide-private-chat')
            jQuery('#private-room-selector-container').removeClass('d-none')
            jQuery('#btn-close-private-chat').addClass('d-none')
            jQuery('#btn-close-private-chat').off('click', closePrivateRoom)
            
        }

    jQuery('#btn-close-private-chat').on('click', closePrivateRoom)

}

window.addEventListener("message",
                        privateConferenceInitialisedCallback,
                        false
                        )

