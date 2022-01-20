const globalVars = {    //defining elements at global scope
    'vw' : Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0),
    'vh' : Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0),
    'sideFoot' : document.getElementById('sidebar-footer'),
    'mainFoot' : document.getElementById('footer'),
    'simBox' : document.getElementById('sim-text'),
    'credits' :document.getElementsByClassName('recog'),
    'discordFooter' : document.getElementById('foot-disc'),
    'fightDuration' : document.getElementById('fight_duration'),
    'opts': [   //dropdowns for equipment and talent points
        document.getElementById('tinket1'),
        document.getElementById('tinket2'),
        document.getElementById('idol'),
        document.getElementById('intensity'),
        document.getElementById('dreamstate')
    ],
    'sel' : document.getElementsByClassName('gear-select'),
    'manaButton' : document.getElementById('mana-management-button'),   //mana collapse button
    'simManaCheck' : document.getElementById('is_mana_simulated'),  //mana sim checkbox
    'manaPanel' : document.getElementById('collapseOne'),   //mana form
    'manaSimDropdown' : document.getElementById('mana-management'), //mana accordion
    'spriestCheck' : document.getElementById('is_shadow_priest'),   //spriest check
    'spriestBox' : document.getElementById('spriest-dps')   //spriest dps box
};
//on page load
window.addEventListener('load', (event) => {
    globalVars.simManaCheck.checked ? globalVars.manaSimDropdown.classList.remove('d-none') : globalVars.manaSimDropdown.classList.add('d-none');
    globalVars.spriestCheck.checked ? globalVars.spriestBox.classList.remove('d-none') : globalVars.spriestBox.classList.add('d-none');
    //takes the preserved value and divides it by 30, then subtracts by 1 to account for indexing
    globalVars.simBox ? globalVars.fightDuration.options[((+globalVars.fightDuration.value) / 30) - 1].selected = true : '';
    globalVars.opts.forEach(i=>slotMemory(i));  //loops over user selects and calls the memory function
    globalVars.simManaCheck.addEventListener('click', function(){
        globalVars.simManaCheck.checked ? globalVars.manaSimDropdown.classList.remove('d-none') : globalVars.manaSimDropdown.classList.add('d-none');
     });
     //when spriest is checked, spriest dps appears
     globalVars.spriestCheck.addEventListener('click', function(){
        globalVars.spriestCheck.checked ? globalVars.spriestBox.classList.remove('d-none') : globalVars.spriestBox.classList.add('d-none');
     });
    
    document.getElementById('sim-text') ? //changes sidebar style to make room for simbox and focuses the sim numbers if they exist
    (document.getElementById('sidebar-footer').classList.remove('sidebar-footer-no-sim'), document.getElementById('sim-text').scrollIntoView()) : '';
    
    //defaults sidebar footer to hidden on mobile
    if(globalVars.vw <= 900 || globalVars.vh <= 650){
        if(globalVars.sideFoot){
            globalVars.sideFoot.classList.add('d-none');
        }
        if(globalVars.discordFooter){
            globalVars.discordFooter.classList.remove('d-none');
        }
    }
    //when the mana sim checkbox is ticked, the mana options show up
    
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
/*function for preserving choices*/
function slotMemory(item){
    for(let i = 1; i < item.options.length; i++){
        if(item.options[i].value === item.options[0].value){
            item.options[i].selected = true;
        }
    }
}
//adjusts where the discord link appears ( sidebar --> footer )
function switchVis(){
    if(window.innerWidth <= 900 || window.innerHeight <= 650){
        if(!globalVars.sideFoot.classList.contains('d-none')){
            globalVars.sideFoot.classList.add('d-none');
            console.log('sidebar foot shouldn\'t be visible');
        }
        if(globalVars.discordFooter){
            globalVars.discordFooter.classList.remove('d-none');
        }

    }else{
        if(globalVars.sideFoot.classList.contains('d-none')){
            globalVars.sideFoot.classList.remove('d-none');
            console.log('sidebar foot should be visible');
        }
        if(globalVars.discordFooter){
            globalVars.discordFooter.classList.add('d-none');
        }
    }
}