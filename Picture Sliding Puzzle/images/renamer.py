import re
import os

for file in os.listdir():
	name, ext = os.path.splitext(file)
	if ext == '.png':
		index = str(int(name[-3:]))
		new = f'img{index}.png'
		os.rename(file, new)