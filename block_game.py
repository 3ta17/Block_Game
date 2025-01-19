import tkinter
import random

# Font settings
FNT = ("Times New Roman", 20, "bold")

key = ""
keyoff = False
idx = 0
tmr = 0
stage = 0
score = 0
bar_x = 0
bar_y = 540
ball_x = 0
ball_y = 0
ball_xp = 0
ball_yp = 0
is_clr = True

# Block layout (5 rows of blocks, 10 empty rows)
block = []
for i in range(5):
    block.append([1] * 10)
for i in range(10):
    block.append([0] * 10)

# Key press event handlers
def key_down(e):
    global key
    key = e.keysym

def key_up(e):
    global keyoff
    keyoff = True

# Draw blocks on the screen
def draw_block():
    global is_clr
    is_clr = True
    cvs.delete("BG")
    for y in range(15):
        for x in range(10):
            gx = x * 80
            gy = y * 40
            if block[y][x] == 1:
                cvs.create_rectangle(gx+1, gy+4, gx+79, gy+32, fill=block_color(x, y), width=0, tag="BG")
                is_clr = False
    # Display stage and score
    cvs.create_text(200, 20, text="STAGE " + str(stage), fill="white", font=FNT, tag="BG")
    cvs.create_text(600, 20, text="SCORE " + str(score), fill="white", font=FNT, tag="BG")

# Calculate block color
def block_color(x, y): 
    col = "#{0:x}{1:x}{2:x}".format(15-x-int(y/3), x+1, y*3+3)
    return col

# Draw the paddle (bar)
def draw_bar():
    cvs.delete("BAR")
    cvs.create_rectangle(bar_x-80, bar_y-12, bar_x+80, bar_y+12, fill="silver", width=0, tag="BAR")

# Move the paddle based on key input
def move_bar():
    global bar_x
    if key == "Left" and bar_x > 80:
        bar_x -= 40
    if key == "Right" and bar_x < 720:
        bar_x += 40

# Draw the ball
def draw_ball():
    cvs.delete("BALL")
    cvs.create_oval(ball_x-20, ball_y-20, ball_x+20, ball_y+20, fill="gold", outline="orange", width=2, tag="BALL")

# Move the ball and handle collisions
def move_ball():
    global idx, tmr, score, ball_x, ball_y, ball_xp, ball_yp
    ball_x += ball_xp
    if ball_x < 20 or ball_x > 780:  # Bounce off left/right walls
        ball_xp = -ball_xp

    # Check for collisions with blocks
    x = int(ball_x / 80)
    y = int(ball_y / 40)
    if block[y][x] == 1:
        block[y][x] = 0
        ball_xp = -ball_xp
        score += 10

    ball_y += ball_yp
    if ball_y >= 600:  # Ball falls out (Game Over)
        idx = 2
        tmr = 0
        return
    if ball_y < 20:  # Bounce off top wall
        ball_yp = -ball_yp

    if block[y][x] == 1:
        block[y][x] = 0
        ball_yp = -ball_yp
        score += 10

    # Paddle collision
    if bar_y-40 <= ball_y <= bar_y:
        if bar_x-80 <= ball_x <= bar_x+80:
            ball_yp = -10
            score += 1

# Main game loop
def main_proc():
    global key, keyoff, idx, tmr, stage, score
    global bar_x, ball_x, ball_y, ball_xp, ball_yp

    if idx == 0:  # Start screen
        tmr += 1
        if tmr == 1:
            stage = 1
            score = 0
        if tmr == 2:
            ball_x, ball_y = 160, 240
            ball_xp, ball_yp = 10, 10
            bar_x = 400
            draw_block()
            draw_ball()
            draw_bar()
            cvs.create_text(400, 300, text="START", fill="cyan", font=FNT, tag="TXT")
        if tmr == 30:
            cvs.delete("TXT")
            idx = 1

    elif idx == 1:  # Gameplay
        move_ball()
        move_bar()
        draw_block()
        draw_ball()
        draw_bar()
        if is_clr:  # All blocks cleared
            idx = 3
            tmr = 0

    elif idx == 2:  # Game Over
        tmr += 1
        if tmr == 1:
            cvs.create_text(400, 260, text="GAME OVER", fill="red", font=FNT, tag="TXT")
        if tmr == 15:
            cvs.create_text(300, 340, text="[R]eplay", fill="cyan", font=FNT, tag="TXT")
            cvs.create_text(500, 340, text="[N]ew game", fill="yellow", font=FNT, tag="TXT")
        if key == "r":  # Replay
            cvs.delete("TXT")
            idx, tmr = 0, 1
        if key == "n":  # New game
            cvs.delete("TXT")
            for y in range(5):
                for x in range(10):
                    block[y][x] = 1
            idx, tmr = 0, 0

    elif idx == 3:  # Stage Clear
        tmr += 1
        if tmr == 1:
            cvs.create_text(400, 260, text="STAGE CLEAR", fill="lime", font=FNT, tag="TXT")
        if tmr == 15:
            cvs.create_text(400, 340, text="NEXT [SPACE]", fill="cyan", font=FNT, tag="TXT")
        if key == "space":  # Move to next stage
            cvs.delete("TXT")
            for y in range(5):
                for x in range(10):
                    block[y][x] = 1
            idx, tmr, stage = 0, 1, stage + 1

    if keyoff:
        keyoff = False
        key = ""

    root.after(50, main_proc)

# Initialize the game window
root = tkinter.Tk()
root.title("Block Game")
root.resizable(False, False)
root.bind("<Key>", key_down)
root.bind("<KeyRelease>", key_up)
cvs = tkinter.Canvas(root, width=800, height=600, bg="black")
cvs.pack()

main_proc()
root.mainloop()
