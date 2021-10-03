import numpy
from . import buffs_list
from . import character

class Encounter:
    def __init__(
    self,
    char,
    buffs,
    fight_length,
    rotation = "Moonfire Starfire"):
        self.fight_length = fight_length
        self.rotation = rotation
        self.char = char
        self.buffs = buffs
    
    def parse_rotation(self):
        pass
    
    def logfunc(self, s):
        is_log_on = False
        if is_log_on:
            print(s)
    
    def compute_dps(self, iteration_nb = 1):
        rng = numpy.random.RandomState(26082019)
        buff_dict = self.buffs.get_stats_buffs()
        intel = self.char.intel + buff_dict.get("intel") 
        crit_score = self.char.crit_score + buff_dict.get("crit_score")
        hit_score = self.char.hit_score + buff_dict.get("hit_score")
        spellpower = self.char.spellpower + buff_dict.get("spellpower")
        haste = self.char.haste + buff_dict.get("haste")
        spirit = self.char.spirit + buff_dict.get("spirit")
        is_idol_of_moongoddess = True if self.char.idol == "Idol of the Moongoddess" else False
        if self.char.idol == "Idol of the Raven Goddess":
            crit_score = crit_score + 20
        # Apply kings after all :
        if self.buffs.is_blessing_kings:
            intel = intel * 1.1
            spirit = spirit * 1.1
        #intel, crit_score, hit_score, spellpower, haste, is_csd, is_spellstrike, is_spellfire
        MF_coeff = 0.15
        if self.buffs.is_T6_2:
            MF_coeff_dot = 0.65
        else:
            MF_coeff_dot = 0.52
        # Starfire base damage : Causes 550 to 647 Arcane damage -> 658 on average
        SF_coeff = 1
        # isApple = True if fruit == 'Apple' else False
        SF_average_damage = 598.5 + 55 if is_idol_of_moongoddess else 598.5
        MF_average_damage = 331
        if self.buffs.is_T6_2:
            MF_average_dot_damage = 750
        else:
            MF_average_dot_damage = 600
        
        # Apply spell haste coefficients here
        # 15.77 Spell Haste Rating increases casting speed by 1%
        # % Spell Haste at level 70 = (Haste Rating / 15.77)
        # New Casting Time = Base Casting Time / (1 + (% Spell Haste / 100))
        spell_haste = haste / 15.77
        # sf_cast_time = 3 / (1 + (spell_haste/100))
        # sf_cast_time_ng = 2.5 / (1 + (spell_haste/100))
        # print("SF Cast time : " + str(sf_cast_time))
        # print("SF NG Cast time : " + str(sf_cast_time_ng))

        # Spell power calculation for fight SP + lunar guidance 
        if self.char.lunar_guidance:
            spellpower = spellpower + 0.25 * intel
        if self.char.is_spellfire:
            spellpower = spellpower + 0.07 * intel
        if self.buffs.is_divine_spirit:
            spellpower = spellpower + .1 * spirit
        
        # Hit chance
        # 12.6 Spell Hit Rating -> 1%
        hit_chance = min(99, 83 + (hit_score/12.6) + self.char.balance_of_power )
        hit_chance_percent_value = hit_chance / 100
        self.logfunc("Hit chance is : " + str(hit_chance))

        # Crit chance
        # At level 70, 22.1 Spell Critical Strike Rating -> 1%
        # Druids receive 1% Spell Critical Strike chance for every 79.4 points of intellect.
        MF_crit_percent = crit_score/22.1 + intel/79.4 + self.char.improved_mf + self.char.moonkin_form 
        MF_crit_percent_value = MF_crit_percent / 100
        self.logfunc("Moonfire crit chance is : " + str(MF_crit_percent))
        if self.buffs.is_T6_4 == True:
            SF_crit_percent =  crit_score/22.1 + intel/79.4 +  self.char.moonkin_form + self.char.focused_starlight + 5
        else: 
            SF_crit_percent =  crit_score/22.1 + intel/79.4 +  self.char.moonkin_form + self.char.focused_starlight
        SF_crit_percent_value = SF_crit_percent / 100
        self.logfunc("Starfire crit chance is : " + str(SF_crit_percent))
        self.logfunc("Spellpower is  : " + str(spellpower))
        self.logfunc("Intel : " + str(intel))
        # Crit coeff
        if self.char.is_csd:
            crit_coeff = 2.09
        else:
            crit_coeff = 2
        
        # Spellstrike bonus:
        if self.char.is_spellstrike:
            spellstrike_bonus = 92
        else:
            spellstrike_bonus = 0
        
        # Prepare and launch the simulations
        # loop_size = 1000 # number of fights simulated
        average_dps = 0
        n = 0
        while n < iteration_nb:
            n = n + 1
            # Initialization
            total_damage_done = 0
            damage = 0
            fight_time = 0
            spellstrike_uptime = 0
            eye_of_mag_uptime = 0
            ff_uptime = 0
            mf_uptime = 0
            trinket_uptime = 0
            trinket_cd_timer = 0
            is_trinket_active = False
            is_trinket_available = True
            is_ff_up = False
            is_mf_up = False
            is_ng = False
            is_eye_of_mag_triggered = False
            is_sextant_of_unstable_currents_triggered = False
            is_ashtongue_triggered = False
            spellstrike_proc = False
            ng_proc = False
            drum_time = 0
            drum_cd = 0
            eye_of_quagg_icd = 0
            eye_of_quagg_proc = False
            eye_of_quagg_uptime = 0
            sextant_of_unstable_currents_icd = 0
            sextant_of_unstable_currents_proc = False
            sextant_of_unstable_currents_uptime = 0
            sextant_icd = 45
            ashtongue_uptime = 0
            skull_uptime = 0
            skull_cd = 0
            skull_active = False
            lust_amount = self.buffs.lust_count
            lust_uptime = 0
            lust_when = 100
            lust_start = 1 - (lust_when/100)
            lusted = False
            fight_haste = spell_haste
            # Time to kick ass and chew bubble gum
            while fight_time <= self.fight_length:
                loop_duration = max(1, (1.5 / (1 + (fight_haste / 100)))) #GCD - can't be less, it's the rule !
                damage = 0
                # adding a variable to keep the initial spellpower to revert to this value in case a trinket bonus
                # fades out before the end of the SF / Wrath cast (ie. no spellpower snapshot)
                loop_start_spellpower = spellpower
                if spellstrike_proc:
                    fight_spell_power = spellpower + spellstrike_bonus
                else:
                    fight_spell_power = spellpower
               
                if is_eye_of_mag_triggered:
                    fight_spell_power = fight_spell_power + 170  
                
                if is_sextant_of_unstable_currents_triggered:
                    fight_spell_power = spellpower + 190
     
                if is_ashtongue_triggered:
                    fight_spell_power = spellpower + 150
                
                if self.buffs.is_drums and drum_cd <= 0:
                    drum_time = 30
                    drum_cd = 120
                    drums_up = True
                    fight_haste = fight_haste + (80/15.77)
                   # self.logfunc(" drums up !!! fight haste is " + str(fight_haste))
                    
                if self.buffs.is_lust and lust_amount >= 1 and fight_time >= (lust_start * self.fight_length) and lusted == False:
                    lust_amount = lust_amount - 1
                    fight_haste = fight_haste + 30
                    lust_uptime = 40
                    lusted = True
                    #self.logfunc("lust up, lust amount is " + str(lust_amount) + " fight time is " + str(fight_time))
                    
                if self.char.skull and skull_cd <= 0 and is_ff_up:
                    fight_haste = fight_haste + (175/15.77)
                    skull_uptime = 20 
                    skull_cd = 120
                    skull_active = True
                    #self.logfunc("skull activated!!")
                    
                    
                # if FF not up, cast FF
                if not is_ff_up:
                    self.logfunc("Casting Faerie Fire !")
                    loop_duration = max(1, (1.5 / (1 + (fight_haste/100)))) #GCD
                    is_crit = False # can't crit on FF
                    damage = 0 # and no damage applied
                    if(rng.random() <= hit_chance_percent_value):
                        is_hit = True
                        ff_uptime = 40
                        is_ff_up = True
                        # Test if spellstrike is proc -> Commented out because tested later on in the code
                        # spellstrike_proc = (rng.randint(1, high = 101, size = 1) <= 10)
                    else:
                        is_hit = False
                        self.logfunc("Faerie Fire -> Resist !")
                # if Moonfire not up, cast Moonfire
                else:
                    # Once FF is up trigger trinket if available.
                    if is_trinket_active:
                        # apply spell modifier
                        fight_spell_power = fight_spell_power + self.char.spellpower_trinket_bonus
                    else:
                        if is_trinket_available and self.char.is_trinket_activable:
                            # activate trinket
                            self.logfunc("Trinket activation !!")
                            is_trinket_active = True
                            # start the chrono of activation
                            trinket_uptime = self.char.trinket_duration
                            # start the chrono of CD
                            trinket_cd_timer = self.char.trinket_cd
                    #
                    if not is_mf_up:
                        self.logfunc("Casting Moonfire !")
                        loop_duration = max(1, (1.5 / (1 + (fight_haste/100)))) #GCD because we cast a spell
                        # Is it a hit ?
                        if(rng.random() <= hit_chance_percent_value):
                            is_hit = True
                            # Is it a crit ?
                            is_crit = (rng.random() <= MF_crit_percent_value)
                            # Is it a partial ?
                            #if(rng.randint(1, high = 101, size = 1) <= hit_chance):
                            #    damage = MF_average_damage + MF_coeff * fight_spell_power * partial_coeff
                            damage = MF_average_damage + MF_coeff * fight_spell_power
                            # Apply damage
                            if is_crit:
                                damage = damage * crit_coeff
                            # DoT :
                            if self.buffs.is_T6_2:
                                damage = damage + MF_average_dot_damage + (MF_coeff_dot * fight_spell_power * min(15, (self.fight_length - fight_time - 1.5))/15)
                            else:
                                damage = damage + MF_average_dot_damage + (MF_coeff_dot * fight_spell_power * min(12, (self.fight_length - fight_time - 1.5))/12)
                            
                            # There is a Hit ! update model
                            if self.buffs.is_T6_2:
                                is_mf_up = True
                                mf_uptime = 15
                            else:
                                is_mf_up = True
                                mf_uptime = 12
                        else:
                            is_hit = False
                            self.logfunc("Moonfire -> Resist ! ")
                    else:
                        # Cast Starfire
                        self.logfunc("Casting Starfire !")
                        sf_cast_time = 3 / (1 + (fight_haste/100))
                        sf_cast_time_ng = 2.5 / (1 + (fight_haste/100))
                         # Computing loop duration
                        if is_ng:
                            sf_cast_time_ng = max(1, (2.5 / (1 + (fight_haste/100))))
                            loop_duration = max(1, sf_cast_time_ng)
                        else:
                            sf_cast_time = max(1, (3 / (1 + (fight_haste/100))))
                            loop_duration = max(1, sf_cast_time)
                        is_ng = False # Consume NG once SF is cast   
                        # Is it a hit ?
                        # if(rng.randint(1, high = 101, size = 1) <= hit_chance):
                        if(rng.random() <= hit_chance_percent_value):
                            is_hit = True
                            if self.char.ashtongue_talisman and rng.randint(1, high = 5, size = 1) == 1:
                                is_ashtongue_triggered = True
                                ashtongue_uptime = 8
                                self.logfunc("Ashtongue Proc !!")
                            # Is it a crit ?
                            is_crit = (rng.random() <= SF_crit_percent_value)
                            if is_crit:
                                self.logfunc("Starfire -> Crit ! ")
                            # Is it a partial ?
                            #if(rng.randint(1, high = 101, size = 1) > hit_chance):
                            #    self.logfunc("Partial hit !")
                            #    damage = (SF_average_damage + (SF_coeff * fight_spell_power * wrath_of_cenarius * partial_coeff )) * moonfury
                                # self.logfunc("Damage done : " + str(damage))
                            
                                                
                            
                            # Let's check if the cast is finished before trinket bonus, if not, we remove the relevant bonus :
                            if spellstrike_proc and (spellstrike_uptime < loop_duration):
                                fight_spell_power = fight_spell_power - spellstrike_bonus 
                                self.logfunc("Spellstrike fades out to early ...")
                            if is_eye_of_mag_triggered and (eye_of_mag_uptime < loop_duration):
                                fight_spell_power = fight_spell_power - 170
                                self.logfunc("Eye of Mag fades out to early ...")
                            if is_sextant_of_unstable_currents_triggered and (sextant_of_unstable_currents_uptime < loop_duration):
                                fight_spell_power = fight_spell_power - 190
                                self.logfunc("Sextant fades out to early ...")
                            if is_ashtongue_triggered and (ashtongue_uptime < loop_duration):
                                fight_spell_power = fight_spell_power - 150
                                self.logfunc("Ashtongue fades out to early ...")
                            
                            # end of trinket verification
                            if self.buffs.is_T5 and is_ng and mf_uptime >= sf_cast_time_ng:
                                damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius )) * self.char.moonfury * 1.1                            
                            elif self.buffs.is_T5 and mf_uptime >= sf_cast_time:
                                damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius )) * self.char.moonfury * 1.1                        
                            else:
                                damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius )) * self.char.moonfury                            
                            if is_crit:
                                damage = damage * crit_coeff
                                self.logfunc("Damage done : " + str(damage))
                        else:
                            is_hit = False
                            self.logfunc("Starfire -> Resist ! ")


                # Update time and model
                fight_time = fight_time + loop_duration
                ff_uptime = ff_uptime - loop_duration
                mf_uptime = mf_uptime - loop_duration
                trinket_uptime = trinket_uptime - loop_duration
                trinket_cd_timer = trinket_cd_timer - loop_duration
                eye_of_mag_uptime = eye_of_mag_uptime - loop_duration
                spellstrike_uptime = spellstrike_uptime - loop_duration
                eye_of_quagg_icd = eye_of_quagg_icd - loop_duration
                eye_of_quagg_uptime = eye_of_quagg_uptime - loop_duration
                sextant_of_unstable_currents_icd = sextant_of_unstable_currents_icd - loop_duration
                sextant_of_unstable_currents_uptime = sextant_of_unstable_currents_uptime - loop_duration
                ashtongue_uptime = ashtongue_uptime - loop_duration
                drum_time = drum_time - loop_duration
                drum_cd = drum_cd - loop_duration
                lust_uptime = lust_uptime - loop_duration
                skull_uptime = skull_uptime - loop_duration
                skull_cd = skull_cd - loop_duration
                # Check the timer on buffs / debuffs                
                if spellstrike_uptime <= 0:
                    spellstrike_proc = False
                
                if mf_uptime <= 0:
                    is_mf_up = False
                if ff_uptime <= 0:
                    is_ff_up = False
                # Trinket 
                if trinket_uptime <= 0:
                    is_trinket_active = False
                else:
                    is_trinket_active = True
                if trinket_cd_timer <= 0:
                    is_trinket_available = True
                else:
                    is_trinket_available = False

                if eye_of_quagg_uptime <= 0 and eye_of_quagg_proc:
                    fight_haste = fight_haste - (320/15.77)
                    eye_of_quagg_proc = False 
                    self.logfunc("eye of quagg fades. fight haste is " + str(fight_haste))
                    
                if eye_of_mag_uptime <= 0:
                    is_eye_of_mag_triggered = False

                if sextant_of_unstable_currents_uptime <= 0:
                    is_sextant_of_unstable_currents_triggered = False

                if ashtongue_uptime <= 0:
                    is_ashtongue_triggered = False
                    
                if self.buffs.is_drums and drum_time <= 0 and drums_up:
                    fight_haste = fight_haste - (80/15.77)
                    drums_up = False
                    #self.logfunc("drums down!!! fight haste is: " + str(fight_haste))
                    
                if lusted and lust_uptime <= 0:
                    fight_haste = fight_haste - 30
                    lusted = False
                    #self.logfunc("lust down!")
                    
                if skull_active and skull_uptime <= 0:
                    fight_haste = fight_haste - (175/15.77)
                    skull_active = False
                    #self.logfunc("skull deactivated !!")
                    
                # Update nature's grace
                if is_crit:
                    if self.char.sextant_of_unstable_currents and rng.randint(1, high = 6, size = 1) == 5 and sextant_of_unstable_currents_icd <= 0:
                        is_sextant_of_unstable_currents_triggered = True
                        sextant_of_unstable_currents_uptime = 15
                        sextant_of_unstable_currents_icd = sextant_icd
                        self.logfunc("Sextant proc!")
                    is_ng = True

                total_damage_done = total_damage_done + damage * self.buffs.curse_of_elements * self.buffs.misery

                # If there is a Hit, Check if spellstrike / Quag'eye is proc or refreshed :
                if is_hit: 
                    if self.char.is_spellstrike and rng.randint(1, high = 11, size = 1) == 10:
                        spellstrike_proc = True
                        spellstrike_uptime = 10
                        self.logfunc("Spellstrike proc !!!")
                    if self.char.quagmirran and rng.randint(1, high = 11, size = 1) == 10 and eye_of_quagg_icd <= 0:
                        eye_of_quagg_proc = True
                        eye_of_quagg_uptime = 6
                        eye_of_quagg_icd = 45
                        fight_haste = fight_haste + (320/15.77)
                        self.logfunc("Eye of Quagmirran proc !!!, fight haste is: "+ str(fight_haste)) 
                        
                # If there is a resist, check eye of mag proc :
                if self.char.eye_of_mag and not is_hit:
                    is_eye_of_mag_triggered = True
                    eye_of_mag_uptime = 10
                    self.logfunc("Eye of mag proc !!!")

                # Print output
                self.logfunc("Loop Duration : " + str(loop_duration))
                self.logfunc("Loop Damage : " + str(damage))
     
            self.logfunc("Overall damage done : " + str(total_damage_done))
            self.logfunc("Overall DPS : "  + str(total_damage_done/fight_time)) # We use fight_time here in case SF lands after the fight_length mark
            average_dps = average_dps + (total_damage_done/fight_time)
     
        real_average_dps = average_dps / iteration_nb
        self.logfunc("Average DPS : " + str(real_average_dps))
        return(real_average_dps)

def main():
    # define buffs
    print("Setup buffs ...")
    buffs = Buffs_list(is_twilight_owl = False,
    is_eye_of_night = False,
    is_T5 = False,
    is_T6_2 = False,
    is_T6_4 = False)
    
    # define stuff
    print("Setup stuff ...")
    toon = Character(intel = 400,
    crit_score = 200,
    hit_score = 110,
    spellpower = 1100,
    haste = 0,
    spirit = 187,
    is_csd = True,
    is_spellstrike = False,
    is_spellfire = True,
    trinket1 = "Xiri's Gift",
    trinket2 = "Ashtongue Talisman of Equilibrium")
    toon.set_talents()
    print(buffs)
    
    # define encounter
    print("Setup encounter ...")
    fight = Encounter(toon, buffs, 180)
    
    # launch sim
    print("Launch the sim ...")
    average_dps = fight.compute_dps(1)
    print("Average DPS computed : " + str(average_dps))
    
 
if __name__ == "__main__":
    main()
   
    