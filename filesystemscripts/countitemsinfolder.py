from pathlib import Path
from typing import Tuple, List
import os

class CountObjects:
	""" Recursively counts the number of files within a folder. Can also count the items in subfolder.
		Parameters
		----------
		level: int
			The number of levels to recurse into if a subfolder is found. A value of 1 refers to the current directory.
	"""

	def __init__(self, level: int = 1):
		self.levels = level

		self.indent_character = "\t"

	def count(self, folder: Path, max_level:int = 1):

		starting_level = len(folder.parents)

		for directory, subfolders, files in os.walk(folder):
			path = Path(directory)
			if path.is_file() or path.name.startswith('.'): continue
			level = len(path.parents) - starting_level
			if level > max_level:
				continue
			indent = self.indent_character * level

			line = f"{indent}{len(files):>5}\t{path}"
			print(line)



	def filter_items(self, path:Path)->Tuple[List[Path], List[Path]]:
		"""
			Splits all items in `path` into folders and files.
		"""
		items = list(path.iterdir())
		folders = [i for i in items if i.is_dir()]
		files = [i for i in items if i.is_file()]
		return folders, files



if __name__ == "__main__":
	#f = Path("/home/proginoskes/Downloads/")
	#counter = CountObjects()

	#counter.count(f)
	folder = Path("/home/proginoskes/Downloads/rips/")

	key = lambda s: len(list(s.iterdir())) if s.is_dir() else 1

	items = sorted(folder.iterdir(), key = key)
	for i in items:
		print(key(i), '\t', i)

