"""
Main UnicodeEngine_RPG module.
"""
import time
import colorama; colorama.init()
from colorama import Fore, Back, Style
import sys
from typing import Callable, Union
from copy import deepcopy

from chars import Char
from getch import getch
from player import Player
from inventory import InventoryItem
from utilities import display_text


class UnicodeEngine_RPG:
	def __init__(
			self,
			tilemap: list,
			player: Player,
			playable_area: tuple[int, int] | list[int, int] = (20, 10),
			controls: str = "wasdf",
			force_monochrome: bool = False,
			inventory: dict = None
	):
		"""
		Initialization of a new engine instance.
		:param tilemap: A 2D list containing all the characters of the map,
			instances of the 'Char' class.
		:param player: A Player object.
		:param playable_area: A tuple of two integers representing the amount of characters
			displayed on each axis.
		:param controls: A string containing the characters to press for :
			- Forward ;
			- Left ;
			- Backward ;
			- Right ;
			- Action key
			('wasdf' by default)
		:param force_monochrome: Whether to disable color rendering. False by default.
		:param inventory: A dict of InventoryItem class instances and their keys.
		"""
		self.tilemap = tilemap
		self.playable_area = playable_area
		self.player = player
		self.controls = controls
		self.force_monochrome = force_monochrome
		self.inventory = inventory if inventory is not None else {}

	def run(self, update: Callable = None):
		"""
		Launches the engine main loop.
		:param update: A function that will get called every frame, having as parameter the delta time.
		"""
		# Registers the update function
		self.update = update if update is not None else lambda dt: None

		# Asking the user to resize his console
		print("\n" * 20)
		for i in range(self.playable_area[0]):
			if i == self.playable_area[0] // 2:
				print("|   Please adjust your console size so that all these lines fit, and only these lines")
			else:
				print("|")
		getch()

		self._last_frame_executed = time.time()
		self.dt = 0
		# Main loop
		while True:
			# Capping at 60 frames per second
			if time.time() - self._last_frame_executed < 1/15: continue
			self.dt = time.time() - self._last_frame_executed

			# Calling the update method
			self.update(self.dt)

			# Rendering the tilemap
			self.render_tiles(force_no_color=self.force_monochrome)

			# Getting the next keystroke
			keystroke = getch()
			if keystroke == "n":
				confirm = input("Do you want to leave ? (y/n): ")
				if confirm.lower() == "y":
					sys.exit(0)

			# Displaying the controls
			elif keystroke == "c":
				self.display_controls()

			# If the action key is pressed
			elif keystroke == self.controls[4]:
				# If the player is doing an action, we check the tile in front of it for the action.
				# Beforehand, we create a position list for the direction, so we know later which tile the player is
				# interacting with.
				relative_tile_position = [0, 0]
				if self.player.current_direction == 1: relative_tile_position[0] = -1
				elif self.player.current_direction == 2: relative_tile_position[0] = 1
				elif self.player.current_direction == 3: relative_tile_position[1] = 1
				elif self.player.current_direction == 0: relative_tile_position[1] = -1

				try:
					# We check if the tile is in range, and if not, just go to the exception
					if self.player.position[0] + relative_tile_position[0] < 0 or \
							self.player.position[1] + relative_tile_position[1] < 0:
						raise IndexError

					tile = self.tilemap[self.player.position[0] + relative_tile_position[0]][self.player.position[1] \
					        + relative_tile_position[1]]
					# If the action of this tile is None, we just ignore it
					if tile.action is not None:
						tile.action()

				except IndexError:
					# If any error from tile number occurs, we just skip it, as it is the intended way
					pass

			self.do_movement(keystroke)

			# Keeping track of the time to execution
			self._last_frame_executed = time.time()


	def do_movement(self, keystroke):
		# Movement
		old_player_pos = self.player.position.copy()
		if keystroke == self.controls[0]:
			self.player.position[0] -= 1
			self.player.current_direction = 1
		elif keystroke == self.controls[2]:
			self.player.position[0] += 1
			self.player.current_direction = 2
		elif keystroke == self.controls[1]:
			self.player.position[1] -= 1
			self.player.current_direction = 0
		elif keystroke == self.controls[3]:
			self.player.position[1] += 1
			self.player.current_direction = 3

		# Checking if the list is not out of bounds
		if self.player.position[0] < 0:
			self.player.position[0] = 0
		elif self.player.position[0] >= len(self.tilemap):
			self.player.position[0] = len(self.tilemap) - 1
		elif self.player.position[1] < 0:
			self.player.position[1] = 0
		elif self.player.position[1] >= len(self.tilemap[0]):
			self.player.position[1] = len(self.tilemap[0]) - 1

		# Remembering the tile on which the player is on
		tile = self.tilemap[self.player.position[0]][self.player.position[1]]
		# Resetting to last position if tile in front is a collider
		if tile.collision is True:
			self.player.position = old_player_pos.copy()
		# Otherwise, calling the walk_action of the tile the player is on (if it is not None)
		else:
			if tile.walk_action is not None and old_player_pos != self.player.position:
				tile.walk_action()


	def display_controls(self):
		controls_text_indicator = "Movement :\n"
		controls_text_indicator += f"      ____ \n     ||{self.controls[0].upper()} ||\n     ||__||\n     |/__\|\n" \
		                           f" ____ ____ ____\n||{self.controls[1].upper()} |||{self.controls[2].upper()}" \
		                           f" |||{self.controls[3].upper()} ||\n" \
		                           "||__|||__|||__||\n|/__\|/__\|/__\|"
		controls_text_indicator += "\n" * 3 + "Interact :\n"
		controls_text_indicator += f" ____ \n||{self.controls[4].upper()} ||\n||__||\n|/__\|"

		print("\n" * max(self.playable_area[0] - len(controls_text_indicator.split("\n")) - 2, 0),
		      controls_text_indicator, "\n" * 2, sep="")
		getch()


	def render_tiles(self, force_no_color: bool = False, display_inventory: bool = True):
		"""
		Main rendering function, allows to render all the tiles in the tilemap and display them on
		the screen. It also displays the player and the inventory.
		"""
		final_str = "" + Fore.WHITE
		# Fetching every coordinate in the displayed range
		for x in range(self.player.position[0] - (self.playable_area[0] // 2), (self.playable_area[0] // 2) + self.player.position[0]):
			for y in range(self.player.position[1] - (self.playable_area[1] // 2), (self.playable_area[1] // 2) + self.player.position[1]):

				# Checking if the tile is in the playable area, and if not, displaying 3 spaces
				if x < 0 or y < 0 or x >= len(self.tilemap) or y >= len(self.tilemap[0]):
					final_str += "   " + Back.RESET

				# If the current coords aren't those of a player
				elif x != self.player.position[0] or y != self.player.position[1]:

					# If this is a regular tile, we display it 3 times
					if self.tilemap[x][y].position == 0:
						final_str += self.tilemap[x][y].color + self.tilemap[x][y].name * 3 + Back.RESET

					# Otherwise, we work out where to place it
					elif self.tilemap[x][y].position == 1:  # Left
						try:
							final_str += self.tilemap[x][y].color + self.tilemap[x][y].name + self.tilemap[x][y + 1].color + \
							             self.tilemap[x][y + 1].name * 2 + Back.RESET
						except IndexError:
							final_str += self.tilemap[x][y].color + self.tilemap[x][y].name + " " * 2 + Back.RESET

					elif self.tilemap[x][y].position == 2:  # Center
						try:
							final_str += self.tilemap[x][y - 1].color + self.tilemap[x][y - 1].name\
							             + self.tilemap[x][y].color + self.tilemap[x][y].name \
							             + self.tilemap[x][y - 1].color + self.tilemap[x][y - 1].name + Back.RESET
						except IndexError:
							try:
								try:
									final_str += self.tilemap[x + 1][y].color + self.tilemap[x + 1][y].name\
							             + self.tilemap[x][y].color + self.tilemap[x][y].name \
							             + self.tilemap[x + 1][y].color + self.tilemap[x + 1][y].name + Back.RESET
								except IndexError:
									final_str += self.tilemap[x - 1][y].color + self.tilemap[x - 1][y].name\
							             + self.tilemap[x][y].color + self.tilemap[x][y].name \
							             + self.tilemap[x - 1][y].color + self.tilemap[x - 1][y].name + Back.RESET
							except IndexError:
								final_str += self.tilemap[x][y].color + " " + self.tilemap[x][y].name + " " + Back.RESET

					elif self.tilemap[x][y].position == 3:  # Right
						try:
							final_str += self.tilemap[x][y].color + self.tilemap[x][y].name + self.tilemap[x][y - 1].color + \
							             self.tilemap[x][y - 1].name * 2 + Back.RESET
						except IndexError:
							final_str += self.tilemap[x][y].color + self.tilemap[x][y].name + " " * 2 + Back.RESET

				else:  # Displaying player character
					# We look if the character usually below the player is a full tile
					if self.tilemap[x][y].position == 0:
						# If so, we know the tile to display below
						char_around = self.tilemap[x][y].name
						color_around = self.tilemap[x][y].color

					else:
						# We look for every character around him, and we determine which is the most used
						# while skipping those who are not full
						chars_around = ""
						colors_around = []
						for t in (-1, 1):
							try:
								if self.tilemap[x][y + t].position == 0:
									chars_around += self.tilemap[x][y + t].name
									colors_around.append(self.tilemap[x][y + t].color)
							except IndexError:
								pass
							try:
								if self.tilemap[x + t][y].position == 0:
									chars_around += self.tilemap[x + t][y].name
									colors_around.append(self.tilemap[x + t][y].color)
							except IndexError:
								pass
						if chars_around == "":
							chars_around = "-"
						if colors_around == "":
							colors_around = Back.BLACK

						# We select the character which is the most present around
						char_around = max(set(chars_around), key=chars_around.count)
						color_around = max(set(colors_around), key=colors_around.count)
						del chars_around
						del colors_around

					final_str += color_around + char_around + Style.BRIGHT + self.player.direction_characters[
						self.player.current_direction] + Style.RESET_ALL + color_around + char_around + Back.RESET
					del char_around
					del color_around

			final_str += "\n" + Style.RESET_ALL


		# Inventory display
		if display_inventory:
			final_str = final_str.split("\n")
			for i, element in enumerate(self.inventory.values()):
				final_str[i + 2] += "\t" + Style.RESET_ALL + element.name + " : " + str(element.value)
			final_str = "\n".join(final_str)


		if force_no_color:
			for style in ("BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "RESET"):
				for element in (Back, Fore):
					final_str = final_str.replace(getattr(element, style), "")
			for style in ("BRIGHT", "RESET_ALL", "DIM", "NORMAL"):
				final_str = final_str.replace(getattr(Style, style), "")

		print(final_str)


if __name__ == '__main__':
	plain_char = Char("▓", color=Back.GREEN)
	semi_plain_char = Char("▒", position=2, color=Back.YELLOW)

	def hello():
		display_text("Hello !")

	def is_low_health(value):
		if app.inventory["health"].value < 5:
			display_text(Fore.RED + "Low health !" + Style.RESET_ALL, slowness_multiplier=0.5, do_getch=False)
		elif app.inventory["health"].value <= 0:
			sys.exit(0)
		return value

	app = UnicodeEngine_RPG(
		tilemap = [
			[plain_char, plain_char, plain_char, plain_char, plain_char],
			[plain_char, plain_char, plain_char, plain_char, plain_char],
			[plain_char, deepcopy(plain_char).set_walk_action(hello), deepcopy(semi_plain_char).set_collision(True).set_action(hello), plain_char, plain_char],
			[plain_char, plain_char, plain_char, plain_char, plain_char],
			[plain_char, plain_char, plain_char, plain_char, plain_char]
		],
		player = Player([0, 0]),
		playable_area = (8, 8),
		controls = "zqsdf",
		force_monochrome = False,
		inventory = {
			"health": InventoryItem("Health", 15, is_low_health)
		}
	)


	def update(dt:float):
		app.inventory["health"].update_value(app.inventory["health"].value - dt)

	app.run(update)
