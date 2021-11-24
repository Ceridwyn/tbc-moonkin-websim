//defining elements at global scope
var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
var sideFoot = document.getElementById('sidebar-footer');
var mainFoot = document.getElementById('footer');
var simBox = document.getElementById('sim-text');
var credits = document.getElementsByClassName('recog');
var discordFooter = document.getElementById('foot-disc');
var fightDuration = document.getElementById('fight_duration');
var trink1 = document.getElementById('tinket1');
var trink2 = document.getElementById('tinket2');
var idol = document.getElementById('idol');
var intensity = document.getElementById('intensity');
var dreamstate = document.getElementById('dreamstate');
var sel = document.getElementsByClassName('gear-select');

//mana collapse button
var manaButton = document.getElementById('mana-management-button');
//mana sim checkbox
var simManaCheck = document.getElementById('is_mana_simulated');
//mana form
var manaPanel = document.getElementById('collapseOne');
//mana accordion
var manaSimDropdown = document.getElementById('mana-management');
//spriest check
var spriestCheck = document.getElementById('is_shadow_priest');
//spriest dps box
var spriestBox = document.getElementById('spriest-dps');

//adjusts where the discord link appears ( sidebar --> footer )
function switchVis(){
    if(window.innerWidth <= 900 || window.innerHeight <= 650){
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
    console.log(simManaCheck.checked);
    simManaCheck.checked ? manaSimDropdown.classList.remove('d-none') : manaSimDropdown.classList.add('d-none');
    spriestCheck.checked ? spriestBox.classList.remove('d-none') : spriestBox.classList.add('d-none');
    //preserving user choice for fight duration
    if(simBox){
        //takes the preserved value and divides it by 30, then subtracts by 1 to account for indexing
        fightDuration.options[((+fightDuration.value) / 30) - 1].selected = true;
        console.log('selected index: ' + fightDuration.selectedIndex);
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

	// User Intensity points
	for(let i = 1; i < intensity.options.length; i++){
        if(intensity.options[i].value === intensity.options[0].value){
            intensity.selectedIndex = i;
        }
    }
	// User Dreamstate points
    for(let i = 1; i < dreamstate.options.length; i++){
        if(dreamstate.options[i].value === dreamstate.options[0].value){
            dreamstate.selectedIndex = i;
        }
    }
    //changes sidebar style to make room for simbox
    if(document.getElementById('sim-text')){
        document.getElementById('sidebar-footer').classList.remove('sidebar-footer-no-sim');
    }

    //defaults sidebar footer to hidden on mobile
    if(vw <= 900 || vh <= 650){
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

    //when the mana sim checkbox is ticked, the mana options show up
    simManaCheck.addEventListener('click', function(){
       simManaCheck.checked ? manaSimDropdown.classList.remove('d-none') : manaSimDropdown.classList.add('d-none');
    });

    //when spriest is checked, spriest dps appears
    spriestCheck.addEventListener('click', function(){
       spriestCheck.checked ? spriestBox.classList.remove('d-none') : spriestBox.classList.add('d-none');
    });

    //stop the dropdown from animating while it's open
    let selects = document.getElementsByClassName('select');
    for(let i of selects){
        i.addEventListener('focusin', function(){
            i.classList.add('stopAnimate');
            console.log('should not animate');
            //console.log(i.classList);
        })
        i.addEventListener('focusout', function(){
            i.classList.remove('stopAnimate');
            console.log('should animate');
            //console.log(i.classList);
        })
    }
});
//adjusts certain elements' visibility at diff viewport sizes on resize
window.onresize = switchVis;

//loading spinner 
document.getElementById('submitBtn').addEventListener('click', event => {
  document.getElementById('spinner').classList.remove('d-none');
  document.getElementById('sim-text').classList.add('d-none');
});