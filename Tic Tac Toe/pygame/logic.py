def check_space(cell):
	return cell == ' '

def isBoardFull(board):
	for cell in board:
		if check_space(cell):
			return False

	return True

def check_win(board, mark):
	if (board[1] == board[2] == board[3] == mark):
		value = (True, '123')
	elif (board[4] == board[5] == board[6] == mark):
		value = (True, '456')
	elif (board[7] == board[8] == board[9] == mark):
		value = (True, '789')
	elif (board[7] == board[4] == board[1] == mark):
		value = (True, '147')
	elif (board[8] == board[5] == board[2] == mark):
		value = (True, '258')
	elif (board[9] == board[6] == board[3] == mark):
		value = (True, '369') 
	elif (board[1] == board[5] == board[9] == mark):
		value = (True, '159')
	elif (board[3] == board[5] == board[7] == mark):
		value = (True, '357')
	else:
		value = (False, -1)

	return value