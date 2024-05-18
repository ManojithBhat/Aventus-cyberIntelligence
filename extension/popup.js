chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const tabUrl = tabs[0].url;
    
    console.log("URL of the active tab:", tabUrl);

    let documentatio=document.querySelector(".documentation");
    if (!(tabUrl.startsWith("https://www.instagram.com/"))) {
        console.log("No Instagram account found");
        let lt=document.querySelector(".loading-paragraph");
        lt.classList.add("redcolor")
        lt.innerHTML="Not a Instagram profile";
        return; // Exit the function if the URL doesn't match
    }

const url = `http://localhost:8080/endpoint/${encodeURIComponent(tabUrl)}`;

console.log(url);
document.addEventListener('DOMContentLoaded', function() {
    documentatio.addEventListener('click', function() {
      chrome.tabs.create({ url: 'www.google.com', active: true });
    });
  });
fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Response from server:', data);
        console.log(data.message);
        
        if('0'===data.message)
        {
            let im = document.createElement("img");
            im.setAttribute("src", "./correct.png");
            im.classList.add("correctimage");
            let insscanning = document.querySelector('.insidescanning');
            let spanElement = insscanning.querySelector("span");
            if (spanElement) 
            {
                insscanning.removeChild(spanElement);
            }
            insscanning.appendChild(im);
            let lt = document.querySelector(".loading-paragraph");
            lt.classList.add("greencolor");
            lt.innerHTML = "Safe account!";
        }
        else{
            let im = document.createElement("img");
            im.setAttribute("src", "./wrong.png");
            im.classList.add("wrongimage");
            let insscanning = document.querySelector('.insidescanning');
            let spanElement = insscanning.querySelector("span");
            if (spanElement) 
            {
                insscanning.removeChild(spanElement);
            }
            insscanning.appendChild(im);
        let lt=document.querySelector(".loading-paragraph");
        lt.classList.add("redcolor")
        lt.innerHTML="Spam account!";
        }
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });

});
