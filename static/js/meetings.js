console.log('Javascript connected')

let allRows = Array.from(document.querySelectorAll('#meetingsTableBody tr'));
console.log(allRows);
let modifyButton = allRows[0].querySelector('.modify');
console.log(modifyButton)
let deleteButton = allRows[0].querySelector('.delete');
console.log(deleteButton)