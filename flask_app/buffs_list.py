class Buffs_list:
	def __init__(
	self,
	is_motw = True,
	is_divine_spirit = True,
	is_arcane_brilliance = True, #40 intellect +14 motw
	is_totem_of_wrath = True,
	is_wrath_of_air = True,
	is_draenei_in_group = True,
	curse_of_elements = 1, # coeff
	is_blessing_kings = True, # 10% stats increased
	is_crusader = True,
	is_sham_4_piece = True,
	is_flask = True,
	is_food = True,
	is_oil = True,
	is_twilight_owl = True,
	is_eye_of_night = True,
	is_T5 = True,
	is_T6_2 = True,
	is_T6_4 = True,
	is_misery = True,
	is_drums = True,
	is_lust = True,
	# Mana stuff
	is_bowis = True,
	is_mana_oil = False,
	is_manapot = True,
	is_rune = True,
	is_innervate = False,
	is_mana_spring = True,
	is_shadow_priest = False,
	is_judgment_of_wisdom = True,
	is_spirit_scroll = False,
	is_destruction_potion = False,
	shadow_priest_dps = 900,
	lust_count = 1):
		self.is_motw = is_motw
		self.is_divine_spirit = is_divine_spirit
		self.is_arcane_brilliance = is_arcane_brilliance #40 intellect +14 motw
		self.is_totem_of_wrath = is_totem_of_wrath
		self.is_wrath_of_air = is_wrath_of_air
		self.is_draenei_in_group = is_draenei_in_group
		self.curse_of_elements = curse_of_elements
		self.is_blessing_kings = is_blessing_kings # 10% stats increased
		self.is_crusader = is_crusader
		self.is_sham_4_piece = is_sham_4_piece
		self.is_flask = is_flask
		self.is_food = is_food
		self.is_oil = is_oil
		self.is_twilight_owl = is_twilight_owl
		self.is_eye_of_night = is_eye_of_night
		self.is_T5 = is_T5
		self.is_T6_2 = is_T6_2
		self.is_T6_4 = is_T6_4
		if is_misery:
			self.misery = 1.05
		else :
			self.misery = 1
		self.is_drums = is_drums
		self.is_lust = is_lust
		self.lust_count = lust_count
		# Mana :
		self.is_bowis = is_bowis
		self.is_mana_oil = is_mana_oil
		self.is_manapot = is_manapot
		self.is_rune = is_rune
		self.is_innervate = is_innervate
		self.is_mana_spring = is_mana_spring
		self.is_shadow_priest = is_shadow_priest
		self.shadow_priest_dps = shadow_priest_dps 
		self.is_judgment_of_wisdom = is_judgment_of_wisdom
		self.is_spirit_scroll = is_spirit_scroll
		self.is_destruction_potion = is_destruction_potion		
				
	def get_stats_buffs(self):
		intel = 0
		crit_score = 0
		hit_score = 0 
		spellpower = 0
		haste = 0
		spirit = 0
		mp5 = 0
		
		## Update stats
		if self.is_motw:
			intel = intel + 18
			spirit = spirit + 18
		if self.is_arcane_brilliance:
			intel = intel + 40 
		if self.is_divine_spirit:
			spirit = spirit + 50
		if self.is_totem_of_wrath:
			hit_score = hit_score + (3 * 12.6)
			crit_score = crit_score + (3 * 22.1) 
		if self.is_draenei_in_group:
			hit_score = hit_score + 12.6 
		if self.is_crusader:
			crit_score = crit_score + (3 * 22.1)
		if self.is_wrath_of_air:
			spellpower = spellpower + 101
		if self.is_sham_4_piece:
			spellpower = spellpower + 20
		if self.is_flask:
			spellpower = spellpower + 80
		if self.is_food:
			spellpower = spellpower + 23
			spirit = spirit + 20
		if self.is_oil: 
			spellpower = spellpower + 36
			crit_score = crit_score + 14
		if self.is_twilight_owl:
			crit_score = crit_score + (2 * 22.1)
		if self.is_eye_of_night:
			spellpower = spellpower + 34 
		if self.is_bowis:
			mp5 = mp5 + 49
		if self.is_mana_spring:
			mp5 = mp5 + 50
		if self.is_shadow_priest:
			mp5 = mp5 + 5 * (.05 * self.shadow_priest_dps)
		if self.is_spirit_scroll and not self.is_divine_spirit:
			spirit = spirit + 30
		stats =  {
		  "intel": intel,
		  "spirit": spirit,
		  "spellpower": spellpower,
		  "crit_score": crit_score,
		  "hit_score": hit_score,
		  "haste": haste,
		  "mp5": mp5
		}
		return(stats)
			
	def __str__(self):
		output =  ("\
		Mark of The Wild : " + str(self.is_motw) + "\n" + "\
		Divine Spirit : " + str(self.is_divine_spirit) + "\n" + "\
		Is Arcane Brillance : " + str(self.is_arcane_brilliance) + "\n" + "\
		Is Totem of Wrath : " + str(self.is_totem_of_wrath) + "\n" + "\
		Is Wrath of air : " + str(self.is_wrath_of_air) + "\n" + "\
		Is Draenei in group : " + str(self.is_draenei_in_group) + "\n" + "\
		Curse of Elements : " + str(self.curse_of_elements ) + "\n" + "\
		Is Blessing of kings : " + str(self.is_blessing_kings) + "\n" + "\
		Is Cursader : " + str(self.is_crusader) + "\n" + "\
		Is Sham 4 piece : " + str(self.is_sham_4_piece) + "\n" + "\
		Is Flask : " + str(self.is_flask) + "\n" + "\
		Is food buff : " + str(self.is_food) + "\n" + "\
		Is Oil : " + str(self.is_oil) + "\n" + "\
		Is Twilight owl : " + str(self.is_twilight_owl) + "\n" + "\
		Is Eye of the night : " + str(self.is_eye_of_night) + "\n" + "\
		Is T5 Bonuus : " + str(self.is_T5) + "\n" + "\
		Is T6 2 piece bonus : " + str(self.is_T6_2) + "\n" + "\
		Is T6 4 piece bonus : " + str(self.is_T6_4) + "\n" + "\
		Misery coeff : " + str(self.misery) + "\n" + "\
		Is Drums : " + str(self.is_drums) + "\n" + "\
		Is Lust / Hero : " + str(self.is_lust) + "\n" + "\
		Nb Lust avialable : " + str(self.lust_count))
		return(output)
