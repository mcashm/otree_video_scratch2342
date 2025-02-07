
    /* 
    SECTION: AVOID TEMPLATING SYNTAX
    allow for variable passing into here from a template while being
    able to serve the script as a static file.*/

    const script_ele = document.currentScript;

    let participant_code = script_ele.dataset.participant_code
    let jwt_token = script_ele.dataset.jwt_token
    let content_container = script_ele.dataset.content_container
    let room_name = script_ele.dataset.room_name
    let pin_experimenter_interval;
    let main_experimenter_id;

    console.log("room_name:")
    console.log(room_name)


    /*
    END SECTION: AVOID TEMPLATING SYNTAX
    */
  
    const initIframeAPI = () => {
      const domain = "8x8.vc"
      const options = {
        roomName: room_name,
        jwt: jwt_token,
        parentNode: document.querySelector('#meet'),
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

          startWithAudioMuted: true,
          prejoinPageEnabled: false,
            lobby: {
              autoKnock: true,
              enableChat: false
            },
              
            securityUi: {
              hideLobbyButton: true,
              disableLobbyPassword: true,
            },
              
            disableTileView: false,

            disableAddingBackgroundImages: true,

            readOnlyName: true,

            disableRemoteMute: true,

            disableModeratorIndicator: true,

            remoteVideoMenu: {
              disabled: true,
              disableDemote: true,
              disableKick: true,
              disableGrantModerator: true,
              disablePrivateChat: true,
            },
            participantMenuButtonsWithNotifyClick: ['pinToStage'],

            redirectURI: 'https://8x8.vc/static/oauth.html',

            disabledSounds: [
                'RECORDING_OFF_SOUND',
                'RECORDING_ON_SOUND',
            ],

            recordingService: {
              sharingEnabled: false,
            },
            /*
            recordings: {
                recordAudioAndVideo: true,
                suggestRecording: false,
                showPrejoinWarning: false
            },
            */

            toolbarButtons: [
              'camera',
              'toggle-camera',
              'microphone',
              'chat',
            ],

            //hideRecordingLabel: true,

            disabledNotifications: [
              //'notify.moderator',
              //'dialog.recording',
              //'notify.localRecordingStarted', // shown when the local recording has been started
              //'notify.localRecordingStopped',
              //'recording.linkAvailable',
              //'recording.linkGenerated',
              //'recording.inProgress',
            ],
        },
      };

      
      window.jaas_api = new JitsiMeetExternalAPI(domain, options);
         jaas_api.addListener('participantJoined', function(e)
            {
                if (e.displayName == "Experimenter")
                {
                    main_experimenter_id = e.id
                    jaas_api.executeCommand('setLargeVideoParticipant', e.id) 
                    jaas_api.pinParticipant(e.id)
                }

        });
       


        /*jaas_api.addListener('largeVideoChanged', function(e)
            {
                console.log("new listener e:")
                console.log(e)
                if (main_experimenter_id){
                    if (e.id != main_experimenter_id)
                    {
                        jaas_api.executeCommand('setLargeVideoParticipant', main_experimenter_id) 
                        jaas_api.pinParticipant(e.id)
                    }
                }

        });*/

        jaas_api.addListener('videoConferenceJoined', function(e){
            console.log("videoConferenceJoined event fired with data:")
            if (jQuery('#checks_passed').val() == "1" /* because apparently the ORM in otree 5 doesn't really keep booleans. Thanks for documenting that, Chris. */){
                jQuery('#connecting').remove()   
            }
            else if (e.breakoutRoom){

                jQuery('#connecting').remove()   
            }
        });

    }
  
   window.onload = () => {
     if (window.self == window.parent.self) {

          jQuery('.otree-wait-page').first().remove(); 
          jQuery('.otree-body').remove(); 
          jQuery('#btn-request-exptr').removeClass("d-none"); 
          jQuery('#meet').removeClass("d-none"); 
          jQuery('#connecting').removeClass("d-none");
          initIframeAPI();
     }
      else
    {

        jQuery('#meet').remove(); 
        jQuery('#connecting').remove(); 
        jQuery('#experiment_container').remove(); 
        jQuery('#btn-request-exptr').remove(); 

    }

  }


