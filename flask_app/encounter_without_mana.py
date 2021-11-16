import math
import numpy
from . import buffs_list
from . import character

class Encounter_without_mana:
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
		self.output_logs = ""
	
	def parse_rotation(self):
		pass
	
	def logfunc(self, s):
		is_log_on = True
		if is_log_on:
			self.output_logs = self.output_logs + "\n" + s
	def logmana(self, s):
		is_log_on = False
		if is_log_on:
			self.output_logs = self.output_logs + "\n" + s
			
	def compute_dps(self, iteration_nb = 1):
		#Paddington - Added toggling of spells
		casting_SF = True
		casting_wrath = False
		SF_rank = 8
		is_MF = True
		is_IS = False

		rng = numpy.random.RandomState()
		#rng = numpy.random.RandomState(26082019)
		buff_dict = self.buffs.get_stats_buffs()
		intel = self.char.intel + buff_dict.get("intel") 
		crit_score = self.char.crit_score + buff_dict.get("crit_score") + 40.665 # value from character sheet
		hit_score = self.char.hit_score + buff_dict.get("hit_score")
		spellpower = self.char.spellpower + buff_dict.get("spellpower")
		self.logfunc("Character Sheet spellpower : " + str(spellpower))
		haste = self.char.haste + buff_dict.get("haste")
		spirit = self.char.spirit + buff_dict.get("spirit")
		mp5 = buff_dict.get("mp5")
		is_idol_of_moongoddess = True if self.char.idol == "Idol of the Moongoddess" else False
		if self.char.idol == "Idol of the Raven Goddess":
			crit_score = crit_score + 20
		self.logfunc("Crit score is : " + str(crit_score))
		
		trinket_one = self.char.trinket_one
		trinket_two = self.char.trinket_two
		self.logfunc("Trinkets : " + str(trinket_one) + " --- " + str(trinket_two))
		if trinket_one.is_eye_of_mag() or trinket_two.is_eye_of_mag():
			self.logfunc("One trinket is Eye of Mag")
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
		
		#MF_average_damage = 331
		
		MF_average_damage = 397.5
		if self.buffs.is_T6_2:
			MF_average_dot_damage = 720
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
		
		self.logfunc("After Lunar Guidance spellpower : " + str(spellpower))
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
		
		wrath_crit_percent =  crit_score/22.1 + intel/79.4 +  + self.char.moonkin_form + self.char.focused_starlight 
		wrath_crit_percent_value = wrath_crit_percent / 100
		self.logfunc("Wrath crit chance is : " + str(wrath_crit_percent))
		
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
		
		# New added spells
		IS_coeff = 0.76
		# IS_mana_cost = 175
		IS_average_dot_damage = 792
		
		wrath_coeff = 0.671
		# wrath_mana_cost = 232
		wrath_average_damage = 448.5
		wrath_cast_time = 1.5
		wrath_cast_time_ng = 1
		
		partial_coeff = 0.94 # For the moment, let's say that in average, partials get 6% damage reduction
		
		#Paddington - Added spell downranking
		if SF_rank == 6:
		#	SF_mana_cost = 287
			SF_average_damage = 553.5
		elif SF_rank == 7:
		#	SF_mana_cost = 309
			SF_average_damage = 614.5
		else:
		#	SF_mana_cost = 337
			SF_average_damage = 658
		
		# SF_average_damage = SF_average_damage + 55 if is_idol_of_moongoddess else SF_average_damage
		
		# T6 bonus
		if self.buffs.is_T6_2:
			MF_average_dot_damage = 720
		else:
			MF_average_dot_damage = 600
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
			trinket_one_duration = 0
			trinket_one_cd = 0
			trinket_shared_cd = 0
			trinket_two_duration = 0
			trinket_two_cd = 0
			trinket_one_active = False
			trinket_two_active = False
			Mag_Triggered = False
			ff_uptime = 0
			mf_uptime = 0
			trinket_uptime = 0
			trinket_cd_timer = 0
			is_trinket_active = False
			
			wrath_fight_value = wrath_crit_percent_value
			sf_fight_value = SF_crit_percent_value
			mf_fight_value = MF_crit_percent_value
			destro_duration = 0
			destro_active = False
			
			#Paddington - Added on-use trinket internal cooldown
			on_use_icd_timer = 0
			#Paddington - Added Insect Swarm
			is_is_up = False
		
			is_trinket_available = True
			is_ff_up = False
			is_mf_up = False
			is_ng = False
			is_eye_of_mag_triggered = False
			is_sextant_of_unstable_currents_triggered = False
			Ashtongue_Triggered = False
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
			is_uptime = 0
			lust_start = 1 - (lust_when/100)
			is_lusted = False
			loopcount = 0
			fight_haste = spell_haste
			fight_spell_power = spellpower
			
			#Paddington - Added individual spell damage totals
			SF_damage = 0
			MF_damage = 0
			IS_damage = 0
			Wrath_damage  = 0
			#Treant_damage = 0
			SF_hit = False
			MF_hit = False
			IS_hit = False
			Wrath_hit = False
			is_trinket_activable = self.char.is_trinket_activable

			while fight_time <= self.fight_length:
				if is_lusted:
					loop_duration = max(1, (1.5 / (1 + (fight_haste / 100))/1.3)) #GCD - can't be less, it's the rule !
				else:
					loop_duration = max(1, (1.5 / (1 + (fight_haste / 100)))) #GCD - can't be less, it's the rule !
				damage = 0
				# adding a variable to keep the initial spellpower to revert to this value in case a trinket bonus
				# fades out before the end of the SF / Wrath cast (ie. no spellpower snapshot)
				loop_start_spellpower = spellpower
				if spellstrike_proc:
					fight_spell_power = spellpower + spellstrike_bonus
			   
				# if is_eye_of_mag_triggered:
				# 	fight_spell_power = fight_spell_power + 170  
				# 
				# if is_sextant_of_unstable_currents_triggered:
				# 	fight_spell_power = spellpower + 190
				# 
				# if is_ashtongue_triggered:
				# 	fight_spell_power = spellpower + 150
				
				if self.buffs.is_drums and drum_cd <= 0:
					drum_time = 30
					drum_cd = 120
					drums_up = True
					fight_haste = fight_haste + (80/15.77)
					self.logfunc(" drums up !!! fight haste is " + str(fight_haste))
					
				if self.buffs.is_lust and lust_amount >= 1 and fight_time >= (lust_start * self.fight_length) and is_lusted == False:
					lust_amount = lust_amount - 1
					lust_uptime = 40
					is_lusted = True
					
				# if FF not up, cast FF
				#Paddington - Added mana management
				# self.logfunc("Is FF UP ? : " + str(is_ff_up))
				if not is_ff_up:
					self.logfunc("Casting Faerie Fire !")
					#Paddington - Added mana management
					if is_lusted:
						loop_duration = max(1, ((1.5 / (1 + (fight_haste/100)))/1.3)) #GCD
					else:
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
					# Trinkets before applying damage
					if trinket_one.ttype == "Active" and trinket_one_cd <= 0 and trinket_one.shared and trinket_shared_cd <= 0 and trinket_one.effect == "SP":
						self.logfunc("fight spell power is " + str(fight_spell_power))
						fight_spell_power = fight_spell_power + trinket_one.effect_amount
						trinket_one_duration = trinket_one.duration
						trinket_one_cd = trinket_one.cd
						trinket_shared_cd = trinket_one.sharedcd
						trinket_one_active = True
						self.logfunc("Trinket one active! fight spell power is " + str(fight_spell_power) + " Trinket cd " + str(trinket_one.cd) + " shared cd " + str(trinket_one.sharedcd) )
					
					if trinket_one.ttype == "Active" and trinket_one_cd <= 0 and trinket_one.shared and trinket_shared_cd <= 0 and trinket_one.effect == "Haste":
						fight_haste = fight_haste + (trinket_one.effect_amount/15.77)
						trinket_one_duration = trinket_one.duration
						trinket_one_cd = trinket_one.cd
						trinket_shared_cd = trinket_one.sharedcd
						trinket_one_active = True
						self.logfunc("trinket one active! haste " + str(fight_haste))
				
					if self.buffs.is_destruction_potion and manapot_cd <= 0:
						fight_spell_power = fight_spell_power + 120
						wrath_fight_value = wrath_fight_value + .02
						sf_fight_value = sf_fight_value + .02
						mf_fight_value = mf_fight_value + .02
						destro_duration = 15
						manapot_cd = 120
						destro_active = True
						self.logfunc("destruction pot used! sp " + str(fight_spell_power) + " wrath crit " + str(wrath_fight_value) + " sf crit " + str(sf_fight_value) + " mf crit " + str(mf_fight_value))
					
					#setup for the second trinket slot
					if trinket_two.ttype == "Active" and trinket_two_cd <= 0 and trinket_two.shared and trinket_shared_cd <= 0 and trinket_two.effect == "SP":
						fight_spell_power = fight_spell_power + trinket_two.effect_amount
						trinket_two_duration = trinket_two.duration
						trinket_two_cd = trinket_two.cd
						trinket_shared_cd = trinket_two.sharedcd
						trinket_two_active = True
						self.logfunc("trinket two active! spellpower " +  str(fight_spell_power))
		
					if trinket_two.ttype == "Active" and trinket_two_cd <= 0 and trinket_two.shared and trinket_shared_cd <= 0 and trinket_two.effect == "Haste":
						fight_haste = fight_haste + (trinket_two.effect_amount/15.77)
						trinket_two_duration = trinket_two.duration
						trinket_two_cd = trinket_two.cd
						trinket_shared_cd = trinket_two.sharedcd
						trinket_two_active = True
						self.logfunc("trinket two active! haste " + str(fight_haste))
					
					
					if not is_mf_up and is_MF:
						self.logfunc("Casting Moonfire !")
						if is_lusted:
							loop_duration = max(1, ((1.5 / (1 + (fight_haste/100)))/1.3)) #GCD
						else:
							loop_duration = max(1, (1.5 / (1 + (fight_haste/100)))) #GCD
						# Is it a hit ?
						if(rng.random() <= hit_chance_percent_value):
							is_hit = True
							MF_hit = True								  
							# Is it a crit ?
							is_crit = (rng.random() <= MF_crit_percent_value)
							# Is it a partial ?
							#if(rng.randint(1, high = 101, size = 1) <= hit_chance):
							#	damage = MF_average_damage + MF_coeff * fight_spell_power * partial_coeff
							damage = (MF_average_damage + (MF_coeff * fight_spell_power)) * self.char.moonfury * self.char.imp_mf * self.buffs.curse_of_elements * self.buffs.misery
							# Apply damage
							if is_crit:
								damage = damage * crit_coeff
				
							# self.logfunc("Moonfire base damange :" + str(damage))
							# DoT :
							if self.buffs.is_T6_2:
								damage = damage + ((MF_average_dot_damage + (MF_coeff_dot * fight_spell_power) * min(15, (self.fight_length - fight_time - 1.5))/15) * self.char.moonfury * self.char.imp_mf * self.buffs.curse_of_elements * self.buffs.misery)
								# self.logfunc("Damage done (T6_2): " + str(damage))
							else:
								damage = damage + ((MF_average_dot_damage + (MF_coeff_dot * fight_spell_power) * min(12, (self.fight_length - fight_time - 1.5))/12)* self.char.moonfury * self.char.imp_mf * self.buffs.curse_of_elements * self.buffs.misery)
								# self.logfunc("Damage done : " + str(damage))

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
							
					#Paddington - Added insect swarm use
					elif not is_is_up and is_IS :
						self.logfunc("Casting Insect Swarm !")
						if is_lusted:
							loop_duration = max(1, ((1.5 / (1 + (fight_haste/100)))/1.3)) #GCD
						else:
							loop_duration = max(1, (1.5 / (1 + (fight_haste/100)))) #GCD because we cast a spell
						# Is it a hit ?
						if(rng.random() <= hit_chance_percent_value):
							is_hit = True
							#Paddington - Added hit check for individual spell dmg totals
							IS_hit = True										   
							# DoT :
							damage = damage + ((IS_average_dot_damage + (IS_coeff * fight_spell_power) * min(12, (self.fight_length - fight_time - 1.5))/12) * self.buffs.misery)
							# There is a Hit ! update model
							is_is_up = True
							is_uptime = 12
						else:
							is_hit = False
							self.logfunc("Insect Swarm -> Resist ! ")
							
					#Paddington - Added wrath option here   
					#Paddington - Added mana management		 
					elif casting_wrath :
						# Cast Wrath
						self.logfunc("Casting Wrath !")
						# Is it a hit ?
						if(rng.randint(1, high = 101, size = 1) <= hit_chance):
							is_hit = True
							#Paddington - Added hit check for individual spell dmg totals
							Wrath_hit = True
							# Is it a crit ?
							is_crit = (rng.randint(1, high = 101, size = 1) <= wrath_crit_percent)
							damage = (wrath_average_damage + (wrath_coeff * fight_spell_power * self.char.wrath_of_cenarius_wrath )) * self.char.moonfury * self.buffs.misery
							if is_crit:
								damage = damage * crit_coeff
							self.logfunc("Damage done : " + str(damage))
						else:
							is_hit = False
							self.logfunc("Wrath -> Resist ! ")
						
						if is_ng and is_lusted:
							wrath_cast_time_ng = max(1, ((1 / (1 + (fight_haste/100)))/1.3))
							loop_duration = max(1, wrath_cast_time_ng)
						elif is_lusted:
							wrath_cast_time = max(1, ((1.5 / (1 + (fight_haste/100)))/1.3))
							loop_duration = max(1, wrath_cast_time)
						elif is_ng:
							wrath_cast_time_ng = max(1, (1 / (1 + (fight_haste/100))))
							loop_duration = max(1, wrath_cast_time_ng)
						else:
							wrath_cast_time = max(1, (1.5 / (1 + (fight_haste/100))))
							loop_duration = max(1, wrath_cast_time)
						is_ng = False # Consume NG once wrath is cast

					#Paddington - Added mana management
					elif casting_SF :
						# Cast Starfire
						self.logfunc("Casting Starfire !")
						# self.logfunc("Is HEROISM still UP ? : " + str(is_lusted))
						if is_ng and is_lusted:
							sf_cast_time_ng = max(1, ((2.5 / (1 + (fight_haste/100)))/1.3))
							loop_duration = max(1, sf_cast_time_ng)
							sf_cast_time = sf_cast_time_ng # sf_cast_time is necessary later in the code
						elif is_lusted:
							sf_cast_time = max(1, ((3 / (1 + (fight_haste/100)))/1.3))
							loop_duration = max(1, sf_cast_time)
						elif is_ng:
							sf_cast_time_ng = max(1, (2.5 / (1 + (fight_haste/100))))
							loop_duration = max(1, sf_cast_time_ng)
							sf_cast_time = sf_cast_time_ng
						else:
							sf_cast_time = max(1, (3 / (1 + (fight_haste/100))))
							loop_duration = max(1, sf_cast_time)
						is_ng = False # Consume NG once SF is cast  
						# self.logfunc("Starfire fight_haste value : " + str(fight_haste))
						# Is it a hit ?
						# if(rng.randint(1, high = 101, size = 1) <= hit_chance):
						if(rng.random() <= hit_chance_percent_value):
							is_hit = True
							#Paddington - Added hit check for individual spell dmg totals
							SF_hit = True
							if trinket_one.is_ashtongue() and rng.randint(1, high = 101, size = 1) <= 25 and Ashtongue_Triggered == False:
								trinket_one_active = True
								fight_spell_power = fight_spell_power + trinket_one.effect_amount
								trinket_one_duration = trinket_one.duration
								self.logfunc("fresh ashtongue trigger. spellpower " + str(fight_spell_power) + " fight_time " + str(fight_time))
								Ashtongue_Triggered = True
		
							elif trinket_one.is_ashtongue() and rng.randint(1, high = 101, size = 1) <= 25 and Ashtongue_Triggered == True:
								trinket_one_duration = trinket_one.duration
								self.logfunc("ashtongue refresh spellpower " + str(fight_spell_power) + " fight_time " + str(fight_time))

							if trinket_two.is_ashtongue() and rng.randint(1, high = 101, size = 1) <= 25 and Ashtongue_Triggered == False:
								trinket_two_active = True
								fight_spell_power = fight_spell_power + trinket_two.effect_amount
								trinket_two_duration = trinket_two.duration
								self.logfunc("fresh ashtongue trigger. spellpower " + str(fight_spell_power) + " fight_time " + str(fight_time))
								Ashtongue_Triggered = True
	
							elif trinket_two.is_ashtongue() and rng.randint(1, high = 101, size = 1) <= 25 and Ashtongue_Triggered == True:
								trinket_two_duration = trinket_two.duration
								self.logfunc("ashtongue refresh spellpower " + str(fight_spell_power) + " fight_time " + str(fight_time))
							
							
							# if self.char.ashtongue_talisman and rng.randint(1, high = 5, size = 1) == 1:
							# 	is_ashtongue_triggered = True
							# 	ashtongue_uptime = 8
							# 	self.logfunc("Ashtongue Proc !!")
							
							# Is it a crit ?
							is_crit = (rng.random() <= SF_crit_percent_value)
							if is_crit:
								self.logfunc("Starfire -> Crit ! ")
							
							if spellstrike_proc and (spellstrike_uptime < loop_duration):
								fight_spell_power = fight_spell_power - spellstrike_bonus 
								#self.logfunc("Spellstrike fades out to early ...")
								
							if trinket_one.is_ashtongue() and trinket_one_active and trinket_one_duration <= loop_duration: 
								self.logfunc("fight spellpower + " + str(fight_spell_power))
								fight_spell_power = fight_spell_power - trinket_one.effect_amount
								trinket_one_active = False
								#self.logfunc("ashtongue fades early fight spellpower + " + str(fight_spell_power))
								Ashtongue_Triggered = False
							
							elif trinket_one.is_eye_of_mag() and trinket_one_active and trinket_one_duration <= loop_duration: 
								#self.logfunc("fight spellpower + " + str(fight_spell_power))
								fight_spell_power = fight_spell_power - trinket_one.effect_amount
								trinket_one_active = False
								#self.logfunc("Eye of Mag fades early fight spellpower + " + str(fight_spell_power))
								Mag_Triggered = False
			
							elif trinket_one_active and trinket_one_duration <= loop_duration and  trinket_one.effect == "SP":
								# self.logfunc("fight spellpower + " + str(fight_spell_power))
								fight_spell_power = fight_spell_power - trinket_one.effect_amount
								trinket_one_active = False
								#self.logfunc("trinket fades early fight spellpower + " + str(fight_spell_power))
				
							if trinket_two.is_ashtongue() and trinket_two_active and trinket_two_duration <= loop_duration:
								# self.logfunc("fight spellpower " + str(fight_spell_power))
								fight_spell_power = fight_spell_power - trinket_two.effect_amount
								trinket_two_active = False
								#self.logfunc("ashtongue fades early fight spellpower + " + str(fight_spell_power))
								Ashtongue_Triggered = False
							
							elif trinket_two.is_eye_of_mag() and trinket_two_active and trinket_two_duration <= loop_duration:
								# self.logfunc("eye of mag fades early fight spellpower + " + str(fight_spell_power))
								fight_spell_power = fight_spell_power - trinket_two.effect_amount
								trinket_two_active = False
								#self.logfunc("trinket fades early fight spellpower + " + str(fight_spell_power))
								Mag_Triggered = False
							
							elif trinket_two_active and trinket_two_duration <= loop_duration and  trinket_two.effect == "SP":
								fight_spell_power = fight_spell_power - trinket_two.effect_amount
								trinket_two_active = False
								#self.logfunc("trinket fades early fight spellpower + " + str(fight_spell_power))
							
							#if self.buffs.is_destruction_potion and not self.buffs.is_manapot and destro_duration <= loop_duration and destro_active:
							#	fight_spell_power = fight_spell_power - 120
							#	wrath_fight_value = wrath_fight_value -.02
							#	sf_fight_value = sf_fight_value - .02
							#	mf_fight_value = mf_fight_value - .02
							#	#self.logfunc("destruction fades out early! sp " + str(fight_spell_power) + " wrath crit " + str(wrath_fight_value) + " sf crit " + str(sf_fight_value) + " mf crit " + str(mf_fight_value))
							#	destro_active = False
								

							# end of trinket verification
							#Paddington - Added check for Insect Swarm
							if self.buffs.is_T5 and is_ng and mf_uptime >= sf_cast_time_ng and is_uptime >= sf_cast_time_ng:
								damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius_starfire )) * self.char.moonfury * 1.1  * self.buffs.curse_of_elements * self.buffs.misery						  
							elif self.buffs.is_T5 and mf_uptime >= sf_cast_time:
								damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius_starfire )) * self.char.moonfury * 1.1  * self.buffs.curse_of_elements * self.buffs.misery					  
							elif self.buffs.is_T5 and is_uptime >= sf_cast_time:
								damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius_starfire )) * self.char.moonfury * 1.1 * self.buffs.curse_of_elements * self.buffs.misery
							else:
								damage = (SF_average_damage + (SF_coeff * fight_spell_power * self.char.wrath_of_cenarius_starfire )) * self.char.moonfury * self.buffs.curse_of_elements * self.buffs.misery						   
								# self.logfunc("Damage formula : " + str(SF_average_damage) + " + (" + str(SF_coeff) + " x " + str(fight_spell_power) + " x " + str(self.char.wrath_of_cenarius) + ")) x "  +
								# str(self.char.moonfury ) + " x " + str(self.buffs.curse_of_elements) + " x " + str(self.buffs.misery) )
							if is_crit:
								damage = damage * crit_coeff
								# self.logfunc("Damage done : " + str(damage))
						else:
							is_hit = False
							self.logfunc("Starfire -> Resist ! ")

						
						#Treant_damage = 0
						#Individual spell damage totals
						if SF_hit:
							SF_damage = SF_damage + damage
							SF_hit = False

						if MF_hit:
							MF_damage = MF_damage + damage
							MF_hit = False

						if IS_hit:
							IS_damage = IS_damage + damage
							IS_hit = False
	  
						if Wrath_hit:
							Wrath_damage = Wrath_damage + damage
							Wrath_hit = False
						
				# Apply partials in the end, once and for all
				damage = damage * partial_coeff
				# Update time and model
				fight_time = fight_time + loop_duration
				self.logfunc("Fight Time until now : " + str(fight_time))
				ff_uptime = ff_uptime - loop_duration
				mf_uptime = mf_uptime - loop_duration
				is_uptime = is_uptime - loop_duration
				# trinket_uptime = trinket_uptime - loop_duration
				# trinket_cd_timer = trinket_cd_timer - loop_duration
				trinket_one_duration = trinket_one_duration - loop_duration
				trinket_one_cd = trinket_one_cd - loop_duration
				trinket_two_duration = trinket_two_duration - loop_duration
				trinket_two_cd = trinket_two_cd - loop_duration
				trinket_shared_cd = trinket_shared_cd - loop_duration
				destro_duration = destro_duration - loop_duration
				#Paddington - Added Internal CD for on-use trinkets
				# on_use_icd_timer = on_use_icd_timer - loop_duration
				# eye_of_mag_uptime = eye_of_mag_uptime - loop_duration
				spellstrike_uptime = spellstrike_uptime - loop_duration
				# eye_of_quagg_icd = eye_of_quagg_icd - loop_duration
				# eye_of_quagg_uptime = eye_of_quagg_uptime - loop_duration
				# sextant_of_unstable_currents_icd = sextant_of_unstable_currents_icd - loop_duration
				# sextant_of_unstable_currents_uptime = sextant_of_unstable_currents_uptime - loop_duration
				# ashtongue_uptime = ashtongue_uptime - loop_duration
				drum_time = drum_time - loop_duration
				drum_cd = drum_cd - loop_duration 
				
				lust_uptime = lust_uptime - loop_duration
				######################
				skull_uptime = skull_uptime - loop_duration
				skull_cd = skull_cd - loop_duration
				# Check the timer on buffs / debuffs				
				if spellstrike_uptime <= 0:
					spellstrike_proc = False
				
				
				
				if mf_uptime <= 0:
					is_mf_up = False
				
				if self.buffs.is_drums and drum_time <= 0 and drums_up:
					fight_haste = fight_haste - (80/15.77)
					drums_up = False
					self.logfunc("drums down!!! fight haste is: " + str(fight_haste))
				
				if trinket_one.is_ashtongue() and trinket_one_duration <= 0 and trinket_one_active and trinket_one.effect == "SP":
					fight_spell_power = fight_spell_power - trinket_one.effect_amount
					trinket_one_active = False
					#self.logfunc("ashtongue fades fight spellpower + " + str(fight_spell_power))
					Ashtongue_Triggered = False
				
				elif trinket_one.is_eye_of_mag() and trinket_one_duration <= 0 and trinket_one_active and trinket_one.effect == "SP":
					fight_spell_power = fight_spell_power - trinket_one.effect_amount
					trinket_one_active = False
					#self.logfunc("Eye of Mag Fades fight spellpower + " + str(fight_spell_power))
					Mag_Triggered = False
					
				elif trinket_one_duration <= 0 and trinket_one_active and trinket_one.effect == "SP":
					fight_spell_power = fight_spell_power - trinket_one.effect_amount
					trinket_one_active = False
					#self.logfunc("trinket one fades. fight spellpower + " + str(fight_spell_power))
					
				elif trinket_one_duration <= 0 and trinket_one_active and trinket_one.effect == "Haste":
					fight_haste = fight_haste - (trinket_one.effect_amount/15.77)
					trinket_one_active = False
					#self.logfunc("trinket one fades. fight haste " + str(fight_haste))
				
				if trinket_two.is_ashtongue() and trinket_two_duration <= 0 and trinket_two_active and trinket_two.effect == "SP":
					fight_spell_power = fight_spell_power - trinket_two.effect_amount
					trinket_two_active = False
					#self.logfunc("ashtongue two fight spellpower + " + str(fight_spell_power))
					Ashtongue_Triggered = False
					
				elif trinket_two.is_eye_of_mag() and trinket_two_duration <= 0 and trinket_two_active and trinket_two.effect == "SP":
					fight_spell_power = fight_spell_power - trinket_two.effect_amount
					trinket_one_active = False
					#self.logfunc("eye of mag fades early. fight spellpower + " + str(fight_spell_power))
					Mag_Triggered = False				
				
				elif trinket_two_duration <= 0 and trinket_two_active and trinket_two.effect == "SP":
					fight_spell_power = fight_spell_power - trinket_two.effect_amount
					#self.logfunc("trinket two fades. fight spellpower + " + str(fight_spell_power))
					trinket_two_active = False
					
				elif trinket_two_duration <= 0 and trinket_two_active and trinket_two.effect == "Haste":
					fight_haste = fight_haste - (trinket_two.effect_amount/15.77)
					trinket_two_active = False
					#self.logfunc("trinket two fades. fight haste" + str(fight_haste))
				
				if self.buffs.is_destruction_potion and destro_duration <= 0 and destro_active:
					fight_spell_power = fight_spell_power - 120
					wrath_fight_value = wrath_fight_value -.02
					sf_fight_value = sf_fight_value - .02
					mf_fight_value = mf_fight_value - .02
					#self.logfunc("destruction fades sp " + str(fight_spell_power) + " wrath crit " + str(wrath_fight_value) + " sf crit " + str(sf_fight_value) + " mf crit " + str(mf_fight_value))
					destro_active = False
				
				if ff_uptime <= 0:
					is_ff_up = False
			
					
				if is_lusted and lust_uptime <= 0:
					is_lusted = False
					#logfunc("lust down!")
					
				# if skull_active and skull_uptime <= 0:
				# 	fight_haste = fight_haste - (175/15.77)
				# 	skull_active = False
				# 	#logfunc("skull deactivated !!")
					
				# Update nature's grace
				if is_crit:
					# if self.char.sextant_of_unstable_currents and rng.randint(1, high = 6, size = 1) == 5 and sextant_of_unstable_currents_icd <= 0:
					# 	is_sextant_of_unstable_currents_triggered = True
					# 	sextant_of_unstable_currents_uptime = 15
					# 	sextant_of_unstable_currents_icd = sextant_icd
					# 	self.logfunc("Sextant proc!")
					if trinket_one.is_sextant()and trinket_one_cd <= 0 and rng.randint(1, high = 6, size = 1) == 1:
						fight_spell_power = fight_spell_power + trinket_one.effect_amount
						trinket_one_duration = trinket_one.duration
						trinket_one_cd = trinket_one.cd
						trinket_one_active = True
						self.logfunc("sextant active! spellpower " + str(fight_spell_power))
		
					if trinket_two.is_sextant()and trinket_two_cd <= 0 and rng.randint(1, high = 6, size = 1) == 1:
						fight_spell_power = fight_spell_power + trinket_two.effect_amount
						trinket_two_duration = trinket_two.duration
						trinket_two_cd = trinket_two.cd	  
						trinket_two_active = True
						self.logfunc("sextant active! spellpower " + str(fight_spell_power))
						
					is_ng = True

				total_damage_done = total_damage_done + damage 

				# If there is a Hit, Check if spellstrike / Quag'eye is proc or refreshed :
				if is_hit: 
					if self.char.is_spellstrike and rng.randint(1, high = 11, size = 1) == 10:
						spellstrike_proc = True
						spellstrike_uptime = 10
						self.logfunc("Spellstrike proc !!!")
					#if self.char.quagmirran and rng.randint(1, high = 11, size = 1) == 10 and eye_of_quagg_icd <= 0:
					#	eye_of_quagg_proc = True
					#	eye_of_quagg_uptime = 6
					#	eye_of_quagg_icd = self.char.trinket_icd
					#	fight_haste = fight_haste + (320/15.77)
					#	self.logfunc("Eye of Quagmirran proc !!!, fight haste is: "+ str(fight_haste)) 
					if trinket_one.is_quag_eye() and trinket_one_cd <= 0 and rng.randint(1, high = 11, size = 1) == 1:
						fight_haste = fight_haste + (trinket_one.effect_amount/15.77)
						self.logfunc("quags eye procced! " + str(fight_haste))
						trinket_one_duration = trinket_one.duration
						trinket_one_cd = trinket_one.cd
						trinket_one_active = True
						self.logfunc("trinket cd timer" + str(trinket_one_cd))
	
					if trinket_two.is_quag_eye() and trinket_two_cd <= 0 and rng.randint(1, high = 11, size = 1) == 1:
						fight_haste = fight_haste + (trinket_two.effect_amount/15.77)
						self.logfunc("quags eye procced! " + str(fight_haste))
						trinket_two_duration = trinket_two.duration
						trinket_two_cd = trinket_two.cd
						trinket_two_active = True
						self.logfunc("trinket cd timer" + str(trinket_two_cd))
					
				if not is_hit:
					if trinket_one.is_eye_of_mag() and Mag_Triggered == False:
						fight_spell_power = fight_spell_power + trinket_one.effect_amount
						trinket_one_active = True
						trinket_one_duration = trinket_one.duration
						Mag_Triggered = True
						self.logfunc("Eye of Mag Triggered! Time remaining " + str(trinket_one.duration) + " spell power "+ str(fight_spell_power))

					elif trinket_one.is_eye_of_mag() and Mag_Triggered == True:
						trinket_one_duration = trinket_one.duration
						self.logfunc("Eye of Mag refreshed! Time remaining " + str(trinket_one.duration))
						
					if trinket_two.is_eye_of_mag() and Mag_Triggered == False:
						fight_spell_power = fight_spell_power + trinket_two.effect_amount
						trinket_two_active = True
						trinket_two_duration = trinket_two.duration
						Mag_Triggered = True
						self.logfunc("Eye of Mag Triggered! Time remaining " + str(trinket_two.duration))

					elif trinket_two.is_eye_of_mag() and Mag_Triggered == False:
						trinket_two_duration = trinket_two.duration
						self.logfunc("Eye of Mag refreshed! Time remaining " + str(trinket_two.duration))
				
				# Print output
				self.logfunc("Loop Duration : " + str(loop_duration))
				self.logfunc("Loop Damage : " + str(damage))
				if damage > 0:
					loopcount = loopcount + 1
				
			#print("damage loops: ", loopcount)  Used to track how many loops actually do damage in a fight i.e. before mana runs out.
			self.logfunc("Overall damage done : " + str(total_damage_done))
			#Paddington - Added individual spell damage totals
			#print("Starfire damage : ", str(SF_damage))
			#print("Starfall DPS: ", SF_damage/fight_time)
			#print("Percent Starfall damage: ", (SF_damage/total_damage_done)*100)
			#print("Wrath damage : ", str(Wrath_damage))
			#print("Wrath DPS: ", Wrath_damage/fight_time)
			#print("Percent Wrath damage: ", (Wrath_damage/total_damage_done)*100)
			#print("Moonfire damage : ", str(MF_damage))
			#print("Moonfire DPS: ", MF_damage/fight_time)
			#print("Percent Moonfire damage: ", (MF_damage/total_damage_done)*100)
			#print("Insect Swarm damage : ", str(IS_damage))
			#print("Insect Swarm DPS: ", IS_damage/fight_time)
			#print("Percent Insect Swarm damage: ", (IS_damage/total_damage_done)*100)
			self.logfunc("Overall DPS : "  + str(total_damage_done/fight_time)) # We use fight_time here in case SF lands after the fight_length mark
			average_dps = average_dps + (total_damage_done/fight_time)
		
		#Paddington - Changed to average dps. Seems more accurate.
		real_average_dps = average_dps / iteration_nb
		self.logfunc("Average DPS : " + str(real_average_dps))
		return real_average_dps, self.output_logs

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
   
	