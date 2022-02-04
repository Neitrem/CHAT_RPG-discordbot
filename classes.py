class ITEM:
	"""for any object that can be stored in the inventory"""
	def __init__(self, id_, type_, rarity, amount, is_stackable):
		self.id_ = id_
		"uniq number of this type of items"
		self.type_ = type_
		"full line of current type (item.tool.sword.common_sword)"
		self.rarity = rarity
		"the rarity of the item (common, non-common, rare, super, legendary)"
		self.amount = amount
		"current amount of this items in the inventory (1, 3, 22 ...)"
		self.is_stackable = is_stackable
		"flag for recognize non-stackable item (True, False)"

	def get_string(self):
		return self.__dict__


class FOOD(ITEM):
	"""for any food item"""
	def __init__(self, id_, type_, rarity, amount, is_stackable, amount_hp_reg, effect=None):
		ITEM.__init__(self, id_, type_, rarity, amount, is_stackable)
		self.amount_hp_reg = amount_hp_reg
		"the amount of hp that will be healed after using this item (1, 3, 3.5, 20 ...)"
		self.effect = effect
		"any boosts or debuffs that will be gained after using this item (increase.speed:10, decrease.intelligence:10 ...)"


class POTION(ITEM):
	"""for any potion"""
	def __init__(self, id_, type_, rarity, amount, is_stackable, ban_use_time, toxin_lvl, effect):
		ITEM.__init__(self, id_, type_, rarity, amount, is_stackable)
		self.ban_use_time = ban_use_time
		"the timeout of using potion of one type (heal:20, power:10 ....)"
		self.toxin_lvl = toxin_lvl
		"the level of intoxication u will gain after using this potion (5, 10 ,40)"
		self.effect = effect
		"some extra effects of potion (power:2, speed:4 ...)"


class EQUIPMENT(ITEM):
	"""for anything that can be equip"""
	def __init__(self, id_, type_, rarity, amount, is_stackable, lvl, is_breakable, durability, max_durability, enchant=None, bonuses=None):
		ITEM.__init__(self, id_, type_, rarity, amount, is_stackable)
		self.lvl = lvl
		"the lvl of this item (1 ,5 , 55, ...)"
		self.is_breakable = is_breakable
		"flag for recognize non_breakable item (True, False)"
		self.durability = durability
		"the current durability of item (189, 765, 23456 ...)"
		self.max_durability = max_durability
		"the max durability of item (200, 1000, 50000 ...)"
		self.bonuses = bonuses
		"bonuses that item gained after craft ({speed:2, slow:3}, {...} ...)"
		self.enchant = enchant
		"the enchants gained by enchanting by wizard or blacksmith"


class TOOL(EQUIPMENT):
	"""for any tools like axe, pickaxe, sword, bowl and etc."""
	def __init__(self, id_, type_, rarity, amount, is_stackable, lvl, is_breakable, durability, max_durability, damage,
					damage_type, damage_distance, enchant=None, bonuses=None):
		EQUIPMENT.__init__(self, id_, type_, rarity, amount, is_stackable, lvl, is_breakable, durability, max_durability, enchant, bonuses)
		self.damage = damage # damage that item deals by one hit (2, 15 ,105 ...)
		self.damage_type = damage_type # the damage type that this item deals (slash, crush, ...)
		self.damage_distance = damage_distance # the distance when it can be used (short, medium, long)


class CLOTHES(EQUIPMENT):
	"""for any type of armour and non-armour clothes"""
	def __init__(self, id_, type_, rarity, amount, is_stackable, lvl, is_breakable, durability, max_durability, resist,
					body_part, resist_list=None, enchant=None, bonuses=None):
		EQUIPMENT.__init__(self, id_, type_, rarity, amount, is_stackable, lvl, is_breakable, durability, max_durability, enchant, bonuses)
		self.resist = resist
		"the damage that will be ignored (1, 13, 100)"
		self.resist_list = resist_list
		"list of damage types that will be ignored more or lesser ({slash:2, crush:-3}, {...}, ...)"
		self.body_part = body_part


class ENTITY:
	"""for any living and deadly characters"""
	def __init__(self, hp, max_hp, lvl, type_, base_armour, stats):
		self.hp = hp
		"""the health point of this character (7, 45, 145, ...)"""
		self.max_hp = max_hp
		"""max amount of hp (10, 100, 1000, ...)"""
		self.lvl = lvl
		"""the current lvl (1, 5, 15, ...)"""
		self.type_ = type_
		"""string variable that contains info about type of this character(wolf, villager, player, etc...)"""
		self.base_armour = base_armour
		"""the base armour that character have without any shields and so-on (0, 1, 2 , 23, ...)"""
		self.stats = stats
		"""the dictionary that contains all characteristics of character (strength, speed, etc) as integer"""

	def get_string(self):
		return self.__dict__


class HUMAN(ENTITY):
	"""u can use it for every entities that has body like human and also have some intelligence)"""
	def __init__(self, hp, max_hp, lvl, type_, base_armour, stats, name, clothes, tool, coins):
		ENTITY.__init__(self, hp, max_hp, lvl, type_, base_armour, stats)
		self.name = name
		"""the name or nickname of this character (Nikol, Neitrem, etc)"""
		self.clothes = clothes
		"""the list of clothes that is on this character ({{name:t-short, ...}, {...}, ...}, {...})"""
		self.tool = tool
		"""the tool that equipped now ({name: sword, damage: 12, ...})"""
		self.coins = coins
		"""the money that character have with it (12, 34, 109089, ...)"""


class PLAYER(HUMAN):
	"""use it only for players characters"""
	def __init__(self, hp, max_hp, lvl, type_, base_armour, stats, name, coins, inventory, tool=None, clothes=None, exp=None,
				death_debuffs=None, professions=None):
		HUMAN.__init__(self, hp, max_hp, lvl, type_, base_armour, stats, name, clothes, tool, coins)
		self.inventory = inventory
		"""the list of items that player has now ({{name: apple, ...}, {name: sword, ...}, ...}, ...)"""
		self.exp = exp
		"""the current amount of lvl points (123 ,450, ...)"""
		self.death_debuffs = death_debuffs
		"""the debuffs that u got after death ({slow:3, weakness:4, ...}, {...}, ...)"""
		self.professions = professions
		"""list of this player profession and its lvl ({{name: dswdvef, ...}, {...}, ...}, {...})"""

	def get_string(self):
		# creating string from list of classes in inventory
		string = HUMAN.get_string(self)
		inv = string['inventory'] # list of classes
		new_inv_arr = []
		for i in inv:
			# getting all variable from class object in i
			new_inv_arr.append(i.__dict__)

		# sett new inventory string
		string['inventory'] = new_inv_arr

		# getting all variable from class object in tool
		try:
			string['tool'] = string['tool'].__dict__
		except:
			string['tool'] = {}

		# regenerating clothes variable
		cloth = string['clothes']  # dict of classes
		new_cloth = {'head': None, 'body': None, 'legs': None}
		# creating string from classes
		try:
			new_cloth['head'] = cloth['head'].__dict__
		except:
			new_cloth['head'] = None
		try:
			new_cloth['body'] = cloth['body'].__dict__
		except:
			new_cloth['body'] = None
		try:
			new_cloth['legs'] = cloth['legs'].__dict__
		except:
			new_cloth['legs'] = None

		# sett new clothes string
		string['clothes'] = new_cloth

		if string['coins'] is None:
			string['coins'] = 0

		return string


class MOB(ENTITY):
	def __init__(self, hp, max_hp, lvl, type_, base_armour, stats, damage_type,
				resist_list):
		ENTITY.__init__(self, hp, max_hp, lvl, type_, base_armour, stats)
		self.damage_type = damage_type
		"""the damage type that this mob deal (slash, crush, ...)"""
		self.resist_list = resist_list
		"""list of damage types that will be ignored more or lesser ({slash:2, crush:-3}, {...}, ...)"""


class ANIMAL(MOB):
	"""use it for any animals"""
	def __init__(self, hp, max_hp, lvl, type_, base_armour, stats, damage_type,
				resist_type, agro):
		MOB.__init__(self, hp, max_hp, lvl, type_, base_armour, stats, damage_type, resist_type)
		self.agro = agro
		"""the flag for recognize aggressive or not animals"""


class MONSTER(MOB):
	"""use it for always aggressive creatures and some other strange things"""
	def __init__(self, hp, max_hp, lvl, type_, base_armour, stats, damage_type, resist_type):
		MOB.__init__(self, hp, max_hp, lvl, type_, base_armour, stats, damage_type, resist_type)
