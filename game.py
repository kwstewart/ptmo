import datetime
from random import randint

class MYFAROG(object):

	def roll(self, quantity = 1, sides = 6):
		total = 0

		for r in range(0, quantity):
			ri = randint(1,sides)
			total = total + ri

		return total



class character(MYFAROG):

	# Attributes
	CHA = 0
	CON = 0
	DEX = 0
	INT = 0
	STR = 0
	WIL = 0

	# Attribute Modifiers
	Cha = 0
	Con = 0
	Dex = 0
	Int = 0
	Str = 0
	Wil = 0

	# Race, Age and Gender
	Race = ""
	Age = 0
	MaxAge = 0
	Gender = ""

	# Height, Weight and size
	Height = 0
	Weight = 0
	Size = 0


	def __init__(self, generate = True):

		if generate:			
			self.generateCharacter()

		self.listAttributes()

	def generateCharacter(self):
		# Roll attributes
		self.CHA = self.roll(3,6)
		self.CON = self.roll(3,6)
		self.DEX = self.roll(3,6)
		self.INT = self.roll(3,6)
		self.STR = self.roll(3,6)
		self.WIL = self.roll(3,6)

		# Set Race, Age and Gender
		self.setRace()
		self.setAge()
		self.setGender()

		# Apply Racial Modifactions
		self.setRaceMods()

		# Set Height, Weight and Size
		self.setHeight()
		self.setWeight()
		self.setSize()

		# Calculate Attribute Modifiers
		self.setAttributeModifiers()

	# Sets the attr mods
	def setAttributeModifiers(self):
		for a in ['CHA','CON','DEX','INT','STR','WIL']:
			setattr(self,a.capitalize(), self.getAttributeModifier(a))


	# Returns the attr mod (ie STR 15 = Str of +1, INT 8 = Int of -1 )
	def getAttributeModifier(self,AttributeName):
		ATR = getattr(self,AttributeName)
		if ATR <= 1:
			return -5
		elif ATR == 2:
			return -4
		elif ATR == 3:
			return -3
		elif ATR >= 4 and ATR <= 5:
			return -2
		elif ATR >= 6 and ATR <= 8:
			return -1
		elif ATR >= 9 and ATR <= 12:
			return 0
		elif ATR >= 13 and ATR <= 15:
			return 1
		elif ATR >= 16 and ATR <= 17:
			return 2
		elif ATR == 18:
			return 3
		elif ATR == 19:
			return 4
		elif ATR >= 20:
			return 5




	# Sets Race - During generation only
	def setRace(self):
		d = self.roll(3,6)
		if(d == 3):
			r = "Elf-Born"
		elif(d >=4 and d <= 16):
			r = "Native"
		elif(d == 17):
			r = "Demigod"
		elif(d == 18):
			r = "Fairling"
		setattr(self,"Race",r)

	# Sets Age - During generation only
	def setAge(self):
		d = self.roll(1,3)

		# Set base age value and CON multiplier based on Race
		if(self.Race == "Elf-Born"):		
			b = 15
			m = 5
		elif(self.Race == "Native"):
			b = 15
			m = 5
		elif(self.Race == "Demigod"):
			b = 15
			m = 6
		elif(self.Race == "Fairling"):
			b = 15
			m = 6

		# Age is Base age value + 1D3
		a = b + d

		# MaxAge is CON * CON_multiplier
		ma = self.CON * m

		setattr(self,"Age",a)
		setattr(self,"MaxAge",ma)

	# Sets Gender - During generation only
	def setGender(self):
		d = self.roll(1,6)
		# Fairlings are more likely male
		if self.Race == "Fairling":
			if d >= 5:
				g = "M"
			else:
				g = "F"
		else:
			if d <= 3:
				g = "M"
			else:
				g = "F"
		setattr(self,"Gender",g)

	# Applies Racial Modifications
	def setRaceMods(self):
		mods = {
			"Darkling": {
				"M": { "CHA" : -2, "CON": 0, "DEX": 0, "INT": -2, "STR": 0, "WIL": -2},
				"F": { "CHA" : -1, "CON": 0, "DEX": 0, "INT": -2, "STR": -1, "WIL": -2}
			},
			"Weakling": {
				"M": { "CHA" : -1, "CON": -1, "DEX": 1, "INT": -1, "STR": -2, "WIL": -2},
				"F": { "CHA" : 0, "CON": -1, "DEX": 1, "INT": -1, "STR": -3, "WIL": -2}
			},
			"Foreigner": {
				"M": { "CHA" : -1, "CON": 0, "DEX": 0, "INT": -1, "STR": -1, "WIL": -1},
				"F": { "CHA" : 0, "CON": 0, "DEX": 0, "INT": -1, "STR": -2, "WIL": -1}
			},
			"Native":{
				"M": { "CHA" : 0, "CON": 0, "DEX": 0, "INT": 0, "STR": 0, "WIL": 0},
				"F": { "CHA" : 2, "CON": 0, "DEX": 0, "INT": 0, "STR": -2, "WIL": 0}
			},
			"Elf-Born":{
				"M": { "CHA" : 2, "CON": -1, "DEX": 1, "INT": 1, "STR": -1, "WIL": 1},
				"F": { "CHA" : 4, "CON": -1, "DEX": 1, "INT": 1, "STR": -3, "WIL": 1}
			},
			"Demigod": {
				"M": { "CHA" : 1, "CON": 1, "DEX": 0, "INT": 1, "STR": 1, "WIL": 1},
				"F": { "CHA" : 3, "CON": 1, "DEX": 0, "INT": 1, "STR": -1, "WIL": 1}
			},
			"Fairling": {
				"M": { "CHA" : 1, "CON": 1, "DEX": 0, "INT": 2, "STR": 2, "WIL": 1},
				"F": { "CHA" : 3, "CON": 1, "DEX": 0, "INT": 2, "STR": 0, "WIL": 1}
			}
		}

		for a in ['CHA','CON','DEX','INT','STR','WIL']:
			# Get the modifier from the table above
			m = mods[self.Race][self.Gender][a]
			# Get the current value for this attribute
			v = getattr(self,a)
			# Add the modifer to the current value
			setattr(self,a, m + v)

	# Sets Height (in inches) - During generation only
	def setHeight(self):
		d = self.roll(4,6)
		if self.Race == "Native":
			if self.Gender == "M":
				b = 58
			else:
				b = 53
		if self.Race == "Elf-Born":
			if self.Gender == "M":
				b = 56
			else:
				b = 51
		if self.Race == "Demigod":
			if self.Gender == "M":
				b = 59
			else:
				b = 54
		if self.Race == "Fairling":
			if self.Gender == "M":
				b = 59
			else:
				b = 56
		h = b + d
		setattr(self,"Height",h)

	# Sets Weight (in pounds) - During generation only
	# W = 4D6 * 3 + (Str * 10) + 40
	def setWeight(self):
		w = self.roll(4,6) * 3 + (self.Str * 10) + 40 + self.Height
		setattr(self,"Weight",w)

	# Sets Size - During generation only
	def setSize(self):
		if self.Weight <= 45:
			s = -6
		elif self.Weight >= 46 and self.Weight <= 60:
			s = -5
		elif self.Weight >= 46 and self.Weight <= 75:
			s = -4
		elif self.Weight >= 76 and self.Weight <= 95:
			s = -3
		elif self.Weight >= 96 and self.Weight <= 115:
			s = -2
		elif self.Weight >= 116 and self.Weight <= 135:
			s = -1
		elif self.Weight >= 136 and self.Weight <= 165:
			s = 0
		elif self.Weight >= 166 and self.Weight <= 205:
			s = 1
		elif self.Weight >= 206 and self.Weight <= 255:
			s = 2
		elif self.Weight >= 256:
			s = 3

		setattr(self,"Size",s)


	# Debugging attr
	def listAttributes(self):
		print ' CHA: {obj.CHA} ({obj.Cha})\n CON: {obj.CON} ({obj.Con})\n DEX: {obj.DEX} ({obj.Dex})\n INT: {obj.INT} ({obj.Int})\n STR: {obj.STR} ({obj.Str})\n WIL: {obj.WIL} ({obj.Wil})\n Race: {obj.Race}\n Age: {obj.Age} ({obj.MaxAge})\n Gender: {obj.Gender}\n Height: {obj.Height}\n Weight: {obj.Weight}\n Size: {obj.Size}'.format(obj = self)
