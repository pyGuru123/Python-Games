import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter import messagebox
from datetime import datetime

from logic import isSolvable, isSolved
from game_over_screen import GameWon

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.gridCells = []
		self.imgType = tk.StringVar()
		self.imgType.set('car')
		self.numMoves = 0
		self.firstMove = True
		self.timer_id = None

		self.imgDict = {'car':car_list, 'rain':rain_list, 'superhero':superhero_list,
					'universe':universe_list, 'nature':nature_list, 'night':night_list}
		self.solDict = {'car':car_sol, 'rain':rain_sol, 'superhero':superhero_sol,
					'universe':universe_sol, 'nature':nature_sol, 'night':night_sol}

		self.draw_header()
		self.draw_body()

		self.master.bind('<Up>', self.up)
		self.master.bind('<Down>', self.down)
		self.master.bind('<Left>', self.left)
		self.master.bind('<Right>', self.right)

		self.imgType.trace_add('write', self.new_game)

	def draw_header(self):
		self.header = tk.LabelFrame(self, width=400, height=100, bg='white', relief=tk.SUNKEN)
		self.header.grid()
		self.header.grid_propagate(False)

		self.reset_btn = tk.Button(self.header, image=refresh_icon,
				relief=tk.FLAT, command=self.new_game, bg='white')
		self.reset_btn.grid(row=0, column=0, padx=(30,10), pady=0)

		self.options = ttk.OptionMenu(self.header, self.imgType, 'car', *self.imgDict.keys())
		self.options.config(width=10)
		self.options.grid(row=0, column=1, padx=(30,10), pady=10)
		
		# self.options.bind("<Configure>", self.new_game)

		self.hint_btn = tk.Button(self.header, image=hint_icon,
				relief=tk.FLAT, command=self.show_solution, bg='white')
		self.hint_btn.grid(row=0, column=2, padx=(30,10), pady=0)

		self.timer_label = tk.Label(self.header, font=('verdana', 14), fg='black',
						text='00:00:00', width=10, bg='white')
		self.timer_label.grid(row=1, column=0, columnspan=3)

		self.movesFrame = tk.LabelFrame(self.header, width=100, height=100, bg='gray')
		self.movesFrame.grid(row=0, column=3, rowspan=2)
		self.movesFrame.grid_propagate(False)

		self.movesLabel = tk.Label(self.movesFrame, bg='gray', fg='white', text=self.numMoves,
						font='verdana 24', width=5, height=2)
		self.movesLabel.grid(row=0, column=0)

		self.sbody = tk.Frame(self, width=400, height=400)
		self.slabel = tk.Label(self.sbody, image=self.solDict[self.imgType.get()])
		self.slabel.grid(row=0, column=0)

	def draw_body(self):
		self.body = tk.Frame(self, width=400, height=400)
		self.body.grid()
		self.body.grid_propagate(False)

		self.create_board(self.imgType.get())

	def create_board(self, im_type):
		self.array = [i for i in range(1,16)] + [0]
		random.shuffle(self.array)
		while not isSolvable(self.array):
			random.shuffle(self.array)

		self.emptyCell = self.array.index(0)
		img_list = self.imgDict[im_type]
		self.imgMatrix = [img_list[index-1] if index else None for index in self.array]

		for index, img in enumerate(self.imgMatrix):
				frame = tk.Frame(self.body, width=100, height=100)
				frame.grid(row=index//4, column=index%4)
				frame.grid_propagate(False)

				if img:
					lbl = tk.Label(frame, image=img)
				else:
					img = white_bg
					lbl = tk.Label(frame, image=img)

				lbl.grid()
				lbl.bind('<Button-1>', lambda event, pos=index: self.move(pos))
				self.gridCells.append(lbl)

	def new_game(self, *args):
		self.body.destroy()

		self.numMoves = 0
		self.movesLabel['text'] = self.numMoves
		self.firstMove = True
		self.gridCells = []

		if self.timer_id:
			self.after_cancel(self.timer_id)
			self.timer_label['text'] = '00:00:00'
		# self.start_time = datetime.now()

		self.draw_body()

	def move(self, pos):
		# print(pos)
		
		if self.imgMatrix[pos]:
			for num in (-1, 1, -4, 4):
				index = num + pos
				if index == self.emptyCell and (pos % 4 - (index % 4) in (-1,0,1)):
					self.swap_cell(pos, index)
					self.emptyCell = pos
					self.update_state()

	def up(self, event=None):
		if self.emptyCell - 4 >= 0:
			self.swap_cell(self.emptyCell, self.emptyCell - 4)
			self.emptyCell -= 4
			self.update_state()

	def down(self, event=None):
		if self.emptyCell + 4 <= 15:
			self.swap_cell(self.emptyCell, self.emptyCell + 4)
			self.emptyCell += 4
			self.update_state()

	def left(self, event=None):
		row_changed = self.emptyCell // 4 == (self.emptyCell - 1) // 4
		if 0 <= (self.emptyCell - 1) % 4 < 4 and row_changed:
			self.swap_cell(self.emptyCell, self.emptyCell - 1)
			self.emptyCell -= 1
			self.update_state()

	def right(self, event=None):
		row_changed = self.emptyCell // 4 == (self.emptyCell + 1) // 4
		if 0 <= (self.emptyCell + 1) % 4 < 4 and row_changed:
			self.swap_cell(self.emptyCell, self.emptyCell + 1)
			self.emptyCell += 1
			self.update_state()

	def swap_cell(self, p1, p2):
		if self.firstMove:
			self.start_time = datetime.now()
			self.firstMove = False
			self.timer_id = self.after(1000, self.update_timer)

		self.imgMatrix[p1], self.imgMatrix[p2] = self.imgMatrix[p2], self.imgMatrix[p1]
		self.array[p1], self.array[p2] = self.array[p2], self.array[p1]
		self.update_moves()

		if isSolved(self.array):
			GameWon(self.master, self.numMoves, self.new_game)

	def update_state(self):
		for index, img in enumerate(self.imgMatrix):
			if img:
				self.gridCells[index]['image'] = img
			else:
				self.gridCells[index]['image'] = white_bg
		self.update_idletasks()

	def update_moves(self):
		self.numMoves += 1
		self.movesLabel['text'] = self.numMoves

	def update_timer(self):
		now =  datetime.now()
		minutes, seconds = divmod((now - self.start_time).total_seconds(),60)
		string = f"00:{int(minutes):02}:{round(seconds):02}"
		self.timer_label['text'] = string
		self.timer_id = self.after(1000, self.update_timer)

	def show_solution(self):
		self.body.grid_forget()
		self.sbody.grid()
		self.slabel['image'] = self.solDict[self.imgType.get()]
		self.reset_btn.config(state=tk.DISABLED)
		self.hint_btn.config(state=tk.DISABLED)
		self.after(1000, self.hide_solution)

	def hide_solution(self):
		self.sbody.grid_forget()
		self.body.grid()
		self.reset_btn.config(state=tk.NORMAL)
		self.hint_btn.config(state=tk.NORMAL)


# https://www.imgonline.com.ua/eng/cut-photo-into-pieces.php
# https://stackoverflow.com/questions/34570344/check-if-15-puzzle-is-solvable
# https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Picture Puzzle')
	root.geometry('400x500+450+130')

	white_bg = PhotoImage(file='icons/white_bg.png') 
	refresh_icon = PhotoImage(file='icons/refresh.png')
	hint_icon = PhotoImage(file='icons/hint.png')
	solved_icon = PhotoImage(file='icons/solved.png')

	rain_list = [PhotoImage(file=f'images/rain/img{index}.png') for index in range(1,17)]
	car_list = [PhotoImage(file=f'images/car/img{index}.png') for index in range(1,17)]
	nature_list = [PhotoImage(file=f'images/nature/img{index}.png') for index in range(1,17)]
	night_list = [PhotoImage(file=f'images/night/img{index}.png') for index in range(1,17)]
	superhero_list = [PhotoImage(file=f'images/superhero/img{index}.png') for index in range(1,17)]
	universe_list = [PhotoImage(file=f'images/universe/img{index}.png') for index in range(1,17)]

	rain_sol = PhotoImage(file='images/rain_resized.png')
	car_sol = PhotoImage(file='images/car_resized.png')
	nature_sol = PhotoImage(file='images/nature_resized.png')
	night_sol = PhotoImage(file='images/night_resized.png')
	superhero_sol = PhotoImage(file='images/superhero_resized.png')
	universe_sol = PhotoImage(file='images/universe_resized.png')

	app = Application(master=root)
	app.mainloop()