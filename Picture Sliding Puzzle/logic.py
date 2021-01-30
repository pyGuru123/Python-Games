# In general, for a given grid of width N, we can find out check if a N*N – 1
# puzzle is solvable or not by following below simple rules : 
 
# 1. If N is odd, then puzzle instance is solvable if number of inversions
#	 is even in the input state.
# 2. If N is even, puzzle instance is solvable if 
#	 * the blank is on an even row counting from the bottom
#	   (second-last, fourth-last, etc.) and number of inversions is odd.
#    * the blank is on an odd row counting from the bottom
#       (last, third-last, fifth-last, etc.) and number of inversions is even.
# For all other cases, the puzzle instance is not solvable.

# Read detailed info here : https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

solved_array = list(range(1,16))

def isSolvable(arr):
	inversions = 0 # Number of inversions in the array
	width = 4      # width of the puzzle 
	row = 0        
	blankrow = 0   # row on which empty cell exists

	for i in range(0, len(arr)):
		if i % width == 0:
			row += 1 # move to the next row
		if arr[i] == 0:
			blankrow = row # empty cell exists on this row
			continue

		for j in range(i+1, len(arr)):
			if arr[i] > arr[j] & arr[j] != 0:
				inversions += 1

	if width % 2 == 0:
		if blankrow % 2 == 0:
			return inversions % 2 == 0
		else:
			return inversions % 2 != 0
	else:
		return inversions % 2 == 0

def isSolved(arr):
	return solved_array == arr[:15]