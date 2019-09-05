#! /home/proginoskes/anaconda3/bin/python

import math
from pathlib import Path
from typing import Optional, Union, Callable


def checkdir(path: Union[str, Path]) -> Path:
	path = Path(path)
	if not path.exists():
		path.mkdir()
	return path


def sort_folder(folder: Path, by: str, output_folder: Optional[Path] = None):
	if output_folder is None: output_folder = folder
	sorter = select_sorter(by)
	all_files = folder.glob("**/*")

	for filename in all_files:
		key = sorter(filename)
		destination_folder = checkdir(output_folder / key)
		destination = destination_folder / filename.name
		filename.rename(destination)


def select_sorter(by: str) -> Callable[[Path], str]:
	if by == 'filetype':
		return sort_by_filetype
	elif by == 'filecount':
		return sort_by_filecount
	elif by == 'imagesize':
		return sort_by_imagesize
	elif by == 'filesize':
		return sort_by_filesize
	else:
		raise ValueError(f"Could not find a sorter with key '{by}'")


def sort_by_filetype(filename: Path) -> str:
	return filename.suffix[1:]  # exclude the '.'


def sort_by_filecount(filename: Path, bin_size: int = 250) -> str:
	try:
		sort_by_filecount.count += 1
	except AttributeError:
		sort_by_filecount.count = 1
	return str(sort_by_filecount.count % bin_size)


def sort_by_imagesize(filename: Path) -> str:
	from PIL import Image
	image = Image.open(filename)
	image_size = image.height * image.width / 1000 ** 2

	if image_size < 1:
		s = f"{image_size:.1f}MP"
	else:
		s = f"{image_size:.0f}MP"

	return s


def sort_by_filesize(filename: Path) -> str:
	size = filename.stat().st_size

	size = math.floor(size / 1024 ** 2)

	return f"{size}MB"


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument(
		"by",
		help = "The type of sorting operation.",
		choices = ["filetype", "filecount", "filesize", "imagesize"]
	)
	parser.add_argument(
		"folder",
		help = "The folder to sort",
		type = Path
	)

	parser.add_argument(
		"--destination",
		help = "The destination folder",
		type = Path,
		default = None
	)

	args = parser.parse_args()
	if args.destination is None: args.destination = args.folder

	sort_folder(args.folder, args.by, args.destination)
