console.log("javascript connected");
const baseURL = 'http://localhost:5000';

function selectButtons() {
    let allrows = Array.from(document.querySelectorAll('#attendeeMeetings tr'))
    // console.log('rows', rows)
    let buttons = Array.from(document.querySelectorAll('#attendeeMeetings button'))
    // console.log('buttons', buttons)
    for (i = 0; i < buttons.length; i++) {
        let row = allrows[i];
        let button = buttons[i];
        // console.log('row_id', row_id, 'button', button);
        button.addEventListener('click', () => get_attendees(allrows, row));
        // button.addEventListener('click', () => selectClick(allrows, row));
    };
};

function selectClick(allrows, row) {
    // console.log(row);
    for (let r of allrows) {
      r.classList.remove('table-primary');
    };
    row.setAttribute('class', 'table-primary');
    let tableDiv = document.getElementById('attendeeTable');
    tableDiv.setAttribute('class', 'hidden');
    console.log(tableDiv);
    let noDiv = document.getElementById('noattendees');
    noDiv.setAttribute('class', 'hidden');
    console.log(noDiv);
    meetingID = document.getElementById('meetingID');
    meetingID.value = row.firstElementChild.innerHTML;
};
    

document.addEventListener('DOMContentLoaded', selectButtons);


function get_attendees(allrows, row) {
    for (let r of allrows) {
      r.classList.remove('table-primary');
    };
    row.setAttribute('class', 'table-primary');
    let tableDiv = document.getElementById('attendeeTable');
    tableDiv.setAttribute('class', 'hidden');
    let noDiv = document.getElementById('noattendees');
    noDiv.setAttribute('class', 'hidden');
    let meetingID = row.firstElementChild.innerHTML;
    console.log('meetingID', meetingID);
    
    fetch('/get_attendees?meetingID=' + meetingID)
        .then(function (response) {
            return response.json();
        }).then(function (json) {
            console.log('length', json.length)
            console.log('GET response', json);
            if (json.length > 0) {
                let tableDiv = document.getElementById('attendeeTable');
                tableDiv.classList.remove('hidden')
                let tableBody = document.getElementById('tableBody');
                // remove previous table data
                tableBody.querySelectorAll('*').forEach(n => n.remove());
                // add new table data
                for (i = 0; i < json.length; i++) {
                    let newRow = document.createElement('tr');
                    let rowData = json[i];
                    // console.log('rowData', rowData);
                    for (let el in rowData) {
                        let newCell = document.createElement('td');
                        newRow.appendChild(newCell);
                        newCell.textContent = rowData[el];
                    };
                    let cell = document.createElement('td');
                    let button = document.createElement('input');
                    let buttonAttributes = {'type' : 'button', 
                                            'value' : 'Leave', 
                                            'id' : 'leave',
                                            'class' : 'btn btn-warning btn-sm' }
                    for (let attr in buttonAttributes) {
                        button.setAttribute(attr, buttonAttributes[attr]);
                    };
                    button.addEventListener('click', () => leaveClick(rowData['meetingID'], rowData['memberID']));
                    cell.appendChild(button);
                    newRow.appendChild(cell);
                    tableBody.appendChild(newRow);
                };
            } else {
                let noDiv = document.getElementById('noattendees');
                noDiv.classList.remove('hidden');
                console.log('no attendees for that meeting');
            };
        });
};

function leaveClick(meetingID, memberID) {
    console.log('leaveClick meetingID', meetingID, 'memberID', memberID);
};












attendee_select = document.getElementById('attendeeSelect');
console.log(attendee_select);
attendee_select.addEventListener('change', getMeetings);


function getMeetings() {
  club = this.value;
  console.log('club', club);
  
};