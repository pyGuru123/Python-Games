import math

def convert_to_pygame(pos):
	return int(pos.x), int(-pos.y + HEIGHT)

def vector(a, b):
	dx = b[0] - a[0]
	dy  = b[1] - a[1]
	return dx, dy

def distance(a, b):
	dx, dy = vector(a, b)
	return math.sqrt(dx**2 + dy**2)

def unit_vector(v):
	''' unit vector = vector / magnitude of vector '''
	magnitude = math.sqrt(v[0] ** 2 + v[1] ** 2)
	if magnitude == 0:
		magnitude = 0.0000000000001

	unit_p = v[0] / magnitude
	unit_q = v[1] / magnitude

	return unit_p, unit_q