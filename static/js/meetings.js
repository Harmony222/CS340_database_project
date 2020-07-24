// console.log('Javascript connected')

club_select = document.getElementById('clubSelect');
club_select.addEventListener('change', getBooks);

// getBooks function used when clubSelect dropdown menu is changed to 
// a different club, calls set_book_select to create the book dropdown menu
function getBooks() {
    clubID = this.value;
    // console.log('clubID', clubID);
    fetch('/get_books_in_genre?clubID=' + clubID)
        .then(function (response) {
            return response.json();
        }).then(function (json) {
            // console.log('GET response', json);
            if (json.length > 0) {
                set_book_select(json);
            };
        });
};

// Set the book drop down menu. If selected_book argument
// is given, the list is created with that book as the 
// selected book.
function set_book_select(json, selected_book) {
    // console.log(json, selected_book)
    let bookSelect = document.getElementById('bookSelect');
    bookSelect.querySelectorAll('*').forEach(n => n.remove());
    let firstOption = document.createElement('option');
    firstOption.selected = true;    
    if (selected_book) {
        // if selected book is not None, add selected book to initial
        // drop done list
        if (selected_book[0] !== -1) {
            // console.log('selected_book', selected_book)
            firstOption.setAttribute('value', selected_book[0]);
            firstOption.textContent = selected_book[1];
            bookSelect.appendChild(firstOption)
        };
    } else {
        firstOption.disabled = true;
        firstOption.setAttribute('value', '');
        firstOption.textContent = 'Select a book';
        bookSelect.appendChild(firstOption);
    };

    for (i = 0; i < json.length; i++) {
        let newOption = document.createElement('option');
        let bookData = json[i];
        newOption.setAttribute('value', bookData[0]);
        newOption.textContent = bookData[1];
        bookSelect.appendChild(newOption);
    }; 
}

function buttons() {
    let allRows = Array.from(document.querySelectorAll('#meetingsTableBody tr'));
    // console.log(allRows);
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
    // console.log(row, modifyButton);
    meetingID = row.id;
    fetch('/meetings?meetingID=' + meetingID)
        .then(function (response) {
            return response.json();
        }).then(function (json) {
            // console.log('GET response', json);
            let formMeetingID = document.getElementById('formMeetingID');
            formMeetingID.value = meetingID
            let selectClub = document.getElementById('clubSelect');
            selectClub.value = json.meeting_data.bookClubID;
            let dateTime = new Date(json.meeting_data.dateTime);
            let dateString = convertDateString(dateTime);
            let timeString = convertTimeString(dateTime);
            // console.log(dateString, timeString);
            let formDate = document.getElementById('formDate');
            formDate.value = dateString;
            let formTime = document.getElementById('formTime');
            formTime.value = timeString;
            selected_book = json.books['selected_book'];
            books = json.books['book_options'];
            // call the set_book_select function to create a dropdown menu
            // pass in selected_book to have intial book menu include 
            // selected book value
            set_book_select(books, selected_book);
            let formBookID = document.getElementById('bookSelect');
            formBookID.value = selected_book[0];
            let formLeaderID = document.getElementById('formLeaderEmail');
            formLeaderID.value = json.leader_email.email;
        });
};

// converts date to string in format YYYY-MM-DD
function convertDateString(date) {
    var month = date.getMonth() + 1;
    if (month < 10) {
      var monthStr = '0' + month.toString();
    } else {monthStr = month.toString()};
    var day = date.getUTCDate();
    if (day < 10) {
      var dayStr = '0' + day.toString();
    } else {dayStr = day.toString()}
    let dateString = date.getFullYear().toString() + '-' + monthStr + '-' + dayStr;
    return dateString;
};

// converts time to string in format HH:MM:00
function convertTimeString(dateTime) {
    let hourStr = dateTime.getUTCHours();
    let minutes = dateTime.getMinutes();
    if (minutes < 10) {
        minutesStr = '0' + minutes.toString()
    } else { minutesStr = minutes.toString() }
    return hourStr + ':' + minutesStr + ':00';
};