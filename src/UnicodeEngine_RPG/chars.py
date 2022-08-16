from colorama import Fore, Back, Style
from typing import Callable, Union
from copy import deepcopy

class Char:
	def __init__(
			self,
			name: str,
			position: int = 0,
			color: Back = Back.BLACK,
			collision: bool = False,
			action: Union[Callable, None] = None,
			walk_action: Union[Callable, None] = None
	):
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
		:param action: The function that should be triggered when the player uses the action key in front of the tile.
		:param walk_action: The function that should be triggered when the player walks on the tile.
		"""
		self.name = name
		self.position = position
		self.color = color
		self.collision = collision
		self.action = action
		self.walk_action = walk_action


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


	def set_action(self, action: Union[Callable, None]):
		"""
		Sets the function that should be triggered when the player uses the action key in front of the tile.
		:return: The class instance, to allow for class chaining.
		"""
		self.action = action
		return self


	def set_walk_action(self, walk_action: Union[Callable, None]):
		"""
		Sets the function that should be triggered when the player walks on the tile.
		:return: The class instance, to allow for class chaining.
		"""
		self.walk_action = walk_action
		return self


	def set_color(self, color: Back):
		"""
		Sets the color of the tile, using an instance of the colorama Back class.
		:return: The class instance, to allow for class chaining.
		"""
		self.color = color
		return self

	def copy(self):
		"""
		Returns a copy of this object.
		"""
		return deepcopy(self)
