import turtle
import winsound

# Window properties
win = turtle.Screen()
win.title('Pong')
win.bgcolor('green')
win.setup(width=800,height=600)
win.tracer(0)

def drawField():
	draw = turtle.Turtle()
	draw.penup()
	draw.speed(0)
	draw.color('white')
	draw.hideturtle()
	draw.goto(-390,295)
	draw.pendown()
	for i in range(2):
		draw.forward(770)
		draw.right(90)
		draw.forward(580)
		draw.right(90)
	draw.goto(0,295)
	draw.right(90)
	draw.goto(0,-285)
	draw.penup()
	draw.goto(-50,0)
	draw.pendown()
	draw.circle(50)

drawField()

# Scores
scoreA = 0
scoreB = 0

# Paddle A
padA = turtle.Turtle()
padA.speed(0)
padA.shape('square')
padA.shapesize(stretch_wid=6,stretch_len=1)
padA.color('white')
padA.penup()
padA.goto(-350,0)

# Paddle B
padB = turtle.Turtle()
padB.speed(0)
padB.shape('square')
padB.shapesize(stretch_wid=6,stretch_len=1)
padB.color('white')
padB.penup()
padB.goto(350,0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('white')
ball.penup()
ball.goto(0,0)

ball.dx = 1.0
ball.dy = 1.0


# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0,250)



# Functions :
def padA_up():
	y = padA.ycor()
	y += 25
	padA.sety(y)

def padA_down():
	y = padA.ycor()
	y -= 25
	padA.sety(y)

def padB_up():
	y = padB.ycor()
	y += 25
	padB.sety(y)

def padB_down():
	y = padB.ycor()
	y -= 25
	padB.sety(y)


def write():
	pen.write(f"Player A : {scoreA}    Player B : {scoreB}",align='center',font=('Courier',24,'normal'))


def playMusic(music):
	try:
		winsound.PlaySound(music, winsound.SND_ASYNC)
	except FileNotFoundError:
		print('The required music file does not exist.')
	except:
		print('winsound module only works on windows.')
		print('try playing the sound with os module')

# Keyboard bindings
win.listen()
win.onkeypress(padA_up,'w')
win.onkeypress(padA_down,'s')
win.onkeypress(padB_up,'Up')
win.onkeypress(padB_down,'Down')

write()

# * ------------------------------------------------------------ *

# Main game loop
try:
	while True:
		win.update()

		# Moving the ball
		ball.setx(ball.xcor() + ball.dx)
		ball.sety(ball.ycor() + ball.dy)

		# Border collison
		if ball.ycor() > 290:
			ball.dy *= -1
			playMusic('assets/hit1.wav')

		if ball.ycor() < -290:
			ball.dy *= -1
			playMusic('assets/hit1.wav')

		if ball.xcor() > 390:
			ball.setx(-100)
			ball.dx *= -1
			scoreA += 1
			pen.clear()
			write()

		if ball.xcor() < -390:
			ball.setx(-100)
			ball.dx *= -1
			scoreB += 1
			pen.clear()
			write()

		# Paddle and ball collision
		if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < padB.ycor() + 50 and ball.ycor() > padB.ycor() - 50):
			playMusic('assets/hit2.wav')
			ball.setx(340)
			ball.dx *= -1
		if (ball.xcor() < -340 and ball.xcor() >-350) and (ball.ycor() < padA.ycor() + 50 and ball.ycor() > padA.ycor() - 50):
			playMusic('assets/hit2.wav')
			ball.setx(-340)
			ball.dx *= -1


except Exception as e:
	pass