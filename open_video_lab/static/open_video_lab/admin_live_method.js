
jQuery(document).ready(function(){
//  if (window.top.self != window.self){
    console.warn("the script is running") 
    window.ovl_ws = new ReconnectingWebSocket(`ws://${window.location.host}${window.location.pathname}`)
    function onMessage(event){
        let data = JSON.parse(event.data)
        console.info("received data on websocket")
        console.info(data)

        let participant_code = data.data.participant_id //crypto.randomUUID();

        if (participant_code == "admin" || data.participant_code == "admin"){


            if (data.data.type == "query_new_ppt_response"){
                console.warn("posting query_new_ppt_response to main_conference_window")
                main_conference_window.postMessage(data.data)
            }

            console.info("participant_code == admin - returning")
            return
        }
        else 
        {
            console.info(`participant_code == ${participant_code} - continuing`)
        }

        if (data.type == "lower_hand"){

            console.warn(`attempting to remove .raised-hand[data-participant-id="${participant_code}"]`)


            jQuery(`.raised-hand[data-participant-id="${participant_code}"]`).remove()

            
         }

        
        if (data.type == "new_todo"){

                let item = JSON.parse(data.data) 
                console.log(item)
                if (item.todo_type == "raised_hand"){
                    let html = `<div class="accordion-item raised-hand" data-participant-id="${item._participant_code}">
                        <h2 class="accordion-header" id="todo-${item.id}">
                          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-todo-${item.id}" aria-expanded="true" aria-controls="collapase-todo-${item.id}">
                           P${item._participant_code} - ${item.title}
                          </button>
                        </h2>

                       <div id="collapse-todo-${item.id}" class="accordion-collapse collapse" aria-labelledby="todo-${item.id}" data-bs-parent="#to-do-list">
                           <div class="accordion-body">         
                                ${item.content}
                              <button class="todo-done-button btn btn-success float-end" type="button" data-todo_id=${item.id} data-participant_code="${item._participant_code}">Done</button>
                           </div>
                       </div>
                    </div>`

                jQuery('#to-do-list').append(html)
                }


                if (item.todo_type == "code_exchange"){
                    let html = `<div class="accordion-item code-exchange" data-participant-id="${item._participant_code}">
                        <h2 class="accordion-header" id="todo-${item.id}">
                          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-todo-${item.id}" aria-expanded="true" aria-controls="collapase-todo-${item.id}">
                           P${item._participant_code} - ${item.title}
                          </button>
                        </h2>

                       <div id="collapse-todo-${item.id}" class="accordion-collapse collapse" aria-labelledby="todo-${item.id}" data-bs-parent="#to-do-list">
                           <div class="accordion-body">         
                                ${item.content}
                              <button class="todo-done-button btn btn-success" type="button" data-todo_id=${item.id} data-participant_code="${item._participant_code}">Done</button>
                           </div>
                       </div>
                    </div>`

                jQuery('#to-do-list').append(html)
 
                }


            }

         }

        ovl_ws.onmessage = onMessage


        jQuery('body').on('click', '.todo-done-button', function(e){


            let jQele = jQuery(this)
            let todo_id = jQele.data('todo_id');
            let participant_code = jQele.data('participant_code');

           jQele.closest(".accordion-item").remove()

            ovl_ws.send(JSON.stringify({"data": {"type": "todo_done", "id": todo_id}, "participant_code": "admin"}))
            if (jQele.data.lower_hand){
                ovl_ws.send(JSON.stringify({"data": {"type": "admin_lowered_hand", "participant_code": participant_code}, "participant_code": "admin"}))
            }

        });


//  }
});
