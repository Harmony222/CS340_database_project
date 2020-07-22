console.log('Javascript connected')

club_select = document.getElementById('clubSelect');
console.log(club_select);
club_select.addEventListener('change', getBooks);

function getBooks() {
    clubID = this.value;
    console.log('clubID', clubID);
    document.getElementById('clubSelectForm').submit();
};

// // Add id
// let options = Array.from(document.querySelectorAll('#clubSelect option'));
// console.log('options', options);
// for (let option of options) {
//     console.log(option.value);
//     option.setAttribute('id', 'opt' + option.value);
// };

function buttons() {
    let allRows = Array.from(document.querySelectorAll('#meetingsTableBody tr'));
    console.log(allRows);
    for (i = 0; i < allRows.length; i++) {
        let row = allRows[i];
        // console.log(row);
        let modifyButton = row.querySelector('.modify');
        let deleteButton = row.querySelector('.delete');
        modifyButton.addEventListener('click', () => modifyClick(row, modifyButton))
    };
};

document.addEventListener('DOMContentLoaded', buttons);

function modifyClick(row, modifyButton) {
    console.log(row, modifyButton);
    meetingID = row.id;
    fetch('/meetings?meetingID=' + meetingID)
        .then(function (response) {
            return response.json();
        }).then(function (json) {
            console.log('GET response', json);
            console.log(json.bookClubID);
            console.log(json.dateTime);
            console.log(typeof json.dateTime);
            let dateTime = new Date(json.dateTime);
            let date = dateTime.getDate();
            let time = dateTime.getTime();
            console.log(date, time);

            let dateString = convertDateString(dateTime);
            console.log(dateString);
            console.log(dateTime.toLocaleTimeString('it-IT'));
            console.log(dateTime.getUTCHours());
            console.log(dateTime.getMinutes());
            let selectClub = document.getElementById('clubSelect');
            selectClub.value = json.bookClubID;
            let subFormDate = document.getElementById('subFormDate');

            // document.getElementById('clubSelectForm').submit();
        });

    // meetingID = row.id;
    // let dateTime = row.querySelector('.dateTime').textContent;
    // console.log(dateTime);
    // let date = dateTime.slice(0, 10);
    // let time = dateTime.slice(11);
    // console.log(date);
    // console.log(time);
    // let formDate = document.getElementById('subFormDate');
    // formDate.value = date;
    // let formTime = document.getElementById('formTime');
    // formTime.value = time;
    // let options = Array.from(document.querySelectorAll('#clubSelect option')); 
    // for (let option of options) {
    //     option.setAttribute('selected', false);
    //     // console.log('option value', option.value)
    //     if (option.value === meetingID) {
    //         option.setAttribute('selected', true);
    //         document.getElementById('clubSelectForm').submit();
    //     };
    // };
};

function convertDateString(date) {
    var month = date.getMonth() + 1;
    if (month < 10) {
      var monthStr = '0' + month.toString();
    } else {monthStr = month.toString()};
    var day = date.getUTCDate();
    if (day < 10) {
      var dayStr = '0' + day.toString();
    } else {dayStr = day.toString()}
    let dateString = monthStr + '-' + dayStr + '-' + date.getFullYear().toString();
    return dateString;
  }