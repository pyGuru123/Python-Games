import random
from pprint import pprint
from functools import partial
from datetime import datetime

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter import messagebox

msg = 'Click a square, you get a number.\
That number is the number of how many mines are surrounding it.\
If you find the mine, you can open "unopened" squares around it, opening more areas.'

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.level = tk.StringVar(value='easy')
		self.level_dict = {'easy':'easy', 'medium':'medium', 'hard':'hard'}
		self.mine_dict = {'easy':10, 'medium':12, 'hard':15}

		self.highscore = 0

		self.draw_main_frame()

	def draw_main_frame(self):
		self.main_frame = tk.Frame(self, width=345, height=485)
		self.main_frame.grid(row=0, column=0)
		self.main_frame.grid_propagate(False)

		self.logo = tk.Label(self.main_frame, image=minesweeper_logo)
		self.logo.grid(row=0, column=0, columnspan=6, padx=22, pady=40)

		self.level_frame = tk.LabelFrame(self.main_frame, text='Select Level ', 
			width=250, height=60, fg='dodgerblue3', font=('verdana', 10))
		self.level_frame.grid(row=2, column=1, columnspan=4, pady=15)
		self.level_frame.grid_propagate(False)

		i = 0
		for text, value in self.level_dict.items():
			tk.Radiobutton(self.level_frame, text=text, value=value, 
					variable=self.level).grid(row=0, column=i, pady=6, padx=7)
			i += 1

		self.start_btn = ttk.Button(self.main_frame, text='Start Game', width=15,
					command=self.start_playing)
		self.start_btn.grid(row=3, column=2, columnspan=2, pady=10)

		self.help_btn = ttk.Button(self.main_frame, text='Help', width=15,
					command=self.help_window)
		self.help_btn.grid(row=4, column=2, columnspan=2, pady=10)

		self.quit_btn = ttk.Button(self.main_frame, text='Quit', width=15,
					command=self.master.destroy)
		self.quit_btn.grid(row=5, column=2, columnspan=2, pady=10)


	def draw_game_frames(self):
		self.header_frame = tk.Frame(self, width=345, height=85)
		self.body_frame = tk.LabelFrame(self, width=345, height=400, bg='gray70',
						relief=tk.RIDGE)

		self.header_frame.grid(row=0, column=0)
		self.body_frame.grid(row=1, column=0)

		self.header_frame.grid_propagate(False)
		self.body_frame.grid_propagate(False)

	def draw_header_frame(self):
		self.score_frame = tk.LabelFrame(self.header_frame, width=130, height=85, bg='dodgerblue',
					relief=tk.FLAT)
		self.score_frame.grid(row=0, column=0, rowspan=2)

		self.current_score_frame = tk.Frame(self.score_frame, width=80, height=85, bg='white')
		self.current_score_frame.grid(row=0, column=0, rowspan=2)

		self.highscore_frame = tk.Frame(self.score_frame, width=50, height=41, bg='white')
		self.highscore_frame.grid(row=1, column=1, sticky='W')

		self.timer_frame = tk.Frame(self.header_frame, width=215, height=35, bg='dodgerblue')
		self.timer_frame.grid(row=0, column=1)

		self.others = tk.Frame(self.header_frame, width=215, height=50, bg='white')
		self.others.grid(row=1, column=1)

		self.score_frame.grid_propagate(False)
		self.current_score_frame.grid_propagate(False)
		self.highscore_frame.grid_propagate(False)
		self.timer_frame.grid_propagate(False)
		self.others.grid_propagate(False)

		self.score_label = tk.Label(self.current_score_frame, font=('verdana', 42, 'bold'),
						fg='dodgerblue3', text='0', width=2, bg='white')
		self.score_label.grid(row=0, column=0, pady=8)

		self.highscore_label = tk.Label(self.highscore_frame, font=('verdana', 24), fg='#E8175D',
						text=self.highscore, width=2, bg='white', anchor='w')
		self.highscore_label.grid(row=0, column=0, pady=2)

		self.timer_label = tk.Label(self.timer_frame, font=('verdana', 14), fg='black',
						text='00:00:00', width=10, bg='white')
		self.timer_label.grid(row=0, column=0, padx=55, pady=3)

		self.others_label = tk.Label(self.others, font=('verdana', 12), fg='black',
						width=10, bg='white')
		self.others_label.grid(row=0, column=0, pady=14, padx=110)

	def start_playing(self):
		self.main_frame.destroy()

		self.draw_game_frames()
		self.draw_header_frame()

		self.score = 0
		self.buttons_list = []
		self.draw_cells()

		m = self.level.get()
		self.numMines = self.mine_dict[m]
		self.others_label['text'] = f'Mines : {self.numMines}'
		self.start_game()
		
	def draw_cells(self):
		for row in range(9):
			buttons = []
			for col in range(9):
				if row == 0:
					pady = 3
				else:
					pady = 0
				btn = tk.Button(self.body_frame, text=f'', width=2, height=1,
						relief=tk.RAISED, command = partial(self.check_cell, row, col),
						highlightthickness=4, fg='blue', font=('verdana'),
						highlightcolor="#37d3ff", 
						highlightbackground="#37d3ff", 
						borderwidth=3)
				btn.grid(row=row, column=col, padx=(0,0), pady=(pady,0))
				buttons.append(btn)
			self.buttons_list.append(buttons)

	def start_game(self):
		self.board = [[' ' for i in range(9)] for j in range(9)]
		self.mines = []

		self.first_Move = True
		self.gameRunning = True
		self.score = 0

		self.place_mines(self.numMines)

		self.start_time = datetime.now()
		self.timer_label['text'] = '00:00:00'
		self.after(1000, self.update_timer)

	def place_mines(self, num):
		if num > 0:
			x = random.randint(0, 8)
			y = random.randint(0, 8)

			if (x,y) in self.mines:
				self.place_mines(num)
			else:
				self.board[x][y] = 'X'
				self.mines.append((x,y))
				self.place_mines(num-1)

	def check_cell(self, x, y):
		btn = self.buttons_list[x][y]
		if btn['relief'] == tk.RAISED:
			btn.config(relief=tk.FLAT)
			btn['bg'] = 'gray'

			if self.isMine(x, y):
				if self.first_Move:
					self.board[x][y] = ' '
					self.mines.remove((x,y))
					self.place_mines(1)
					self.first_Move = False

					self.updateAdjecentCells(btn, x, y)
					self.update_score(1)
				else:
					btn.config(width=24, height=26)
					btn['bg'] = 'red'
					btn['image'] = mine_icon
					self.showAllMines()	
					self.game_lost()
			else:
				self.first_Move = False
				self.updateAdjecentCells(btn, x, y)
				self.update_score(1)

	def isMine(self, row, col):
		return True if (row, col) in self.mines else False

	def isValidCell(self, row, col):
		return ((row >= 0 and row < 9) and (col >= 0 and col < 9))

	def updateAdjecentCells(self, btn, row, col):
		num = self.checkAdjecentCells(row, col)
		if num:
			if num == 1:
				color = 'green'
			elif num == 2:
				color = 'blue'
			elif num >=3:
				color = 'red'
			btn['fg'] = color
			btn['text'] = str(num)

	def update_score(self, point):
		self.score += point
		self.score_label['text'] = self.score
		if self.score >= self.highscore:
			self.highscore = self.score
			self.highscore_label['text'] = self.highscore

	def update_timer(self):
		if self.gameRunning:
			now =  datetime.now()
			minutes, seconds = divmod((now - self.start_time).total_seconds(),60)
			string = f"00:{int(minutes):02}:{round(seconds):02}"
			self.timer_label['text'] = string
			self.after(1000, self.update_timer)

	def checkAdjecentCells(self, row, col):
		mine = 0
		cell_list = []
		for i in range(row-1, row+2):
			for j in range(col-1, col+2):
				if not (row == i and col == j):
					if self.isValidCell(i, j):
						cell_list.append((i,j))
						if self.isMine(i,j):
							mine += 1

		if mine == 0:
			score = 0
			for x,y in cell_list:
				btn = self.buttons_list[x][y]
				if btn['relief'] == tk.RAISED:
					btn.config(relief=tk.FLAT)
					btn['bg'] = 'gray'
					score += 1
			self.update_score(score)
		else:
			return mine

	def showAllMines(self):
		for x,y in self.mines:
			btn = self.buttons_list[x][y]
			if btn['relief'] == tk.RAISED:
				btn.config(relief=tk.FLAT)
				btn['bg'] = 'red'

				btn.config(width=24, height=26)
				btn['image'] = mine_icon

	def redraw_body_frame(self):
		self.body_frame.destroy()
		self.body_frame = tk.LabelFrame(self, width=345, height=400, bg='gray70',
						relief=tk.RIDGE)
		self.body_frame.grid(row=1, column=0)
		self.body_frame.grid_propagate(False)
		
		self.score = 0
		self.buttons_list = []
		self.draw_cells()
		self.start_game()

	def game_lost(self):
		self.gameRunning = False
		self.game_lost_window()

	def restart_game(self):
		self.top.destroy()
		self.start_game()
		self.after(100, self.redraw_body_frame)
		self.score_label['text'] = 0

	def go_home(self):
		self.top.destroy()
		self.highscore = 0

		self.header_frame.destroy()
		self.body_frame.destroy()
		self.draw_main_frame()

	def game_lost_window(self):
		self.top = tk.Toplevel(self)
		self.top.geometry('200x100+580+355')
		self.top.title('Minesweeper')
		self.top.resizable(0,0)
		self.top.protocol("WM_DELETE_WINDOW", self.master.destroy)

		tk.Label(self.top, text=' You Lost', image=sad_face, fg='black',
				font=('verdana', 10, 'bold'), compound=tk.LEFT,
				).grid(row=0, column=0, padx=50, pady=5,
						columnspan=4)

		ttk.Button(self.top, text='Play Again', command=self.restart_game, 
				width=10).grid(row=1,column=0, columnspan=2, pady=15)

		ttk.Button(self.top, text='Home', command=self.go_home, 
				width=8).grid(row=1,column=2, columnspan=2, pady=15)

	def help_window(self):
		win = tk.Toplevel(self)
		win.geometry('200x120+580+355')
		win.title('Minesweeper')
		win.resizable(0,0)

		tk.Label(win, text=msg, wraplength=180, anchor='w').grid(row=0, column=0, padx=10, pady=4)

if __name__ == '__main__':
	root = tk.Tk()
	ttk.Style().theme_use('clam')
	root.title('Minesweeper')
	root.geometry('345x450+500+150')

	mine_icon = PhotoImage(file='icons/mine.png')
	minesweeper_logo = PhotoImage(file='icons/logo.png')
	sad_face = PhotoImage(file='icons/sad.png')

	app = Application(master=root)
	app.mainloop()