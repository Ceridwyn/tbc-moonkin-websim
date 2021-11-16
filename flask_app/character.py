class Trinket:
	def __init__(trinket, cd, ttype, shared, sharedcd,  duration, chance, effect, effect_amount):
		trinket.cd = cd
		trinket.ttype = ttype
		trinket.shared = shared
		trinket.sharedcd = sharedcd
		trinket.duration = duration
		trinket.chance = chance
		trinket.effect = effect
		trinket.effect_amount = effect_amount
		trinket.name = "undefined"
	
	def is_ashtongue(self):
		return self.name == "Ashtongue Talisman of Equilibrium"
	
	def is_eye_of_mag(self):
		return self.name == "Eye of Magtheridon"
	
	def is_quag_eye(self):
		return self.name == "Quagmirran's eye"
	
	def is_sextant(self):
		return self.name == "Sextant of the Unstable Currents"
		
	def __str__(self):
		return self.name

class Character:
	balance_of_power = True
	focused_starlight = True
	moonkin_form = True
	improved_mf = True
	starlight_wrath = True
	vengeance = True
	lunar_guidance = True
	moonfury = True
	wrath_of_cenarius = True
	intensity = 3
	
	trinket_duration = 0
	trinket_cd = 10000
	spellpower_trinket_bonus = 0
	
	def __init__(
	self,
	intel = 407,
	crit_score = 184,
	hit_score = 114,
	spellpower = 949,
	haste = 0,
	spirit = 187,
	is_csd = False, # Chaotic Skyfire Diamond equiped
	is_spellstrike = False,
	is_spellfire = False,
	trinket1 = "Icon of the Silver Crescent",
	trinket2 = "Quagmirran's Eye",
	idol = "none"):
		# Stats
		self.intel = intel
		self.crit_score = crit_score
		self.hit_score = hit_score
		self.spellpower = spellpower
		self.haste = haste
		self.spirit = spirit
		self.is_csd = is_csd # Chaotic Skyfire Diamond equiped
		self.is_spellstrike = is_spellstrike
		self.is_spellfire = is_spellfire
		self.idol = idol
		
		# Trinkets
		self.eye_of_mag = False # +54 SP + Grants 170 increased spell damage for 10 sec when one of your spells is resisted.
		self.silver_crescent = False # 43 SP + Use: Increases damage and healing done by magical spells and effects by up to 155 for 20 sec. (2 Min Cooldown)
		self.scryer_gem = False # 32 Hit rating + Use: Increases spell damage by up to 150 and healing by up to 280 for 15 sec. (1 Min, 30 Sec Cooldown)
		self.quagmirran = False # 37 SP + Equip: Your harmful spells have a chance to increase your spell haste rating by 320 for 6 secs. (Proc chance: 10%, 45s cooldown)
		self.essence_sapphi = False #  Use: Increases damage and healing done by magical spells and effects by up to 130 for 20 sec. (2 Min Cooldown)
		self.illidari_vengeance = False # +26 Crit . Use: Increases spell damage done by up to 120 and healing done by up to 220 for 15 sec. (1 Min, 30 Sec Cooldown)
		self.lightening_capacitor = False # Equip: You gain an Electrical Charge each time you cause a damaging spell critical strike.  When you reach 3 Electrical Charges, -> 750 dmg on average (2.5s ICD for charges, concern with wrath spam only)
		self.xiris_gift = False #  +32 crit / Use: Increases spell damage by up to 150 and healing by up to 280 for 15 sec. (1 Min, 30 Sec Cooldown)
		self.sextant_of_unstable_currents = False # +40 crit, Chance on critical strike to increase your spellpower by 190 for 15 seconds (20% proc chance, 45 second icd)
		self.ashtongue_talisman = False # Starfire has a 25% chance to grant you 150 spellpower for 8 seconds (25% proc chance, no icd)
		self.skull = False # +55 spellpower, +25 hit, 175 haste for 20 seconds on a 120 second cooldown. 
		self.shiffar = False # Chance on spell critical hit to increase your spell damage and healing by 225 for 10 secs. (Proc chance: 20%, 45s cooldown)
		self.is_trinket_activable = False
		self.dark_iron_smoking_pipe = False
		self.trinket_one = self.identify_trinket(trinket1)
		self.trinket_one.name = trinket1
		self.trinket_two = self.identify_trinket(trinket2)	
		self.trinket_two.name = trinket2
	

	def identify_trinket(self, trinket):
		if trinket == "Icon of the Silver Crescent":
			return(Trinket(120, "Active", True, 20, 20, 0, "SP", 155)) #tested
		if trinket == "Dark Iron Smoking Pipe":
			return(Trinket(120, "Active",  True, 20, 20, 0, "SP", 155)) #tested
		elif trinket == "Eye of Magtheridon":
			return(Trinket(0, "Proc", False, 0, 10, 0, "SP", 170)) #tested
		elif trinket == "Scryer's Bloodgem":
			return(Trinket(90, "Active", True, 15, 15, 0, "SP", 150)) #tested
		elif trinket == "Quagmirran's eye":
			return(Trinket(45, "Proc", False, 0, 6, 0, "Haste", 320)) #tested
		elif trinket == "The Restrained Essence of Sapphiron":
			return(Trinket(120, "Active", True, 20, 20, 0, "SP", 130)) #tested
		elif trinket == "Vengeance of the Illidari":
			return(Trinket(90, "Active", True, 15, 15, 0, "SP", 120)) # tested
		elif trinket == "The Lightning Capacitor":
			return(Trinket(0, "Proc", False, 0, 0, 0, "SP", 0)) #tested
		elif trinket == "Xiri's Gift":
			return(Trinket(90, "Active", True, 15, 15, 0, "SP", 150)) #tested
		elif trinket == "Sextant of the Unstable Currents":
			return(Trinket(45, "Proc", False, 0, 15, 0, "SP", 190)) #tested
		elif trinket == "Ashtongue Talisman of Equilibrium":
			return(Trinket(0, "Proc", False, 0, 8, 25, "SP", 150)) #tested
		elif trinket == "The Skull of Gul'dan":
			return(Trinket(120, "Active", True, 20, 20, 0, "Haste", 175)) #tested
		elif trinket == "Shiffar's Nexus-Horn":
			return(Trinket(45, "Proc", False, 0, 10, 0, "SP", 225)) #TODO
		# trinket.cd = cd
		# trinket.ttype = ttype
		# trinket.shared = shared
		# trinket.sharedcd = sharedcd
		# trinket.duration = duration
		# trinket.chance = chance
		# trinket.effect = effect
		# trinket.effect_amount = effect_amount		
		elif trinket == "Hex Shrunken Head":
			return( Trinket(120, "Active", True, 20, 20, 0, "SP", 211)) #tested
		elif trinket == "Shifting Naaru Sliver":
			return(Trinket(90, "Active", True, 15, 15, 0, "SP", 320)) # tested
		else: 
			print("Trinket not found : ", trinket)
			return(Trinket(0, "Proc", False, 0, 0, 0, "SP", 0)) #empty
			
	def set_talents(self, 
	balance_of_power = True, # +4% Hit
	focused_starlight = True, # +4% crit for SF and Wrath
	moonkin_form = True, # +5% Crit
	improved_mf = True, # +10% Moonfire crit 
	starlight_wrath = True, # reduce cast time by 0.5s
	vengeance = True, # +100% Crit damange
	lunar_guidance = True, # Spellpower bonus = 24% of total intel
	moonfury = True, # +10% damage
	intensity = 3, # Each point gives 10% normal regen while casting
	dreamstate = 3, # Gives a mana regen based on int % : 0.1% - 0.07% - 0.04%
	wrath_of_cenarius = True): # +20% Spellpower for SF | +10% SpellPower for Wrath
		self.intensity = intensity
		self.dreamstate = .1 if dreamstate == 3 else ( .07 if dreamstate == 3 else (.04  if dreamstate == 1 else 0 ))
		if balance_of_power:
			self.balance_of_power = 4 # +4% Hit
		else:
			self.balance_of_power = 0
		if focused_starlight:
			self.focused_starlight = 4 # +4% crit for SF and Wrath
		else:
			self.focused_starlight = 0
		if moonkin_form:
			self.moonkin_form = 5 # +5% Crit
		else:
			self.moonkin_form = 0
		if improved_mf:
			self.improved_mf = 10 # +10% Moonfire crit 
			self.imp_mf = 1.1 
		else:
			self.improved_mf = 0
			imp_mf = 1 
		self.starlight_wrath = starlight_wrath # reduce cast time by 0.5s
		self.vengeance = vengeance # +100% Crit damange
		self.lunar_guidance = lunar_guidance # Spellpower bonus = 24% of total intel
		if moonfury:
			self.moonfury = 1.1 # +10% damage
		else : 
			self.moonfury = 1
		if wrath_of_cenarius:
			self.wrath_of_cenarius_starfire = 1.2
			self.wrath_of_cenarius_wrath = 1.1
		else:
			self.wrath_of_cenarius_starfire = 1
			self.wrath_of_cenarius_wrath = 1
		