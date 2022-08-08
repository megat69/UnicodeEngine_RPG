class Player:
	def __init__(self, position: list, direction_characters: str = "←↑↓→"):
		self.position = position
		self.direction_characters = direction_characters
		self.current_direction = 1
