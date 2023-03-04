var formAdd = document.getElementById("formAdd");
formAdd.addEventListener("change", function (event) {
    event.preventDefault();
    let fileInput = document.getElementById("myfiles");
    if (parseInt(fileInput.files.length) > 10){
        alert("You can only upload a maximum of 10 files");
       }
});