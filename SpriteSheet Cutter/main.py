import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ALL, EventType
from tkinter import filedialog

from cutter import ImageProcessor

cwd = os.getcwd()

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.filepath = None
		self.zoom_val = tk.IntVar()
		self.zoom_val.set(100)
		self.crop_option = tk.IntVar()
		self.options = {'Divide by TileSize':1, 'Divide in Rows & Columns':2, 'Custom Cropping':3,
						'Rectangular Selection' : 4}
		self.image = None
		self.lines = []

		self.x = tk.IntVar()
		self.y = tk.IntVar()
		self.x1 =tk.IntVar()
		self.y1 =tk.IntVar()
		self.tilewidth = tk.IntVar()
		self.tileheight = tk.IntVar()
		self.tilewidth.set(24)
		self.tileheight.set(24)
		self.rows = tk.IntVar()
		self.columns = tk.IntVar()
		self.first = None
		self.second = None
		self.imwidth = tk.IntVar()
		self.imheight = tk.IntVar()
		self.imsize = None

		self.original_imsize = (0,0)
		self.drag = True

		self.draw_frames()
		self.draw_editor()
		self.draw_canvas()
		self.draw_options_frame()
		self.draw_header_frame()
		self.draw_menu_frame()

		self.master.bind('<Up>', self._go_up)
		self.master.bind('<Down>', self._go_down)
		self.master.bind('<Enter>', self._bound_to_mousewheel)
		self.master.bind('<Leave>', self._unbound_to_mousewheel)

	def draw_frames(self):
		self.canvas_frame = tk.Frame(self, width=600, height=500, bg='white')
		self.canvas_frame.grid(row=0, column=1, rowspan=2)
		self.canvas_frame.grid_propagate(False)

		self.editor_frame = tk.Frame(self, width=200, height=400, bg='white')
		self.editor_frame.grid(row=0, column=2)
		self.editor_frame.grid_propagate(False)

		self.options_frame = tk.Frame(self, width=200, height=100, bg='white')
		self.options_frame.grid(row=1, column=2)
		self.options_frame.grid_propagate(False)

	def draw_editor(self):
		self.header_frame = tk.Frame(self.editor_frame, width=200, height=60, bg='white')
		self.header_frame.grid(row=0, column=0)
		self.header_frame.grid_propagate(False)

		self.menu_frame = tk.Frame(self.editor_frame, width=200, height=140, bg='white')
		self.menu_frame.grid(row=1, column=0)
		self.menu_frame.grid_propagate(False)

		self.variable_frame = tk.Frame(self.editor_frame, width=200, height=200, bg='white')
		self.variable_frame.grid(row=2, column=0)
		self.variable_frame.grid_propagate(False)

	def draw_canvas(self):
		self.scrolly = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
		self.scrolly.grid(row=0, column=1, sticky='ns')

		self.scrollx = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
		self.scrollx.grid(row=1, column=0, sticky='we')

		self.canvas = tk.Canvas(self.canvas_frame, width=580, height=480, bg='#242424',
						yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
		self.canvas.grid(row=0, column=0)

		self.scrolly.configure(command=self.canvas.yview)
		self.scrollx.configure(command=self.canvas.xview)

		self.canvas.bind('<ButtonPress-1>', lambda event: self._get_position(event))
		self.canvas.bind("<B1-Motion>", lambda event: self._drag(event))

	def draw_options_frame(self):
		self.open = ttk.Button(self.options_frame, text='Open', width=12, command=self.open_img)
		self.open.grid(row=0, column=0, padx=(5,0), pady=(4,0))

		self.resize = ttk.Button(self.options_frame, text='Resize', width=12, state=tk.DISABLED,
						command=self.resize_frame)
		self.resize.grid(row=0, column=1, padx=(5,0), pady=(4,0))

		self.scaler = ttk.Scale(self.options_frame, from_=5, to=160, orient=tk.HORIZONTAL)
		self.scaler['variable'] = self.zoom_val
		self.scaler.set(100)
		self.scaler.bind("<ButtonRelease-1>", self.do_zoom)
		self.scaler.grid(row=2, column=0, columnspan=1, pady=5)
		self.scaler.grid_forget()

	def draw_header_frame(self):
		self.header = tk.Label(self.header_frame, bg='#242424', fg='#fff', width=27)
		self.header.grid(row=0, column=0)

		self.size = tk.Label(self.header_frame, bg='#242424', fg='#fff', width=27)
		self.size.grid(row=1, column=0)

	def draw_menu_frame(self):
		r = 0
		for text, value in self.options.items():
			ttk.Radiobutton(self.menu_frame, text=text, variable=self.crop_option,
					value=value, command=self.draw_variable_frame,
					width=25).grid(row=r, column=0, padx=10, pady=2)
			r += 1

		self.crop_option.set(1)
		self.draw_variable_frame()

	def draw_variable_frame(self):
		for widget in self.variable_frame.winfo_children():
			widget.destroy()

		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		self.first = None
		self.second = None

		opt = self.crop_option.get()

		if opt == 1:
			self.tilewidth.set(24)
			self.tileheight.set(24)

			tk.Label(self.variable_frame, text='Tile Width', width=12).grid(row=0, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.tilewidth
						).grid(row=0, column=1, padx=15, pady=5)
			tk.Label(self.variable_frame, text='Tile Height', width=12).grid(row=1, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.tileheight
						).grid(row=1, column=1, padx=15, pady=5)

			ttk.Button(self.variable_frame, text='Draw Tiles', command=self.draw_tiles).grid(
							row=2,column=0, columnspan=2)

			ttk.Button(self.variable_frame, text='Cut Tiles', command=self.cut_tiles_by_tile).grid(
							row=3,column=0, columnspan=2)
		if opt == 2:
			tk.Label(self.variable_frame, text='Num Rows', width=12).grid(row=0, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.rows
						).grid(row=0, column=1, padx=15, pady=5)
			tk.Label(self.variable_frame, text='Num Columns', width=12).grid(row=1, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.columns
						).grid(row=1, column=1, padx=15, pady=5)

			ttk.Button(self.variable_frame, text='Draw Rows & Columns', command=self.draw_rc).grid(
							row=2,column=0, columnspan=2)

			ttk.Button(self.variable_frame, text='Cut Tiles', command=self.cut_tiles_by_rc).grid(
							row=3,column=0, columnspan=2)

		if opt == 3:
			self.x.set(0)
			self.y.set(0)
			self.tilewidth.set(24)
			self.tileheight.set(24)

			tk.Label(self.variable_frame, text='x', width=8).grid(row=0, column=0)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.x
						).grid(row=0, column=1)
			tk.Label(self.variable_frame, text='y', width=8).grid(row=0, column=2)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.y
						).grid(row=0, column=3)

			tk.Label(self.variable_frame, text='width', width=8).grid(row=1, column=0)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.tilewidth
						).grid(row=1, column=1)
			tk.Label(self.variable_frame, text='height', width=8).grid(row=1, column=2)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.tileheight
						).grid(row=1, column=3)

			ttk.Button(self.variable_frame, text='Draw Rect', command=self.draw_rect).grid(
							row=2,column=0, columnspan=4, pady=5)

			ttk.Button(self.variable_frame, text='Cut Tile', command=self.cut_tiles_custom).grid(
							row=3,column=0, columnspan=4)

		if opt == 4:
			self.x.set(0)
			self.y.set(0)
			self.x1.set(0)
			self.y1.set(0)

			tk.Label(self.variable_frame, text='x', width=8).grid(row=0, column=0)
			self.pos1 = ttk.Entry(self.variable_frame, width=4,textvariable=self.x)
			self.pos1.grid(row=0, column=1)

			tk.Label(self.variable_frame, text='y', width=8).grid(row=0, column=2)
			self.pos2 = ttk.Entry(self.variable_frame, width=4,textvariable=self.y)
			self.pos2.grid(row=0, column=3)

			tk.Label(self.variable_frame, text='width', width=8).grid(row=1, column=0)
			self.pos3 = ttk.Entry(self.variable_frame, width=4,textvariable=self.x1)
			self.pos3.grid(row=1, column=1)

			tk.Label(self.variable_frame, text='height', width=8).grid(row=1, column=2)
			self.pos4 = ttk.Entry(self.variable_frame, width=4,textvariable=self.y1)
			self.pos4.grid(row=1, column=3)

			self.posbtn1 = ttk.Button(self.variable_frame, text='Update Rect', command=self.update_rect)
			self.posbtn1.grid(row=2,column=0, columnspan=2, pady=5)

			self.posbtn2 = ttk.Button(self.variable_frame, text='Clear Rect', command=self.clear_rect)
			self.posbtn2.grid(row=2,column=2, columnspan=2, pady=5)

			ttk.Button(self.variable_frame, text='Cut Tile', command=self.cut_tiles_by_rect).grid(
							row=3,column=0, columnspan=4)

			self.pos1.config(state=tk.DISABLED)
			self.pos2.config(state=tk.DISABLED)
			self.pos3.config(state=tk.DISABLED)
			self.pos4.config(state=tk.DISABLED)
			self.posbtn1.config(state=tk.DISABLED)
			self.posbtn2.config(state=tk.DISABLED)

	def resize_frame(self):
		for id_ in self.lines:
			self.canvas.delete(id_)
			self.lines.clear()

		for widget in self.editor_frame.winfo_children():
			widget.destroy()

		self.imwidth.set(100)
		self.imheight.set(100)

		tk.Label(self.editor_frame, text=f'Current Size : {self.original_imsize[0]}x{self.original_imsize[1]}'
			).grid(row=0, column=0, columnspan=2, pady=5, padx=35)

		tk.Label(self.editor_frame, text='width', width=8).grid(row=1, column=0, pady=(10,5))
		ttk.Entry(self.editor_frame, width=4,textvariable=self.imwidth
					).grid(row=1, column=1, pady=(10,0))
		tk.Label(self.editor_frame, text='height', width=8).grid(row=2, column=0)
		ttk.Entry(self.editor_frame, width=4,textvariable=self.imheight
					).grid(row=2, column=1)

		ttk.Button(self.editor_frame, text='Resize', command=self.resize_image).grid(
					row=3, column=0, columnspan=2, pady=(10,0))

		ttk.Button(self.editor_frame, text='Undo', command=self.undo).grid(
					row=4, column=0, columnspan=2, pady=(10,0))

		ttk.Button(self.editor_frame, text='Save', command=self.save_resize).grid(
					row=5, column=0, columnspan=2, pady=(10,0))

		ttk.Button(self.editor_frame, text='Back', command=self.back).grid(
					row=6, column=0, columnspan=2, pady=(10,0))

	def open_img(self):
		filetypes = (("Images","*.png .jpg"),)
		path = filedialog.askopenfilename(initialdir=cwd, filetypes=filetypes)
		if path:
			self.filepath = path
			self.imobject = ImageProcessor(self.filepath)
			self.image, size = self.imobject.display_image()
			self.original_imsize = tuple(size)
			self.canvas.create_image(0, 0, anchor='nw', image=self.image)

			self.header['text'] = os.path.basename(self.filepath)
			self.size['text'] = f'{size[0]}x{size[1]}'

			region = self.canvas.bbox(tk.ALL)
			self.canvas.configure(scrollregion=region)

			self.resize.config(state=tk.NORMAL)
			self.scaler.grid(row=2, column=0, columnspan=2, pady=5)

	def do_zoom(self, event=None):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		factor = self.zoom_val.get()
		self.image = self.imobject.zoom(factor)
		self.canvas.create_image(0, 0, anchor='nw', image=self.image)

		region = list(self.canvas.bbox(tk.ALL))
		if region[-2] <= self.original_imsize[0]:
			region[-2] = self.image.width() + 10
		if region[-1] <= self.original_imsize[1]:
			region[-1] = 480
		self.canvas.configure(scrollregion=tuple(region))

	def draw_tiles(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		tile_width = self.tilewidth.get()
		tile_height = self.tileheight.get()

		if (tile_width or tile_height) and self.image:
			im_width = self.image.width()
			im_height = self.image.height()

			x, y = 0, 0

			if tile_height:
				rows = int(im_height / tile_height)
				for _ in range(rows+1):
					id_ = self.canvas.create_line(0,y,im_width, y, fill='dodgerblue3')
					self.lines.append(id_)
					y += tile_height
			if tile_width:
				cols = int(im_width / tile_width)
				for _ in range(cols+1):
					id_ = self.canvas.create_line(x,0,x, im_height, fill='dodgerblue3')
					self.lines.append(id_)
					x += tile_width

	def draw_rc(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		rows = self.rows.get()
		cols= self.columns.get()
		print(rows,cols)

		if (rows or cols) and self.image:
			im_width = self.image.width()
			im_height = self.image.height()

			x, y = 0, 0

			if rows:
				r = int(im_height / rows)
				for _ in range(rows+1):
					id_ = self.canvas.create_line(0,y,im_width, y, fill='dodgerblue3')
					self.lines.append(id_)
					y += r
			if cols:
				c = int(im_width / cols) 
				for _ in range(cols+1):
					id_ = self.canvas.create_line(x,0,x, im_height, fill='dodgerblue3')
					self.lines.append(id_)
					x += c

	def draw_rect(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		x = self.x.get()
		y = self.y.get()
		width_ = self.tilewidth.get()
		height = self.tileheight.get()

		id_ = self.canvas.create_rectangle(x,y, x+width_, y+height, outline='dodgerblue3', width=2)
		self.lines.append(id_)

	def update_rect(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		x = self.x.get()
		y = self.y.get()
		x1 = self.x1.get()
		y1 = self.y1.get()

		id_ = self.canvas.create_rectangle(x,y, x1, y1, outline='dodgerblue3', width=2)
		self.lines.append(id_)

	def clear_rect(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		self.pos1.config(state=tk.DISABLED)
		self.pos2.config(state=tk.DISABLED)
		self.pos3.config(state=tk.DISABLED)
		self.pos4.config(state=tk.DISABLED)
		self.posbtn1.config(state=tk.DISABLED)
		self.posbtn2.config(state=tk.DISABLED)

		self.first = None
		self.second = None

	def _get_position(self, event=None):
		x, y = event.x, event.y
		opt = self.crop_option.get()
		if opt in (1,2,3):
			self.canvas.scan_mark(event.x, event.y)
			self.drag = True
		else:
			if self.image:
				self.drag = False
				
				if not self.first:
					self.first = (event.x, event.y)
					self.x.set(event.x)
					self.y.set(event.y)

					id_ = self.canvas.create_oval(x-1,y-1,x+2,y+2, fill='dodgerblue3')
					self.lines.append(id_)
					self.posbtn2.config(state=tk.NORMAL)
				else:
					self.pos1.config(state=tk.NORMAL)
					self.pos2.config(state=tk.NORMAL)
					self.pos3.config(state=tk.NORMAL)
					self.pos4.config(state=tk.NORMAL)
					self.posbtn1.config(state=tk.NORMAL)

					self.second = (event.x, event.y)
					self.x1.set(event.x)
					self.y1.set(event.y)

					self.update_rect()

	def cut_tiles_by_tile(self):
		if self.image:
			imwidth = self.image.width()
			imheight = self.image.height()
			twidth = self.tilewidth.get()
			theight = self.tileheight.get()

			self.imobject.dividebytile(imwidth, imheight,twidth, theight)

	def cut_tiles_by_rc(self):
		if self.image:
			imwidth = self.image.width()
			imheight = self.image.height()
			rows = self.rows.get()
			columns = self.columns.get()

			if rows == 0:
				rows = 1
			if columns == 0:
				columns = 1

			self.imobject.dividebyrc(imwidth, imheight,rows, columns)

	def cut_tiles_custom(self):
		if self.image:
			imwidth = self.image.width()
			imheight = self.image.height()
			x = self.x.get()
			y = self.y.get()
			width_ = self.tilewidth.get()
			height = self.tileheight.get()

			if width_ and height:
				self.imobject.dividecustom(imwidth, imheight, x, y, width_, height)

	def cut_tiles_by_rect(self):
		if self.image:
			imwidth = self.image.width()
			imheight = self.image.height()
			x = self.x.get()
			y = self.y.get()
			x1 = self.x1.get()
			y1 = self.y1.get()

			if x and y and x1 and y1:
				self.imobject.dividebyrect(imwidth, imheight, x, y, x1, y1)

	def resize_image(self, save=False):
		width = self.imwidth.get()
		height = self.imheight.get()

		self.image, self.imsize = self.imobject.resize_image(width, height, save)
		self.original_imsize = tuple(self.imsize)
		self.canvas.create_image(0, 0, anchor='nw', image=self.image)

		region = self.canvas.bbox(tk.ALL)
		self.canvas.configure(scrollregion=region)

	def undo(self):
		self.image, self.imsize = self.imobject.display_image()
		self.original_imsize = tuple(self.imsize)
		self.canvas.create_image(0, 0, anchor='nw', image=self.image)

		region = self.canvas.bbox(tk.ALL)
		self.canvas.configure(scrollregion=region)

	def save_resize(self):
		self.resize_image(save=True)

	def back(self):
		for widget in self.editor_frame.winfo_children():
			widget.destroy()

		self.draw_editor()
		self.draw_header_frame()
		self.draw_menu_frame()

		self.header['text'] = os.path.basename(self.filepath)
		self.size['text'] = f'{self.original_imsize[0]}x{self.original_imsize[1]}'

	def _drag(self, event=None):
		if self.drag:
			self.canvas.scan_dragto(event.x, event.y, gain=1)

	def _bound_to_mousewheel(self, event):
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

	def _unbound_to_mousewheel(self, event):
		self.canvas.unbind_all("<MouseWheel>") 

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

	def _go_up(self, event):
		self.canvas.yview_scroll(-1, "units")

	def _go_down(self, event):
		self.canvas.yview_scroll(1, "units")

	def _yview(self, *args):
		if self.canvas.yview() == (0.0, 1.0):
			return self.canvas.yview(*args)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('800x500+200+100')
	root.title('Sprite Cutter')
	root.resizable(0,0)

	app = Application(master=root)
	app.mainloop()