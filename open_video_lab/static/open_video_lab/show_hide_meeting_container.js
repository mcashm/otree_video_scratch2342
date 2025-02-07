/*

    Methods to show or hide the meeting, based on settings from within page vars_for_template

    When hiding the meeting, 

    Requires show_hide_meeting.css to be loaded on the page

*/

const MEETING_IFRAME = document.querySelector('div#meet');
const BLURRED_CLASS = "blurred";
const INTERVAL_PERIOD = 200;

var running_interval;


function clear_old_interval(){

    if (running_interval == undefined){ return }

    clearInterval(running_interval)
    running_interval = undefined;
    }

var blur_meeting = function(){
        clear_old_interval()

        running_interval = window.setInterval( function(){ 
                                                MEETING_IFRAME.classList.add(BLURRED_CLASS)
                                                }, INTERVAL_PERIOD)
        }

var unblur_meeting = function(){
        clear_old_interval()

        running_interval = window.setInterval( function(){ 
                                                MEETING_IFRAME.classList.remove(BLURRED_CLASS)
                                                }, INTERVAL_PERIOD)
        }

 if (window.self == window.parent.self) {

       
    window.addEventListener('message', function(e) {
        let data

            try {
                data = JSON.parse(e.data);
            }
            catch (SyntaxError){
                //console.log("message not in json form - not for us, but could well be from jitsi.  Continue")
                console.warn(`message not json: ${e.data}`)
                return
            }

            if (data.hasOwnProperty("postis")){
                //message is from jitsi. we can ignore it
                return
            }
                console.warn(e.data)

            if (!data.hasOwnProperty("message_source")){
                //untrusted content - stop!
                //console.log("Received unexpected (malformed) message to window object.  Not processing further")
                return
            }


            if (data.message_source == "experiment_container"){
                if (data.action == "blur_meeting"){
                 blur_meeting()
                }
                if (data.action == "show_meeting"){
                    unblur_meeting()
            }
        }
    })
}
