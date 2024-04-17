// Prevent the HTML form from storing state from the previous sessions
// If you refresh the /result page after a successful form submission
// The form will be empty, instead of trying to re-submit
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }
  
  