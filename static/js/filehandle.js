function getFiles(){
    (async () => { 
    const titleEle = document.getElementsByClassName("title")[0];
    const dataStr = await getData("info");
    dataStr.innerHTML = "";
    titleEle.innerHTML = dataStr
    const files = await getData("files");
    JSON.parse(files).forEach(element => {
        console.log(element)
        const nc = document.createElement("div");
        nc.classList.add("item");
        if(String(element).endsWith(".jpg")){ 
            nc.innerHTML = `<img src="${element}"></img>`
        } else if (String(element).endsWith(".mp4")) {
            nc.innerHTML = `<video controls="controls" src="${element}"></video>`
              //      
        }
        const nc2 = document.createElement("div");
        nc2.classList.add("close");
        nc2.innerHTML = "x";
        nc2.addEventListener("click",()=>{ 
            if (window.confirm('delete file?')){
                nc.remove()
                getData(`delete/${element}`)
            }
        })
        nc.append(nc2)
        document.getElementsByClassName("content")[0].append(nc); 
    });
})()
}
getFiles()
function openFilePicker() {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = 'all'; // Define the file types you want to accept
    input.multiple = true; // Allow multiple files selection

    input.onchange = function(e) {
        var files = e.target.files;
        for (var i = 0; i < files.length; i++) {
            uploadFile(files[i]);
        }
    };

    input.click();
}

function uploadFile(file) {
    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    console.log("far")
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(xhr.responseText); // Handle success response
            location.reload()
        } else {
            console.error(xhr.statusText); // Handle error
        }
    };

    xhr.onerror = function() {
        console.error('Request failed'); // Handle network error
    };

    xhr.send(formData);
}