// image input
function previewImage(event, imgs) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function () {
    var img = document.getElementById(imgs);
    img.src = reader.result;
  };
  reader.readAsDataURL(input.files[0]);
}

function menubtn() {
  var menubar = document.querySelector('.menubar');
  var body = document.querySelector('.body');
  if (menubar.style.display === 'none') {
    menubar.style.display = 'block';
    body.style.marginRight = '181px';
  } else {
    menubar.style.display = 'none';
    body.style.marginRight = 0;
  }
}

function setInputValue(value) {
  inputField.value = value;
  optionsList.style.display = "none";
  
}

function printPdf(pdfUrl) {
  var printWindow = window.open(pdfUrl, '_blank');
  printWindow.onload = function() {
      printWindow.print();
  };
}


var today = new Date();
var day = today.getDate();
var month = today.getMonth() + 1; // Adding 1 to get the correct month (0 - 11)
var year = today.getFullYear();

// Pad day and month with leading zeros if needed
if (day < 10) {
  day = "0" + day;
}

if (month < 10) {
  month = "0" + month;
}

var formattedDate = day + "/" + month + "/" + year;
console.log(formattedDate);

var dateParts = formattedDate.split("/");
var formattedValue = dateParts[2] + "-" + dateParts[1] + "-" + dateParts[0];

document.getElementsByName("date_txt")[0].value = formattedValue;