import os
import datetime
from PIL import Image, ImageTk

class ImageProcessor:
	def __init__(self, path):
		self.path = path
		self.img = Image.open(self.path)
		self.size = width, height = self.img.width, self.img.height

	def display_image(self, img=None):
		if not img:
			img = self.img
		return ImageTk.PhotoImage(img), self.size

	def zoom(self, factor):
		if factor > 1:
			basewidth = int(self.size[0] * (factor / 100))
			wpercent = (basewidth/float(self.img.size[0]))
			hsize = int((float(self.img.size[1])*float(wpercent)))
			img = self.img.resize((basewidth,hsize), Image.ANTIALIAS)
			return ImageTk.PhotoImage(img)

	def resize_image(self, width, height, save=False):
		img = self.img.resize((width, height), Image.ANTIALIAS )
		if save:
			name = os.path.basename(self.path)[:-4]
			img.save(f'{name}-resized.png')
			self.img = img
		image, size = self.display_image(img)
		return image, size

	def create_folder(self):
		db = datetime.datetime.now()
		dt = db.strftime('%d%m%Y%H%M%S')
		folder = os.path.basename(self.path)[:-4] + dt + '/'
		if not os.path.exists(folder):
			os.mkdir(folder)

		return folder

	def dividebytile(self, imwidth, imheight, twidth, theight):
		img = self.img.resize((imwidth,imheight), Image.ANTIALIAS)
		folder = self.create_folder()

		x, y = 0, 0
		rows = imheight // theight
		cols = imwidth // twidth
		ct = 1
		for i in range(rows):
			x = 0
			for j in range(cols):
				region = (x, y, x+twidth, y+theight)
				img.crop(region).save(f'{folder}/{ct}.png')
				ct += 1
				x += twidth
			y += theight

	def dividebyrc(self, imwidth, imheight, rows, cols):
		img = self.img.resize((imwidth,imheight), Image.ANTIALIAS)
		folder = self.create_folder()

		x, y = 0, 0
		w = imwidth // cols
		h = imheight // rows
		ct = 1
		for i in range(rows):
			x = 0
			for j in range(cols):
				region = (x, y, x+w, y+h)
				img.crop(region).save(f'{folder}/{ct}.png')
				ct += 1
				x += w
			y += h

	def dividecustom(self, imwidth, imheight, x, y, width, height):
		img = self.img.resize((imwidth,imheight), Image.ANTIALIAS)
		name = os.path.basename(self.path)[:-4]

		region = (x, y, x+width, y+height)
		print(region)
		img.crop(region).save(f'{name}-{width}-{height}.png')

	def dividebyrect(self, imwidth, imheight, x, y, x1, y1):
		img = self.img.resize((imwidth,imheight), Image.ANTIALIAS)
		name = os.path.basename(self.path)[:-4]

		region = (x, y, x1, y1)
		img.crop(region).save(f'{name}-{x1-x}-{y1-y}.png')