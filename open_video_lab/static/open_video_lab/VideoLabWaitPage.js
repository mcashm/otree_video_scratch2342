    const socket_url = document.currentScript.dataset.socket_url;
    const gbat_is_defined = document.currentScript.dataset.gbat_is_defined;
    const group_by_arrival_time = document.currentScript.dataset.gbat;

$(document).ready(function () {


    if (window.self == window.parent.self) {
        return
    }

    console.log(document.currentScript)
    console.log(socket_url)

    var socket;

    initWebSocket();

    function initWebSocket() {
        console.log("initWebSocket called");
        socket = makeReconnectingWebSocket(socket_url);
        socket.onmessage = function(e) {
            var data = JSON.parse(e.data);

            // Handle errors
            if (data.error) {
                // maybe the div's default text doesn't get shown
                $("#_otree-server-error").text(data.error);
                $("#_otree-server-error").show();
                return;
            }

            window.self.location.reload();

            console.log("websocket message received.  The iframe should be reloading");
        };
    }

    if (gbat_is_defined && group_by_arrival_time){

        /*
        Refresh the whole page. This is documented behavior that enables things like
        allowing people to proceed if they have been waiting too long.
        We also make it random to prevent load times from syncing up
        due to reload mechanisms. This will ensure that the page gets
        reloaded regularly, which is useful e.g. for intergenerational
        games.
        */

        var RELOAD_PARAM = "?reload=1";

        var SECOND = 1000;
        // the randomness is useful so that when there are many players,
        // the GBAT page loads get spaced apart. I think this helps wait pages
        // finish quicker, and may prevent some other bugs.
        window.setInterval(function () {
          window.self.location.href = window.self.location.pathname + RELOAD_PARAM;
        }, (10 + Math.random() * 60) * SECOND);

        function setTabHiddenStatus(isHidden) {
          socket.send(JSON.stringify({
            'tab_hidden': isHidden
          }));
          var titleText = document.getElementById('_otree-title').textContent;
          var newIcon = isHidden ? '🟡' : '🟢';
          document.querySelector('title').textContent = newIcon + ' ' + titleText;
        }

        document.addEventListener("visibilitychange", event => {

          // {# if the user tabs in, we mark the tab active.
          // but not vice versa, since then it would be impossible for
          // someone to test a multiplayer game on a single PC #}
          if (!document.hidden)
            setTabHiddenStatus(false);
        })

        // for first page load, we don't consider unfocused tabs to be abandoned.
        // that way, browser bots and manual testing etc still work.
        function sendTabHiddenStatusInitial() {
          // {# better to use hidden rather than hasFocus()
          // because it's OK if the user has a split window with another window
          // focused. that should not be considered getting distracted.
          // hasFocus is too strict. even if you are in the page's JS console it considers you unfocused #}
          let gotDistracted = window.self.location.search.includes(RELOAD_PARAM) && document.hidden;
          setTabHiddenStatus(gotDistracted);
        }

        sendTabHiddenStatusInitial();
    }



 });

