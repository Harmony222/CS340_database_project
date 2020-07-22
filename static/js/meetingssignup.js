// console.log("javascript connected");

function buttons() {
    let allrows = Array.from(document.querySelectorAll('#signUpMeetings tr'))
    // console.log('rows', rows)
    let buttons = Array.from(document.querySelectorAll('#signUpMeetings button'))
    // console.log('buttons', buttons)
    for (i = 0; i < buttons.length; i++) {
        let row = allrows[i];
        let button = buttons[i];
        // console.log('row_id', row_id, 'button', button);
        button.addEventListener('click', () => selectClick(allrows, row));
    };
    let signUpSubmit = document.getElementById('signUpSubmit')
    if (signUpSubmit) {
        signUpSubmit.addEventListener('click', () => signUpClick())
    };
};

function selectClick(allrows, row) {
    // console.log(row);
    for (let r of allrows) {
      r.classList.remove('table-primary');
    };
    row.setAttribute('class', 'table-primary');
    let meetingID = document.getElementById('meetingID');
    meetingID.value = row.firstElementChild.innerHTML;
};
    
function signUpClick() {
    let meetingID = document.getElementById('meetingID').value;
    let err = document.getElementById('selectMeetingError');
    if (!meetingID) {
        err.classList.remove('hidden');
    } else {
        console.log(meetingID);
        err.classList.add('hidden');
    };

};


document.addEventListener('DOMContentLoaded', buttons);