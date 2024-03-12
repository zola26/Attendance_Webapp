$(document).ready(function () {
  function updateDetectedPersonImage() {
      $.ajax({
          url: updateDetectedPersonImageUrl,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
              if (data && data.image_url) {
                  $('#person-image').attr('src', data.image_url);
                  $('#person-name').text('' + data.name);
                  
                  // $('#detection-status').text(data.attendance_status);
                  console.log(data.attendance_status)
                  if (data.attendance_status) {
                      $('#detection-status').text('successfully Marked.');
                      $('#detection-icon').attr('class', 'bx bx-message-rounded-check');
                      // document.getElementById('successSound').play();
                  } else {
                      $('#detection-status').text('Already Marked.');
                      $('#detection-icon').attr('class', 'bx bx-message-rounded-x');
                      // document.getElementById('alreadyDetectedSound').play();
                  }
              }
          },
          error: function (error) {
              console.error('Error updating detected person image:', error);
          }
      });
  }

// Start periodic updates immediately
setInterval(updateDetectedPersonImage, 1000);
});
function displayTime(){
  var d = new Date();
  var hour = d.getHours(); // 0-23
  var min = d.getMinutes(); // 0-59
  var sec = d.getSeconds(); // 0-59
  var amOrPm = "AM";
  if(hour >= 12)
  {
    amOrPm = "PM";
  }
  if(hour > 12)
  {
    hour = hour - 12;
  }
  if(hour < 10)
    hour = "0" + hour;
  if(min < 10)
    min = "0" + min;
  if(sec < 10)
    sec = "0" + sec;
  document.getElementById("clock").innerHTML = hour + ":" + min + ":" + sec + " " + amOrPm;
}
setInterval(displayTime, 1000);