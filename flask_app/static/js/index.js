//defining elements at global scope
var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
var sideFoot = document.getElementById('sidebar-footer');
var mainFoot = document.getElementById('footer');
var credits = document.getElementsByClassName('recog');
var discordFooter = document.getElementById('foot-disc');
var fightDuration = document.getElementById('fight_duration');
var trink1 = document.getElementById('tinket1');
var trink2 = document.getElementById('tinket2');
var idol = document.getElementById('idol');


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
    //preserving user choice for fight duration
    if(fightDuration.value){
        fightDuration.options[(fightDuration.value - 30) / 30].selected = true;
    }

    //user trinket 1
    for(let i = 1; i < trink1.options.length; i++){
        if(trink1.options[i].value === trink1.options[0].value){
            trink1.options[i].selected = true;
        }
    }

    //user trinket 2
    for(let i = 1; i < trink2.options.length; i++){
        if(trink2.options[i].value === trink2.options[0].value){
            trink2.selectedIndex = i;
        }
    }

    //user idol
    for(let i = 1; i < idol.options.length; i++){
        if(idol.options[i].value === idol.options[0].value){
            idol.selectedIndex = i;
        }
    }
    console.log(trink1.options);

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

//loading spinner 
document.getElementById('submitBtn').addEventListener('click', event => {
  document.getElementById('spinner').classList.remove('d-none');
  document.getElementById('sim-text').classList.add('d-none');
});