// Client ID and API key from the Developer Console
var CLIENT_ID = '522587700290-58jeu1o0g3atc3q5s0540m9tnnpagtul.apps.googleusercontent.com';
var API_KEY = 'AIzaSyBQEBnoO8QauNiqQXhUmGyHYs1MqE7h3OU';

setTimeout(function(){
  console.log("Google API has loaded.")
}, 2000);

// Array of API discovery doc URLs for APIs used by the quickstart
var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"];

// Authorization scopes required by the API; multiple scopes can be
// included, separated by spaces.
var SCOPES = "https://www.googleapis.com/auth/calendar.readonly";

var authorizeButton = document.getElementById('authorize_button');
var signoutButton = document.getElementById('signout_button');

/**
 *  On load, called to load the auth2 library and API client library.
 */
function handleClientLoad() {
    gapi.load('client:auth2', initClient);
  }
  
  /**
   *  Initializes the API client library and sets up sign-in state
   *  listeners.
   */
  function initClient() {
    gapi.client.init({
      apiKey: API_KEY,
      clientId: CLIENT_ID,
      discoveryDocs: DISCOVERY_DOCS,
      scope: SCOPES
    }).then(function () {
      // Listen for sign-in state changes.
      gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
  
      // Handle the initial sign-in state.
      updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
      authorizeButton.onclick = handleAuthClick;
      signoutButton.onclick = handleSignoutClick;
    }, function(error) {
      appendPre(JSON.stringify(error, null, 2));
    });
  }
  
  /**
   *  Called when the signed in status changes, to update the UI
   *  appropriately. After a sign-in, the API is called.
   */
  function updateSigninStatus(isSignedIn) {
    if (isSignedIn) {
      authorizeButton.style.display = 'none';
      signoutButton.style.display = 'block';
      $('.select-area').show();
      listUpcomingEvents();
    } else {
      authorizeButton.style.display = 'block';
      signoutButton.style.display = 'none';
      $('.select-area').hide();
      $('#select1 option').remove();
      $('#select1').append('<option value="-1">'+'</option>');
      $('#crntWork').hide();
    }
  }
  
  /**
   *  Sign in the user upon button click.
   */
  function handleAuthClick(event) {
    gapi.auth2.getAuthInstance().signIn();
  }
  
  /**
   *  Sign out the user upon button click.
   */
  function handleSignoutClick(event) {
    gapi.auth2.getAuthInstance().signOut();
  }
  
  /**
   * Append a pre element to the body containing the given message
   * as its text node. Used to display the results of the API call.
   *
   * @param {string} message Text to be placed in pre element.
   */
  function appendPre(message) {
    var pre = document.getElementById('content');
    var textContent = document.createTextNode(message + '\n');
    pre.appendChild(textContent);
  }
  
  /**
   * Print the summary and start datetime/date of the next ten events in
   * the authorized user's calendar. If no events are found an
   * appropriate message is printed.
   */
  function listUpcomingEvents() {
    gapi.client.calendar.events.list({
      'calendarId': 'primary',
      'timeMin': (new Date()).toISOString(),
      'showDeleted': false,
      'singleEvents': true,
      'maxResults': 10,
      'orderBy': 'startTime'
    }).then(function(response) {
      var events = response.result.items;
      var opt = 0;
      if (events.length > 0) {
        for (i = 0; i < events.length; i++) {
          
          var event = events[i];
          var when = event.start.dateTime;
          if (!when){
              when = event.start.date;
          }
          var now = new Date();
          if (when.substring(8,10) == String(now.getDate())){
            $("#select1").append('<option value="'+String(opt)+'">'+event.summary+'</option>');
            opt += 1;
          }
          
        }
      } else {
        console.log('No InComming')
      }
    });
  }

var min = 25;
var sec = 00;
var workTime = 1500;
var breakTime = 300;
var crntTime = 1500; // default: work
var stat = 0; // record the current status
var timeString;
var remainTom = 1;
var isMoreT = 0;
$('#cntBtn').click( btnClicked );

function btnClicked(){
    if ($('#select1 option:selected').val() != -1){
        $('.work-notification').text($('#select1 option:selected').text());
        $('.work-notification').show();
        if ($('#select2 option:selected').val() != 1){
            remainTom = parseInt($('#select2 option:selected').val());
            isMoreT = 1;
        }
    } 
    if ($('#select1 option:selected').val() == -1){
        $('.work-notification').text($('#select1 option:selected').text());
        $('.work-notification').hide();
    }
    
    if (stat == 0){
        $('#cntBtn').text('STOP');
        Timer();
        stat = 1;
    } else {
        $('#cntBtn').text('START');
        clearInterval(down);
        stat = 0;
    }
};

function calTime(){
    min = Math.floor(crntTime / 60);
    sec = crntTime % 60;
    if (sec < 10){
        return String(min) + ':' + String(0) + String(sec);
    } else {
        return String(min) + ':' + String(sec);
    }
}

var down;
function Timer(){
    down = setInterval(CountDown, 1000);
        function CountDown(){
            crntTime -= 1;
            timeString = calTime();
            $('#timer').text(timeString);
            if (crntTime == 0){
                notify();
                if (isMoreT == 1 && remainTom > 1){
                    remainTom -= 1;
                    Timer();
                }
                else if (isMoreT == 1 && remainTom == 1) {
                    Timer();
                    isMoreT = 0;
                }
                clearInterval(down);
            }
        }
    
}

$('#workbtn').click(function(){
    crntTime = 1500;
    timeString = calTime();
    $('#timer').text(timeString);
});
$('#breakbtn').click(function(){
    crntTime = 300;
    timeString = calTime();
    $('#timer').text(timeString);
});

function notify(){
  var step = 0;
  var timer = setInterval( function() {
    if (step%2 == 1) {document.title('Times Up!')};
    if (step%2 == 0) {document.title('')};
    if (step == 5){
      clearInterval(timer);
      document.title('Pomodoro Online');
    }
  }
  ,1000);

};