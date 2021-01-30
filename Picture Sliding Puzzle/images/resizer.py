from PIL import Image
import os

for file in os.listdir('claps/'):
	# if not file.endswith('.py'):
		img  = Image.open('claps/'+file)
		img = img.resize((100,67))
		img.save(f'{file[:7]}.png')