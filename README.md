# UnicodeEngine_RPG
An engine that allows to render worlds and maps for console games based solely on Unicode.

## Features
[x] Full player movement
[x] Customizable controls, player, tilemap...
[x] Full control over the engine
[x] Actions from tiles
[ ] Turn-based fights (WIP)
[x] Inventory system
[x] Level editor system (see [UnicodeEngine_RPG_LevelEditor](https://github.com/megat69/UnicodeEngine_RPG_LevelEditor))
[x] User-created logic in Python

## How to install
### Install from PIP
Use the command `pip install UnicodeEngine-RPG` to install it.

### Install from source
Just download this repository, no building is required.

# Usage
See [the bottom of this file](https://github.com/megat69/UnicodeEngine_RPG/blob/main/src/UnicodeEngine_RPG/__init__.py) for an example.

## The main `UnicodeEngine_RPG` class
Instantiate this class at the beginning of your program to use it.

It requires two parameters : 
- `tilemap` : A tilemap to be used for the game, basically a 2D list of `Char` instances (see below). You can use the tilemap loader of the level editor (see below) to use it if you created the tilemap with the level editor.
- `player` : An instance of the `Player` class (see below) with its parameters set.

The class can also use some additional parameters :
- `playable_area` (tuple[int, int]) : A tuple of two integers representing the amount of characters displayed on each axis. Default is (20, 10)
- `controls` (str, 'wasdf' by default) : A string containing the characters to press for :
  - Forward ;
  - Left ;
  - Backward ;
  - Right ;
  - Action key
- `force_monochrome` (bool) : Whether to disable color rendering. False by default.
- `inventory` (dict) : A dict of InventoryItem class instances (see below) and their keys.
- `noclip` (bool) : Whether to disable collisions altogether. False by default.


Once the class is instantiated, and everything in your code is set up, you can call the `run` method of the class. 

**Keep in mind that this is a blocking function !**

This method can also take as an argument a callback function that will get called every frame, having as parameter the delta time (float).


### The `Char` class
The `Char` class allows you to represent a character on the tilemap, just like you would use a GameObject in your traditional engine.

The class requires an argument : `name`. It represents the current character, and must be a *single-character* string. It can be any Unicode character as well.

But multiple optional parameters can also be set to alter the look of the character :
- `position` (int, default: 0) : The position of the character within its tile, as each character as a 3-character width :
  - 0 -> Solid tile (default)
  - 1 -> Placed left on the tile
  - 2 -> Placed at the middle of the tile
  - 3 -> Placed right on the tile
- `color` (Back, default: Back.BLACK) : The background color of the character, given as a color from the [colorama](https://pypi.org/project/colorama/) library, and more specifically from its `Back` class. Default is `Back.BLACK`.
- `collision` (bool, default: False) : Whether the tile can NOT be walked on. If set to True, the tile will work like a wall ; the character will not be able to go through it.
- `action` (callback function/None, default: None) : A callback function to be called whenever the player *interacts* (via the interaction key) with the tile. Set to None to disable the interaction.
- `walk_action` (callback function/None, default: None) : A callback function to be called whenever the player walks on a tile. Useful to set up traps. If the parameter `collision is set to True, this function will never be called. Set to None to disable the interaction.

The class also contains setters for these methods, which also support method chaining.

### The `Player` class
The `Player` class represents the Player object. It stores its position, direction, and the characters used to represent the player.

It requires the following argument : `position`, a ***list*** of two integers representing the position of the player on the tilemap.

You can also set the `direction_characters` argument, which is a string of four characters representing the different rotations of the player. Default is `←↑↓→`.

The class also possesses a third attribute, though you can't set it through the constructor.<br/>
This attribute is the `current_direction` attribute, which keeps track of the current rotation of the player. It is an integer always between 0 and 3, and is used as an index when choosing the  `direction_characters`.

### The `display_text` function
This function allows to display text on the screen character by character, in an animated fashion.

It takes as argument a string containing the text to be displayed, where you can use the `¶` Unicode character to add an arbitrary pause.

It can also take two more arguments :
- `slowness_multiplier` (float) : The speed multiplier for the text display. Higher is slower, lower is faster. Default is 1.0.
- `do_getch` (bool) : Whether to await a character input at the end, allows for a pause at the end of the animation.

## Examples
The following example is provided at [the bottom of this file](https://github.com/megat69/UnicodeEngine_RPG/blob/main/src/UnicodeEngine_RPG/__init__.py)

```python
from UnicodeEngine_RPG import UnicodeEngine_RPG, Char, display_text, Player, InventoryItem
import sys
import colorama; colorama.init(); from colorama import Fore, Back, Style


# Creating the main characters
plain_char = Char("▓", color=Back.GREEN)
semi_plain_char = Char("▒", position=2, color=Back.YELLOW)

# Creating a callback function for one character's action
def hello():
    display_text("Hello !")

# Creating a function to update one of the inventory items
def is_low_health(value):
    if app.inventory["health"].value < 5:
        display_text(Fore.RED + "Low health !" + Style.RESET_ALL, slowness_multiplier=0.5, do_getch=False)
    elif app.inventory["health"].value <= 0:
        sys.exit(0)
    return value

# Creating the main class and feeding it the tilemap, along with other arguments
app = UnicodeEngine_RPG(
    tilemap = [
        [plain_char, plain_char, plain_char, plain_char, plain_char],
        [plain_char, plain_char, plain_char, plain_char, plain_char],
        [plain_char, plain_char.copy().set_walk_action(hello), semi_plain_char.copy().set_collision(True).set_action(hello), plain_char, plain_char],
        [plain_char, plain_char, plain_char, plain_char, plain_char],
        [plain_char, plain_char, plain_char, plain_char, plain_char]
    ],
    player = Player([0, 0]),
    playable_area = (8, 8),
    controls = "zqsdf",  # AZERTY controls, you can change that
    force_monochrome = False,
    inventory = {
        "health": InventoryItem("Health", 15, is_low_health)
    }
)


# Creating an update function
def update(dt:float):
    app.inventory["health"].update_value(app.inventory["health"].value - dt)

# Finally running the app
app.run(update)
```
