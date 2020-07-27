
club_select = document.getElementById('clubSelect');
club_select.addEventListener('change', getBooks);

// getBooks function used when clubSelect dropdown menu is changed to 
// a different club, calls set_book_select to create the book dropdown menu
function getBooks() {
    clubID = this.value;
    console.log('clubID', clubID);
    fetch('/get_books_in_genre?clubID=' + clubID)
        .then(function (response) {
            return response.json();
        }).then(function (json) {
            // console.log('GET response', json);
            if (json.length > 0) {
                let postClubName = document.getElementById('postClubName');
                postClubName.disabled = false;
                set_book_select(json);
            };
        });
};

// Set the book drop down menu.
function set_book_select(json) {
    // console.log(json, selected_book)
    let bookSelect = document.getElementById('bookSelect');
    bookSelect.querySelectorAll('*').forEach(n => n.remove());
    let firstOption = document.createElement('option');
    firstOption.selected = true;    
    firstOption.disabled = true;
    firstOption.setAttribute('value', '');
    firstOption.textContent = 'Select a book';
    bookSelect.appendChild(firstOption);

    // add each option from json data
    for (i = 0; i < json.length; i++) {
        let newOption = document.createElement('option');
        let bookData = json[i];
        newOption.setAttribute('value', bookData[0]);
        newOption.textContent = bookData[1];
        bookSelect.appendChild(newOption);
    }; 
};
