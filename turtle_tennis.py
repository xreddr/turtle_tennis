import turtle

# Screen
s = turtle.Screen()    
s.bgcolor("blue")
s.setup(1000, 600)
s.bgpic("bgtt.png")

score = turtle.Turtle()
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, 260)

median = turtle.Turtle()
median.goto(0, 0)
median.shapesize(stretch_wid=20, stretch_len=.2)
median.shape("square")
median.color("white")


class Paddle:
    players = []
    def __init__(self, pos, color, keyUp, keyDown):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.color(color)
        self.turtle.shape("square")
        self.turtle.shapesize(stretch_wid=6, stretch_len=.5)
        self.turtle.penup()
        self.turtle.goto(pos)
        self.keyUp = keyUp
        self.keyDown = keyDown
        self.score = 0
        turtle.onkey(self.up, keyUp)
        turtle.onkey(self.down, keyDown)
        Paddle.players.append(self)
    def up(self):
        y = self.turtle.ycor()
        y += 20
        self.turtle.sety(y)
    def down(self):
        y = self.turtle.ycor()
        y -= 20
        self.turtle.sety(y)
    def stop(self):
        pass
        
p1 = Paddle([-400, 0], "white", "Up", "Down")
p2 = Paddle([400, 0], "white", "r", "f")

class Ball(turtle.Turtle):
    balls = []
    def __init__(self, color, goto, movement):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.color(color)
        self.goto(goto[0], goto[1])
        self.dx = movement[0]
        self.dy = movement[1]
        self.spin = 5
        self.speed(100)
        self.shapesize(stretch_wid=1.5, stretch_len=1.5)
        Ball.balls.append(self)
    def move(self):
        mx = self.xcor() + self.dx
        my = self.ycor() + self.dy
        self.right(self.spin)
        self.goto(mx, my)

startBall = Ball("chartreuse", [0, 0], [5, -5])

# Listeners
def aiDown(b, paddle):
    return b.ycor() < paddle.turtle.ycor() and abs(b.ycor() - paddle.turtle.ycor()) > 15

def aiUp(b, paddle):
    return b.ycor() > paddle.turtle.ycor() and abs(b.ycor() - paddle.turtle.ycor()) > 15

def strike(ball, paddle):
    return abs(ball.xcor() - paddle.xcor()) < 15 and abs(ball.ycor() - paddle.ycor()) < 60
    
# Game Board Borders
def ballBorders(b):
    if abs(b.ycor()) > 290:
        b.dy *= -1
        
    if b.xcor() > 500:
        onScore(b, -5, p1)
        
    if b.xcor() < -500:
        onScore(b, 5, p2)

def paddleStop():
    for i in Paddle.players:
        if i.turtle.ycor() > 300:
            turtle.onkey(i.stop, i.keyUp)
        else:
            turtle.onkey(i.up, i.keyUp)
            
    for i in Paddle.players:
        if i.turtle.ycor() < -300:
            turtle.onkey(i.stop, i.keyDown)
        else:
            turtle.onkey(i.down, i.keyDown)

# Scoring
def onScore(b, d, player):
    b.hideturtle()
    player.score += 1
    b.goto(0, 0)
    b.dx = d
    b.dy = 5
    b.spin = 5
    updateScore()
    
def updateScore():
    score.clear()
    score.write("Player 1: {}   Player 2: {}".format(p1.score, p2.score),
                align="center", font=("Courier", 24, "bold"))

# Game Loops
def play():
    for b in Ball.balls:
        b.showturtle()
        b.move()
        ballBorders(b)
        if aiUp(startBall, p2):
            p2.up()
        elif aiDown(startBall, p2):
            p2.down()
        for p in Paddle.players:
            if strike(b, p.turtle):
                b.dx *= -1.2
                b.dy *= 1.2
                b.spin *= 1.2
    paddleStop()
    s.ontimer(play, 10)
            
turtle.listen()
updateScore()
play()
    
turtle.mainloop() # Last line, keeps tkinter window open
    