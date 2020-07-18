console.log("javascript connected");

club_select = document.getElementById('clubSelect');
console.log(club_select);
club_select.addEventListener('change', getBooks);

function getBooks() {
    clubID = this.value;
    console.log('clubID', clubID);
    document.getElementById('clubSelectForm').submit();


};

// function getBooks() {
//     clubID = this.value;
//     console.log('clubID', clubID);
    
//     fetch('/get_books?clubID=' + clubID)
//         .then(function (response) {
//             return response.json();
//         }).then(function (json) {
//             console.log('length', json.length);
//             console.log('GET response', json);
//             if (json.length > 0) {
//                 let selectDiv = document.getElementById('bookSelect');
//                 console.log(selectDiv)
//                 selectDiv.querySelectorAll('*').forEach(n => n.remove());
//                 let firstOption = document.createElement('option');
//                 firstOption.selected = true;
//                 firstOption.disabled = true;
//                 firstOption.setAttribute('value', '');
//                 firstOption.textContent = 'Select a book';
//                 selectDiv.appendChild(firstOption);
//                 for (i = 0; i < json.length; i++) {
//                     let newOption = document.createElement('option');
//                     let bookData = json[i];
//                     console.log('bookData', bookData);
//                     newOption.setAttribute('value', bookData[0]);
//                     newOption.textContent = bookData[1] + ' by ' + bookData[2];
//                     selectDiv.appendChild(newOption);
//                 };
//             }
//         });
// };