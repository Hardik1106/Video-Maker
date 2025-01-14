// window.onload = function() {
//     fetch('/getUserData')
//         .then(response => response.json())
//         .then(user => {
//             var userDetails = document.getElementById('userDetails');
//             userDetails.innerHTML = `
//                 <p>UserName: ${user.username}</p>
//                 <p>Email: ${user.email}</p>
//             `;
//             var name = document.getElementById('name');
//             name.innerHTML = `
//                 <p align="center">Hi ${user.name}!</p>
//             `;
//         });
// }

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
