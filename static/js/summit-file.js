var formAdd = document.getElementById("formAdd");

formAdd.addEventListener("submit", async function (event) {
    event.preventDefault();
    let fileInput = document.getElementById("myfiles");
    let formData = new FormData();
    
    // console.log(fileInput.files)
    for (var ele of fileInput.files){
        formData.append('files', ele);
    }
    // console.log(filesList);
    await sendFile(formData);
});

sendFile = async function (formData) {

    await fetch("/receipts/submitmultiple", {
        method: "POST",
        body: formData,
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate'
      },
    }).then(window.location.href = "/statusreceipts");
}
