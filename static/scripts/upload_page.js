photoinput = document.querySelector(".photo-div input");
photoinputDiv = document.querySelector(".gallery1");
imagesArray = [];

photoinput.addEventListener("change",()=>{
    const files = photoinput.files;
    for(let i = 0; i < files.length; i++) imagesArray.push(files[i]);
    displayImages();
})

photoinputDiv.addEventListener("drop", (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;

    for (let i = 0; i < files.length; i++) {
        if (!files[i].type.match("image")) continue;
        imagesArray.push(files[i]);
    }

    displayImages();
});

photoinputDiv.addEventListener("dragover", (e) => {
    e.preventDefault();
});

function  displayImages(){
    
    let images = "";

    for(let i = 0; i < imagesArray.length; i++){
        let curname = "select-image-";
        curname += i.toString();
        images += `
        <div class="phot">
            <img class="image" src="${URL.createObjectURL(imagesArray[i])}">
            <select name=${curname} id="duration">
                <option value="select">Save</option>
                <option value="dontselect">Dont Save</option>
            </select>
        </div>`
    };

    document.querySelector(".gallery1").innerHTML = images;
}

audioinput = document.querySelector(".audio-div input");
audioinputDiv = document.querySelector(".gallery2");
audioArray = [];

audioinput.addEventListener("change",()=>{
    const files = audioinput.files;
    for(let i = 0; i < files.length; i++) audioArray.push(files[i]);
    displayAudio();
})

audioinputDiv.addEventListener("drop", (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    for (let i = 0; i < files.length; i++) {
        if (!files[i].type.match("audio")) continue;
        audioArray.push(files[i]);
    }
    displayAudio();
});

audioinputDiv.addEventListener("dragover",(e)=>{
    e.preventDefault();
})

function displayAudio(){

    let audios = "";
    for(let i = 0; i < audioArray.length; i++){
        let curname = "select-audio-";
        curname += i.toString();
        audios += `
        <div class="phot">
            <audio controls src="${URL.createObjectURL(audioArray[i])}"></audio>
            <select name=${curname} id="duration">
                <option value="select">Save</option>
                <option value="dontselect">Dont Save</option>
            </select>
        </div>`;
    }

    document.querySelector(".gallery2").innerHTML = audios;
}


