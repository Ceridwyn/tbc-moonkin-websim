function scrollTo(hash) {
    location.hash = "#" + hash;
}
window.addEventListener('load', (event) => {
    if(document.getElementById('sim-text')){
        scrollTo('sim-text');
    }
});