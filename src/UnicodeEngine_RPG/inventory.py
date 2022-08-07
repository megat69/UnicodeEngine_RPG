from typing import Any, Callable


class InventoryItem:
	"""
	An instance of a subcategory in the inventory.
	"""
	def __init__(self, name:str, value:Any, update:Callable):
		"""
		:param name: The name of the subcategory.
		:param value: The value of displayed on the screen.
		:param update: A function to update the value of the subcategory.
			The function should take one argument, 'value', and return the final value.
		"""
		self.name = name
		self.value = value
		self.update = update


	def _update_value(self, value):
		"""
		Updates the value based on the user's function.
		Returns self.
		"""
		self.value = self.update(value)
		return self
