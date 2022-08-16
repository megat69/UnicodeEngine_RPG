"""
Utility functions used by the engine, can also be used by the user..
"""
from colorama import Style
from time import sleep
import sys

from .getch import getch


def display_text(text: str, slowness_multiplier: float = 1.0, do_getch: bool = True):
	"""
	Displays text on the screen character by character, in an animated fashion.
	:param text: The text to display. Use the '¶' Unicode character to add an arbitrary pause.
	:param slowness_multiplier: The speed multiplier for the text display. Higher is slower, lower is faster. Default is 1.0.
	:param do_getch: Whether to await a character input at the end.
	"""
	# Resets the formatting
	print(Style.RESET_ALL)

	# Fetches all the characters in the text
	for i in range(len(text)):
		# Checking if the character is not a skip or a formatting character
		if text[i] != "¶":
			# Writes it to the screen one by one
			sys.stdout.write(text[i])
		# Makes a little pause
		sleep((0.04 if text[i] != "\n" else 0.2) * slowness_multiplier)

	# Awaits a character press
	if do_getch: getch()

