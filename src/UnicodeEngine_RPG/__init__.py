"""
Main UnicodeEngine_RPG module.
"""
import colorama; colorama.init()
from chars import Char
class UnicodeEngine_RPG:
	def __init__(self, chars: list):
		"""
		Initialization of a new engine instance.
		:param chars: A list containing all the characters the engine might use.
		"""
		self.chars = chars

	def run(self):
		"""
		Launches the engine main loop.
		"""
		pass


if __name__ == '__main__':
	app = UnicodeEngine_RPG(
		chars = [
			Char("▓"),
			Char("▒")
		]
	)
	app.run()
