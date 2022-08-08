from colorama import Fore, Back, Style

class Char:
	def __init__(self, name: str, position: int = 0, color: Back = Back.BLACK, collision: bool = False):
		"""
		Creates a new character for the game.
		:param name: A string of exactly one character which represents the current character.
		:param position: The position of the character within its tile :
			0 -> Solid tile (default)
			1 -> Placed left on the tile
			2 -> Placed at the middle of the tile
			3 -> Placed right on the tile
		:param color: A color from the colorama library ; specifically from the 'Back' class. (Black by default)
		:param collision: Whether the tile can NOT be walked on. False by default.
		"""
		self.name = name
		self.position = position
		self.color = color
		self.collision = collision


	def __repr__(self):
		return f"<Char \"{self.name}\" position={self.position} collision={self.collision}>"

	def set_collision(self, collision: bool):
		"""
		Sets whether the tile can NOT be walked on.
		:return: The class instance, to allow for class chaining.
		"""
		self.collision = collision
		return self

	def set_position(self, position: int):
		"""
		Sets the position of the character within its tile :
			0 -> Solid tile (default)
			1 -> Placed left on the tile
			2 -> Placed at the middle of the tile
			3 -> Placed right on the tile
		:return: The class instance, to allow for class chaining.
		"""
		self.position = position
		return self
