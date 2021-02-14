import os
from PIL import Image

for file in os.listdir():
	name, ext = os.path.splitext(file)
	if ext == '.gif':
		num = int(name[6:8])
		img = Image.open(file).resize((60,60))
		img.save(f'explosion{num}.png')