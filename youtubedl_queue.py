from pathlib import Path
import subprocess
from typing import List, Tuple
import os
from loguru import logger
from tqdm import tqdm


def read_queue_file(filename: Path) -> List[Tuple[str, str]]:
	contents = filename.read_text()
	lines = [i.strip() for i in contents.split('\n')]
	lines = [i for i in lines if not i.startswith('#')]
	lines = [i.strip().split('\t') for i in lines]
	return lines


def download_queue(filename: Path, folder: Path):
	if not folder.exists():
		folder.mkdir()

	lines = read_queue_file(filename)

	for index, line in enumerate(lines):

		try:
			url, name = line
			logger.info(f"Downloading {index + 1} of {len(lines)}: {name}")
		except ValueError:
			message = f"This line cannot be parsed: '{line}'"
			logger.warning(message)
			continue

		video_path = folder / (name + '.mp4')
		if video_path.exists(): continue
		command = ["youtube-dl", "-o", f'{folder / name}.%(ext)s', url]
		subprocess.run(command)


from pathlib import Path

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	folder = Path.home() / "Downloads" / "Media Download" / "sponsorplay"

	parser.add_argument(
		"filename",
		help = "A text file with the url and filename (optional) of videos to download using youtube-dl.",
		type = Path
	)

	parser.add_argument(
		"folder",
		help = "The destination folder.",
		type = Path
	)

	args = parser.parse_args([str(folder / "sponsorplay.txt"), str(folder)])

	download_queue(args.filename, args.folder)
