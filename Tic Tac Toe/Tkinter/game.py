import random
import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.board = ['#'] + [' ' for i in range(9)]
		self.x_score = 0
		self.o_score = 0

		self.players = ['X', 'O']
		self.current_player = random.randint(0,1)

		self.line_dict = {'123':[50,50,250,50], '456':[50,150,250,150], '789':[50,250,250,250],
						  '147':[50,50,50,250], '258':[150,50,150,250], '369':[250,50,250,250],
						  '159':[50,50,250,250],'357':[250,50,50,250]}

		self.draw_header_frame()
		self.draw_body_frame()

	def draw_header_frame(self):
		self.header = tk.Frame(self, width=300, height=100)
		self.header.grid(row=0, column=0)
		self.header.grid_propagate(False)

		self.score_frame = tk.Frame(self.header, width=300, height=50)
		self.score_frame.grid(row=0, column=0)
		self.score_frame.grid_propagate(False)

		self.player_frame = tk.Frame(self.header, width=300, height=50)
		self.player_frame.grid(row=1, column=0)
		self.player_frame.grid_propagate(False)

		self.x_label = tk.Label(self.score_frame, text=f'X   {self.x_score}', fg='dodgerblue3',
						 font=('Papyrus', 18, 'bold'))
		self.x_label.grid(row=0, column=0, padx=20, pady=5)

		self.o_label = tk.Label(self.score_frame, text=f'O   {self.o_score}', fg='dodgerblue3',
						 font=('Papyrus', 18, 'bold'))
		self.o_label.grid(row=0, column=3, padx=110, pady=5)

		current = self.players[self.current_player]
		self.player_label = tk.Label(self.player_frame, text=f'Current Player : {current}', fg='green',
						 font=('verdana', 12, 'bold'))
		self.player_label.grid(row=0, column=3, padx=60, pady=15)

	def draw_body_frame(self):
		self.body = tk.Frame(self, width=300, height=300)
		self.body.grid(row=1, column=0)
		self.body.grid_propagate(False)

		self.canvas = tk.Canvas(self.body, width=300, height=300, bg='gray')
		self.canvas.grid()

		self.canvas.create_line([100, 10, 100, 290], width=4, fill='black')
		self.canvas.create_line([200, 10, 200, 290], width=4, fill='black')
		self.canvas.create_line([10, 100, 290, 100], width=4, fill='black')
		self.canvas.create_line([10, 200, 290, 200], width=4, fill='black')

		self.canvas.bind('<Button-1>', self.draw_text)

	def draw_text(self, event):
		x, y = event.x, event.y
		pos, cell = self.get_text_pos((x, y))
		if self.check_space(cell):
			self.board[cell] = self.players[self.current_player]
			self.write_text(pos, text = self.players[self.current_player])

			if self.check_winner('X'):
				self.x_score += 1
				self.x_label['text'] = f'X   {self.x_score}'
				self.after(800, lambda : self.game_over_window('   X Won'))
			elif self.check_winner('O'):
				self.o_score += 1
				self.o_label['text'] = f'O   {self.o_score}'
				self.after(800, lambda : self.game_over_window('   O Won'))

			if self.isBoardFull():
				self.after(800, lambda : self.game_over_window(' Game Draw'))
			else:
				self.current_player = (self.current_player + 1) % 2
				self.player_label['text'] = f'Current Player : {self.players[self.current_player]}'


	def write_text(self, pos, text):
		self.canvas.create_text(pos,  text=text, font='Chiller 50 bold', fill="white")

	def check_space(self, pos):
		return self.board[pos] == ' '

	def isBoardFull(self):
		is_full = ' ' in self.board
		return not is_full

	def check_winner(self, mark):
		ch = self.check_win(mark)
		if ch[0]:
			line = ch[1]
			pos = self.line_dict[line]
			self.canvas.create_line(pos, width=5, fill='white')
			return True
		else:
			return False

	def check_win(self, mark):
		if (self.board[1] == self.board[2] == self.board[3] == mark):
			value = (True, '123')
		elif (self.board[4] == self.board[5] == self.board[6] == mark):
			value = (True, '456')
		elif (self.board[7] == self.board[8] == self.board[9] == mark):
			value = (True, '789')
		elif (self.board[7] == self.board[4] == self.board[1] == mark):
			value = (True, '147')
		elif (self.board[8] == self.board[5] == self.board[2] == mark):
			value = (True, '258')
		elif (self.board[9] == self.board[6] == self.board[3] == mark):
			value = (True, '369') 
		elif (self.board[1] == self.board[5] == self.board[9] == mark):
			value = (True, '159')
		elif (self.board[3] == self.board[5] == self.board[7] == mark):
			value = (True, '357')
		else:
			value = (False, -1)

		return value

	def get_text_pos(self, pos):
		x, y = pos

		# in first row
		if (x > 0 and x < 100) and (y > 0 and y < 100):
			position = ((50, 50), 1)
		elif (x > 100 and x < 200) and (y > 0 and y < 100):
			position = ((150, 50), 2)
		elif (x > 200 and x < 300) and (y > 0 and y < 100):
			position = ((250, 50), 3)

		# in second row
		elif (x > 0 and x < 100) and (y > 100 and y < 200):
			position = ((50, 150), 4)
		elif (x > 100 and x < 200) and (y > 100 and y < 200):
			position = ((150, 150), 5)
		elif (x > 200 and x < 300) and (y > 100 and y < 200):
			position = ((250, 150), 6)

		# in third row
		elif (x > 0 and x < 100) and (y > 200 and y < 300):
			position = ((50, 250), 7)
		elif (x > 100 and x < 200) and (y > 200 and y < 300):
			position = ((150, 250), 8)
		elif (x > 200 and x < 300) and (y > 200 and y < 300):
			position = ((250, 250), 9)

		return position

	def restart_game(self):
		self.top.destroy()

		self.canvas.delete('all')
		self.body.destroy()

		self.board = ['#'] + [' ' for i in range(9)]
		self.draw_body_frame()

		self.current_player = random.randint(0,1)
		self.player_label['text'] = f'Current Player : {self.players[self.current_player]}'


	def game_over_window(self, msg):
		self.top = tk.Toplevel(self)
		self.top.geometry('200x100+500+380')
		self.top.title('Tic Tac Toe')
		self.top.resizable(0,0)
		self.top.protocol("WM_DELETE_WINDOW", self.master.destroy)

		tk.Label(self.top, text=msg, fg='black', font=('verdana', 12, 'bold')
				).grid(row=0, column=0, padx=40, pady=5, columnspan=3)

		ttk.Button(self.top, text='Play Again', command=self.restart_game, 
				width=10).grid(row=1, column=0, columnspan=2, pady=20, padx=20)

		ttk.Button(self.top, text='Quit', command=self.master.destroy, 
				width=8).grid(row=1, column=2, pady=20, padx=10)

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Tic Tac Toe')
	root.resizable(0,0)
	root.geometry('300x400+450+200')

	app = Application(master=root)
	app.mainloop()