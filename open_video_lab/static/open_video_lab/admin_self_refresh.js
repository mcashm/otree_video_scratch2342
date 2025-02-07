window.onload = () => {
     if (window.self == window.parent.self) {

          jQuery('#content').first().remove(); 
          jQuery('#self-refreshing-content-container').attr('src', self.location)
     }
      else
    {

        jQuery('#self-refreshing-content-container').remove(); 
        let content = jQuery('#content').detach()
        let wsscript = jQuery('#reconnecting-websocket-script').detach()
        let script = jQuery('#admin-live-script').detach()
        jQuery('body').empty().css("width: 90%")
        jQuery('body').append(content)
        jQuery('body').append(wsscript)
        jQuery('body').append(script)
        window.setInterval(function(){ 

            jQuery('#content').load(`${window.location} #content`);

        }, 15 * 1000)

    }
}
