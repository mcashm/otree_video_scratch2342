
const script_ele = document.currentScript;

const magic_cookie = script_ele.dataset.magic_cookie;
const session_ovl_room_link = script_ele.dataset.session_ovl_room_link;
const main_room_jwt = script_ele.dataset.main_room_jwt;
const private_room_jwt = script_ele.dataset.private_room_jwt;
const popup_url = script_ele.dataset.popup_url;
const session_code = script_ele.dataset.session_code;

//let main_conference_window;
//let private_conference_window;

function startPrivateConference(participant_code){

        if (participant_code == "none"){
            return
        }


        create_extramenter(participant_code)

        let data = { 
                    "type": "startPrivateConference",
                    "participantCode": participant_code
                    }

        console.warn("Private Conferece dropdown change event fired")

        main_conference_window.postMessage(data, window.location.origin)
}



jQuery(document).ready(function(){

    jQuery('#btnInit').on('click', function(){

        console.debug("btnInit click event fired")

        window.main_conference_window = window.open( popup_url, 
                                                 "MainConferenceWindow",
                                                 "width=800,height=600,resizable,scrollbars=yes,status=1")

        main_conference_window.addEventListener('load', function()
        { 

        let data = { 
                    "type": "init",
                    "magic_cookie": magic_cookie,
                    "room" : session_ovl_room_link,
                    "jwt" : main_room_jwt,
                    "is_main_room": true
                    }

            main_conference_window.postMessage(data, window.location.origin)


        } )





    });

    jQuery('#manual-breakout-room-btn').on('click', function(e){

        let participant_code = jQuery('#private-room-selector :selected').data("participant_code");
        startPrivateConference(participant_code)

    })

    jQuery('#content').on('click','.create_breakout', function(e){

         console.warn("click fired with current target:")
        console.warn(e.currentTarget)

         let participant_code = e.currentTarget.dataset.participant_code
         startPrivateConference(participant_code)

    })


    window.addEventListener('message', function(e){

    console.warn("some message received")
    console.warn(e)

    if (e.data.type == "privateConferenceInitialised"){

        console.warn("privateConferenceInitialised message relayed")
        //retransmit to the private conference
        private_conference_window.postMessage(e.data, window.location.origin)

    } 

    if (e.data.type == "query_new_ppt"){

        ovl_ws.send(JSON.stringify({"participant_id": "admin", "data": e.data}))
        console.warn("query_new_participant message relayed to websocket")
        //retransmit to the private conference
    } 


    }, false);


})


function create_extramenter(target_participant="none"){

        window.private_conference_window = window.open( popup_url, 
                                                 "PrivateConferenceWindow",
                                                 "width=420,height=360,left=1000,resizable,scrollbars=yes,status=1")

        private_conference_window.addEventListener('load', function()
        { 
         let data = { 
                    "type": "init",
                    "magic_cookie": magic_cookie,
                    "room" : session_ovl_room_link,
                    "jwt" : private_room_jwt,
                    "is_main_room": false,
                    "target_participant": target_participant,
                    }

            private_conference_window.postMessage(data, window.location.origin) 
        })

}
