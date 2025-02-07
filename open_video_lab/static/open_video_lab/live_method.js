var session_code = document.currentScript.dataset.session_code
var pcode = document.currentScript.dataset.participant_code

jQuery(document).ready(function(){

        if (window.parent.self == window.self){
        console.warn(`session code: ${session_code}`)

        var ws = new ReconnectingWebSocket(`ws://${window.location.host}/AdminReport/${session_code}`)


        function sessionWideLiveSend(data){
           ws.send(JSON.stringify({'data': data, 'participant_id': pcode}) )
        }

        function onMessage(data){
            let data_obj = JSON.parse(data['data'])
            console.log(data_obj)
            if (data_obj['data']['type'] == 'admin_lowered_hand')
                {
                    if (data_obj['data']['participant_code'] == pcode){
                         jQuery('#btn-request-exptr').html("Raise Hand &#9995;").removeClass("btn-success").addClass("btn-dark")
                    }

                }
            if (data_obj['data']['type'] == 'passed_checks')
                {
                    if (data_obj['data']['participant_code'] == pcode){
                        try{
                         jQuery('#connecting').remove()
                        }
                        catch(Exception){

                        }
                    }

                }

        }

        ws.onmessage = onMessage
            
        
        jQuery('#btn-request-exptr').on('click', function(){
            if ( jQuery('#btn-request-exptr').hasClass("btn-dark") || jQuery('#btn-request-exptr').hasClass("btn-warning")){
                 console.warn("sending lower hand request")
                 sessionWideLiveSend({"type": "raise_hand"})
                 jQuery('#btn-request-exptr').html("Lower Hand &#9995;").removeClass("btn-warning").removeClass("btn-dark").addClass("btn-success")
                }       
             else if ( jQuery('#btn-request-exptr').hasClass("btn-success")){
                 console.warn("sending lower hand request")
                 sessionWideLiveSend({"type": "lower_hand"})
                 jQuery('#btn-request-exptr').html("Raise Hand &#9995;").removeClass("btn-success").addClass("btn-dark")

            }
            else {
                sessionWideLiveSend("Button is in a broken state")
            }
                
        });

     }
});
