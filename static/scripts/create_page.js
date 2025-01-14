document.addEventListener('DOMContentLoaded', function() {
    displayImages();
    displayAudio();

    // Add event listener to the create button
    document.querySelector('.create').addEventListener('click', function(event) {
        const imageForms = document.querySelectorAll('.image-form'); // Select by class
        const imageData = [];
        // Loop through each image form to collect duration and effect data
        imageForms.forEach(form => {
            const duration = parseInt(form.querySelector('.duration').value); // Parse duration as integer
            const effect = form.querySelector('.effect').value; // Select by class
            imageData.push({ duration, effect });
        });

        const audioForms = document.querySelectorAll('.audio-form'); // Select by class
        const audioData = [];
        // Loop through each audio form to collect duration data
        audioForms.forEach(form => {
            const duration = parseInt(form.querySelector('.duration').value); // Parse duration as integer
            audioData.push({ duration });
        });
        // Get the quality value
        const resolution = document.getElementById('resolution').value;
        const dimension = document.getElementById('dimension').value;
        // Send data to Flask backend using AJAX
        fetch('/create_video', {
            method: 'POST',
            body: JSON.stringify({ imageData , audioData , resolution, dimension}),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/create';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function createImageForm(container) {
    const form = document.createElement('form');
    form.classList.add('image-form'); // Add 'image-form' class
    const durationInput = document.createElement('input');
    durationInput.classList.add('duration');
    durationInput.setAttribute('type', 'number');
    durationInput.setAttribute('min', '0');
    durationInput.setAttribute('max', '30');
    durationInput.setAttribute('placeholder', 'Duration');

    const effectSelect = document.createElement('select');
    effectSelect.classList.add('effect'); // Add 'effect' class
    const effectOptions = ['None', 'FadeIn', 'FadeOut', 'FadeIn & FadeOut'];
    effectOptions.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        effectSelect.appendChild(optionElement);
    });

    form.appendChild(durationInput);
    form.appendChild(effectSelect);
    container.appendChild(form);
}

function createAudioForm(container) {
    const form = document.createElement('form');
    form.classList.add('audio-form'); // Add 'audio-form' class
    const durationInput = document.createElement('input');
    durationInput.classList.add('duration');
    durationInput.setAttribute('type', 'number');
    durationInput.setAttribute('min', '0');
    durationInput.setAttribute('placeholder', 'Duration');
    form.appendChild(durationInput);
    container.appendChild(form);
}

function displayImages() {
    const imageContainers = document.querySelectorAll('.phot');
    imageContainers.forEach(container => {
        createImageForm(container);
    });
}

function displayAudio() { 
    const audioContainers = document.querySelectorAll('.aud');
    audioContainers.forEach(container => {
        createAudioForm(container);
    });
}

// const audioFiles = [
//     'static/media/audios/Idea 22 (Sped Up).mp3',
//     'static/media/audios/Homecoming.mp3',
//     'static/media/audios/Indie Corporate.mp3',
//     'static/media/audios/Carousel.mp3'
// ];

// function createAudioElements() {
//     const audioContainer = document.getElementById('audioContainer');

//             audioFiles.forEach((audioPath, index) => {
//                 const audioElementContainer = document.createElement('div');
//                 audioElementContainer.classList.add('audio-element-container');

//                 const audioElement = document.createElement('audio');
//                 audioElement.controls = true;

//                 const sourceElement = document.createElement('source');
//                 sourceElement.src = audioPath;
//                 sourceElement.type = 'audio/mpeg';

//                 audioElement.appendChild(sourceElement);
//                 audioElementContainer.appendChild(audioElement);

//                 const audioNameLabel = document.createElement('label');
//                 audioNameLabel.textContent = getFileName(audioPath);
//                 audioElementContainer.appendChild(audioNameLabel);

//                 audioElementContainer.style.display = 'flex';
//                 audioElementContainer.style.alignItems = 'center';
//                 audioElementContainer.style.marginBottom = '20px';
//                 audioElementContainer.style.borderBottom = '1px solid #ccc';
//                 audioElementContainer.style.paddingBottom = '10px';
//                 audioElementContainer.style.gap = '10px';
//                 audioElementContainer.style.color='rgb(245, 226, 202)';

//                 audioContainer.appendChild(audioElementContainer);
//             });
// }

// function getFileName(path) {
//     return path.split('/').pop();
// }

function searchImages() {
    // Declare variables
    var input, filter, gallery, images, img, i, txtValue;
    input = document.getElementById('searchInput');
    filter = input.value.toUpperCase();
    gallery = document.getElementById("Image_Gallery");
    images = gallery.getElementsByClassName('phot');

    // Loop through all gallery images, and hide those that don't match the search query
    for (i = 0; i < images.length; i++) {
        img = images[i].getElementsByTagName("img")[0];
        txtValue = img.getAttribute("alt") || img.getAttribute("src");
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            images[i].style.display = "";
        } else {
            images[i].style.display = "none";
        }
    }
}

function searchAudios() {
    // Declare variables
    var input, filter, ul, li, audio, i, txtValue;
    input = document.getElementById('searchInput2');
    filter = input.value.toUpperCase();
    ul = document.getElementById('Audio_Gallery');
    li = ul.getElementsByClassName('aud');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        audio = li[i].getElementsByTagName('audio')[0];
        txtValue = audio.getAttribute('alt');
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}


document.getElementById("createVideoBtn").addEventListener("click", function() {
            // Show loading spinner when button is clicked
            document.getElementById("loadingSpinner").style.display = "block";
        });
