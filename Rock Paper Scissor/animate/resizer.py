from PIL import Image

size = [round(0.90+(i*0.02), 2) for i in range(11)]
images = ['paper_large' ,'rock_large', 'scissor_large']
for img in images:
	image = Image.open(img+'.png')
	index = 0
	for zoom in size:
		pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
		image.resize((pixels_x, pixels_y)).save(f'{img}{index}.png')
		index += 1