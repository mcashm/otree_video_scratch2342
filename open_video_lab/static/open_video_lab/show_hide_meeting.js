console.log("OVL show_hide_meeting script running")

    console.log("OVL inside if window.self != window.parent.self")
    /* 
    SECTION: AVOID TEMPLATING SYNTAX
    allow for variable passing into here from a template while being
    able to serve the script as a static file.*/


    const app_name = document.currentScript.dataset.app_name
    const page_name = document.currentScript.dataset.page_name
     /*
    END SECTION: AVOID TEMPLATING SYNTAX
    */
    let blurred_json = document.currentScript.dataset.blurred_pages.replaceAll("'",'"')
    const blurred_pages = JSON.parse(blurred_json)

//    jQuery(document).on('ready', function(){
//        console.log("OVL inside the onready")

    var url_to_match = `${app_name}/${page_name}`

    var show_hide_meeting = "show"

    console.log(`OVL url to match: ${url_to_match}`)

    if (blurred_pages.includes(url_to_match))
    {
        show_hide_meeting = "hide"
        console.log("OVL url matches - hiding")
    }
    else
    {
        show_hide_meeting = "show"
        console.log("OVL url does-not match - unhiding")
    }

    
    data = {"message_source": "experiment_container",
            "action": show_hide_meeting == "hide" ? "blur_meeting" : "show_meeting"
             }
    if (window.self != window.parent.self){
        window.top.postMessage(JSON.stringify(data))
        console.log("OVL pasting message to window.top with data: ")
        console.log(data)
    }
    else
    {
        if (show_hide_meeting == "hide"){
            blur_meeting()
        }
        else
        { unblur_meeting()}
    }

    /*
    if (window.self != window.parent.self){

        console.warn("running code from show_hide_meeting.js")

        let show_hide_meeting = "show"

        if (show_hide_meeting_script_ele.dataset.hasOwnProperty("ovl_show_hide_meeting"))
        {
            show_hide_meeting = show_hide_meeting_script_ele.dataset.ovl_show_hide_meeting;
        }

        console.warn(`show_hide_meeting=${show_hide_meeting}`)

        data = {"message_source": "experiment_container",
                "action": show_hide_meeting == "hide" ? "blur_meeting" : "show_meeting"
                 }
        window.top.postMessage(JSON.stringify(data))
    }

    */
//    })
//}
