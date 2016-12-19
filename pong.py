# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
RIGHT = False
ball_pos = [300, 200]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = paddle2_pos = 200 + HALF_PAD_HEIGHT
acc = 5
radius = 9

# initialize ball_pos and ball_vel for new bal in middle of table
# Spawn a new ball
def spawn_ball(right_direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300, 200]
    # Randomize ball velocity. if direction is RIGHT, the ball's velocity is upper right else upper left
    if right_direction:
        ball_vel = [random.randrange(2,4), random.randrange(1, 3)]
    else:
        ball_vel = [-random.randrange(2,4), random.randrange(1, 3)]



# define event handlers
#Starts a new game
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, RIGHT # these are numbers
    global score1, score2# these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = paddle2_pos = 200 + HALF_PAD_HEIGHT
    
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos
    global ball_vel, paddle1_vel, paddle2_vel, radius
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # draw the scores
    canvas.draw_text(str(score1), [250, 40], 40, "Yellow")
    canvas.draw_text(str(score2), [330, 40], 40, "Yellow")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] - ball_vel[1] 
    if ball_pos[0] >= 17 and ball_pos[0] < 22:
        ball_pos[0] = 17
    # draw ball
    canvas.draw_circle(ball_pos, radius, 18, "White")
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= PAD_HEIGHT   and paddle1_pos + paddle1_vel <= HEIGHT :
        paddle1_pos = paddle1_pos  + paddle1_vel
    if paddle2_pos + paddle2_vel >= PAD_HEIGHT   and paddle2_pos + paddle2_vel <= HEIGHT :
        paddle2_pos = paddle2_pos  + paddle2_vel 
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos], [HALF_PAD_WIDTH , paddle1_pos - PAD_HEIGHT], 8, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH , paddle2_pos], [WIDTH - HALF_PAD_WIDTH , paddle2_pos - PAD_HEIGHT], 8, "White")
    # determine whether paddle 1 and ball collide and draw cores accordigly   
    if (ball_pos[0] <= (PAD_WIDTH + radius + 8)): 
        if ball_pos[1] <= paddle1_pos and ball_pos[1] >= paddle1_pos - PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0] * 0.10
            ball_vel[1] += ball_vel[1] * 0.10
        else:
            score2 += 1
            spawn_ball(True)
    # determine whether paddle 2 and ball collide and draw cores accordigly   
    if (ball_pos[0] >= (WIDTH - radius - 8)): 
        if ball_pos[1] <= paddle2_pos and ball_pos[1] >= paddle2_pos - PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0] * 0.10
            ball_vel[1] += ball_vel[1] * 0.10
        else:
            score1 += 1
            spawn_ball(False)
    # determine whether ball collide with the roof or floor
    if ball_pos[1] < radius + 8 or ball_pos[1] > (HEIGHT - radius - 8):
        ball_vel[1] = -ball_vel[1]
 
#Key handlers        
def keydown(key):
    global paddle1_vel, paddle2_vel, acc
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = paddle1_vel - acc
        
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle1_vel + acc
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = paddle2_vel - acc
        
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle2_vel + acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel, acc
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = paddle1_vel + acc 
        
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle1_vel - acc
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = paddle2_vel + acc
        
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle2_vel - acc


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button("New Game", new_game, 100)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
