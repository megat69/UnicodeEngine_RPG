from colorama import Fore, Back, Style

class Char:
	def __init__(self, name: str, position: int = 0, color: Back = Back.BLACK):
		"""
		Creates a new character for the game.
		:param name: A string of exactly one character which represents the current character.
		:param position: The position of the character within its tile :
			0 -> Solid tile (default)
			1 -> Placed left on the tile
			2 -> Placed at the middle of the tile
			3 -> Placed right on the tile
		:param color: A color from the colorama library ; specifically from the 'Back' class. (Black by default)
		"""
		self.name = name
		self.position = position
		self.color = color
