function handler(event) {
    let target = event.target;
    if (target.id) {
        if (target.id === "clipboard"){
            navigator.clipboard.writeText(target.textContent);
            return;
        }
    }  
};


document.addEventListener('click', handler);
