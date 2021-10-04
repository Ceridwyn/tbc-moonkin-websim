//defining elements at global scope
var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
var sideFoot = document.getElementById('sidebar-footer');
var mainFoot = document.getElementById('footer');
var credits = document.getElementsByClassName('recog');
var discordFooter = document.getElementById('foot-disc');

//adjusts where the discord link appears ( sidebar --> footer )
function switchVis(){
    if(window.innerWidth <= 900){
        if(!sideFoot.classList.contains('d-none')){
            sideFoot.classList.add('d-none');
            console.log('sidebar foot shouldn\'t be visible');
        }
        if(discordFooter){
            discordFooter.classList.remove('d-none');
        }

    }else{
        if(sideFoot.classList.contains('d-none')){
            sideFoot.classList.remove('d-none');
            console.log('sidebar foot should be visible');
        }
        if(discordFooter){
            discordFooter.classList.add('d-none');
        }
    }
}

//on page load
window.addEventListener('load', (event) => {
    //changes sidebar style to make room for simbox
    if(document.getElementById('sim-text')){
        document.getElementById('sidebar-footer').classList.remove('sidebar-footer-no-sim');
    }

    //defaults sidebar footer to hidden on mobile
    if(vw <= 900){
        if(sideFoot){
            sideFoot.classList.add('d-none');
        }
        if(discordFooter){
            discordFooter.classList.remove('d-none');
        }
    }

    //focuses the sim numbers if they exist
    if(document.getElementById('sim-text')){
        document.getElementById('sim-text').scrollIntoView();
    }
});
//adjusts certain elements' visibility at diff viewport sizes on resize
window.onresize = switchVis;