console.log("javascript connected");




function selectButtons() {
    let rows = Array.from(document.querySelectorAll('#signUpMeetings tr'))
    // console.log('rows', rows)
    let buttons = Array.from(document.querySelectorAll('#signUpMeetings button'))
    // console.log('buttons', buttons)
    for (i = 0; i < buttons.length; i++) {
        let row = rows[i];
        let button = buttons[i];
        // console.log('row_id', row_id, 'button', button);
        button.addEventListener('click', () => selectClick(row));
    };
};

function selectClick(row) {
    // console.log(row);
    row.setAttribute('class', 'table-primary');
    meetingID = document.getElementById('meetingID');
    meetingID.value = row.firstElementChild.innerHTML;
};
    

document.addEventListener('DOMContentLoaded', selectButtons);




// https://getbootstrap.com/docs/4.0/components/forms/#validation
(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

