# The Snake Game in Python 3 using the Turtle Module
# Version: 1.0.1
# by vlam

import turtle
import time
import random
import tkinter

# Set up the main screen
wn = turtle.Screen()
wn.title("Snake in Python")
wn.bgcolor("gray")
wn.setup(width=625, height=625)
wn.tracer(0)    # Turns off screen updates


# Create Border
border = turtle.Turtle()
border.speed(0)
border.penup()
border.hideturtle()
border.setposition(-300, -295)
border.pendown()
border.pensize(5)
border.color("white")
for _ in range(2):
    border.forward(wn.window_width() - 30)
    border.left(90)
    border.forward(wn.window_height() - 75)
    border.left(90)

#for _ in range(4):  # This method if you want a perfect square
#    border.forward(600)
#    border.left(90)


# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"


# Apple
apple = turtle.Turtle()
apple.speed(0)
apple.shape("circle")
apple.color("red")
apple.penup()
apple.goto(0,100)
apple.pencolor("black")

segments = []


# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(50, 260)
pen.write("Score: 0          High Score: 0", align="center", font=("Calibri", 24, "normal"))


# Pause screen
pscreen = turtle.Turtle()
pscreen.speed(0)
pscreen.color("white")
pscreen.penup()
pscreen.hideturtle()
pscreen.goto(0, 0)


# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
            head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        head.sety(head.ycor() - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        head.setx(head.xcor() + 20)

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        wn.title("Snake in Python - Paused")
        print("Game Pause. Press the Esc key to resume or 0 to reset.")
        pscreen.write("Game Paused\n[Esc] Resume  |  [0] Reset to Menu", align="center", font=("Calibri", 24, "normal"))
    else:
        print("Game Resumed.")
        wn.title("Snake in Python")
        pscreen.clear()

def difficulty_screen(screen):
    # Global variable to store chosen difficulty
    global chosen_difficulty
    chosen_difficulty = None
    
    screen.clear()
    screen.bgcolor("lightblue")
    screen.title("Snake in Python - Main Menu")

    # Title and build version number
    title = turtle.Turtle()
    title.hideturtle()
    title.speed(0)
    title.penup()
    title.goto(-290, 230)
    title.write("Snake in Python", align="left", font=("calibri", 42, "bold"))

    subtitle = turtle.Turtle()
    subtitle.hideturtle()
    subtitle.speed(0)
    subtitle.penup()
    subtitle.goto(0, 210)
    subtitle.write("by vlam", align="right", font=("calibri", 16, "bold"))

    bldver = turtle.Turtle()
    bldver.hideturtle()
    bldver.speed(0)
    bldver.penup()
    bldver.goto(270, -290)
    bldver.color("gray")
    bldver.write("Build version:  1.0.1", align="right", font=("calibri", 11, "bold"))

    controls = turtle.Turtle()
    controls.hideturtle()
    controls.speed(0)
    controls.penup()
    controls.goto(-270, -260)
    controls.write("Controls:\n [Esc]: Pause/Menu\n [Up Arrow] or [w]: Up\n [Left Arrow] or [a]: Left\n [Down Arrow] or [s]: Down\n [Right Arrow] or [d]: Right", align="left", font=("calibri", 14, "normal"))

    # Display difficulty options
    difficulty = turtle.Turtle()
    difficulty.hideturtle()
    difficulty.speed(0)
    difficulty.penup()
    difficulty.goto(0, 100)
    difficulty.write("Press # on keyboard to select difficulty:", align="center", font=("calibri", 24, "normal"))

    difficulty.goto(-100, 30)
    difficulty.write("1. Easy", align="left", font=("calibri", 18, "normal"))

    difficulty.goto(-100, 0)
    difficulty.write("2. Intermediate", align="left", font=("calibri", 18, "normal"))

    difficulty.goto(-100, -30)
    difficulty.write("3. Hard", align="left", font=("calibri", 18, "normal"))

    difficulty.goto(-100, -60)
    difficulty.write("4. Master", align="left", font=("calibri", 18, "normal"))

    # Listen for key presses
    screen.onkey(lambda: set_difficulty("easy"), "1")
    screen.onkey(lambda: set_difficulty("intermediate"), "2")
    screen.onkey(lambda: set_difficulty("hard"), "3")
    screen.onkey(lambda: set_difficulty("master"), "4")
    screen.listen()

    # Wait for use input
    try:
        while chosen_difficulty is None:
            screen.update()  # Update the screen to show text
    except turtle.Terminator:
        print("Window was closed.")

def set_difficulty(difficulty):
    global chosen_difficulty
    chosen_difficulty = difficulty
    wn.clear()
    print(f"Difficulty set to: {chosen_difficulty}")  # Debugging
    #pscreen.write(f"Difficulty set to: {chosen_difficulty}", align="center", font=("Calibri", 24, "normal"))

def reset_delay():
    global delay
    if chosen_difficulty == "easy":
        delay = 0.1
    elif chosen_difficulty == "intermediate":
        delay = 0.075
    elif chosen_difficulty == "hard":
        delay = 0.050
    elif chosen_difficulty == "master":
        delay = 0.025
    else:
        delay = 0.1

def return_to_difficulty():
    global paused, chosen_difficulty
    if paused:
        paused = False
        chosen_difficulty = None

        # Fully clear and reset the screen
        wn.clear()
        wn.bgcolor("lightblue")
        wn.title("Snake in Python - Main Menu")
        wn.setup(width=625, height=625)
        wn.tracer(0)

        # Show difficulty screen again
        difficulty_screen(wn)  # Re-show difficulty screen
        reset_delay()          # Set speed based on selection
        main()                 # Restart game loop


# Flag to control pause state
paused = False


# Difficulty level
#delay = 0.1    # Easy
#delay = 0.075   # Intermediate
#delay = 0.050   # Hard
#delay = 0.025   # Master


# Scoring
score = 0
high_score = 0


# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkey(toggle_pause, "Escape")
wn.onkey(return_to_difficulty, "0")  # 0 to return to difficulty screen


# Define a list of colors
colors = ["red", "black"]

# Call the difficulty screen function
difficulty_screen(wn)
if chosen_difficulty == "easy":
    #game_speed = 10
    delay = 0.1
elif chosen_difficulty == "intermediate":
    #game_speed = 20
    delay = 0.075
elif chosen_difficulty == "hard":
    #game_speed = 30
    delay = 0.050
elif chosen_difficulty == "master":
    #game_speed = 40
    delay = 0.025
else:
    #game_speed = 10
    delay = 0.1


# Main game loop
def main():
    global delay
    global score, high_score

    # Clear screen and reinitialize background and border
    wn.reset()
    wn.bgcolor("gray")
    wn.setup(width=625, height=625)
    wn.title("Snake in Python")
    wn.tracer(0)

    # Recreate border
    border = turtle.Turtle()
    border.speed(0)
    border.penup()
    border.hideturtle()
    border.setposition(-300, -295)
    border.pendown()
    border.pensize(5)
    border.color("white")
    for _ in range(2):
        border.forward(wn.window_width() - 30)
        border.left(90)
        border.forward(wn.window_height() - 75)
        border.left(90)

    global head, apple, pen, segments

    # Recreate snake head
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color("black")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"

    # Recreate apple
    apple = turtle.Turtle()
    apple.speed(0)
    apple.shape("circle")
    apple.color("red")
    apple.penup()
    apple.goto(0, 100)
    apple.pencolor("black")

    # Recreate pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(50, 260)
    pen.write("Score: 0          High Score: 0", align="center", font=("Calibri", 24, "normal"))

    global chosen_difficulty
    # Difficulty label
    difficulty_label = turtle.Turtle()
    difficulty_label.speed(0)
    difficulty_label.color("white")
    difficulty_label.penup()
    difficulty_label.hideturtle()
    difficulty_label.goto(-290, 260)
    difficulty_label.write(f"Difficulty:\n{chosen_difficulty.capitalize()}", align="left", font=("Calibri", 16, "normal"))

    # Reset segment list
    segments = []

    # Recreate functions
    def go_up():
        if head.direction != "down":
            head.direction = "up"

    def go_down():
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        if head.direction != "left":
            head.direction = "right"

    def move():
        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)

        if head.direction == "down":
            head.sety(head.ycor() - 20)

        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)

        if head.direction == "right":
            head.setx(head.xcor() + 20)

    # Recreate keyboard bindings
    wn.listen()
    wn.onkeypress(go_up, "Up")
    wn.onkeypress(go_down, "Down")
    wn.onkeypress(go_left, "Left")
    wn.onkeypress(go_right, "Right")
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")
    wn.onkey(toggle_pause, "Escape")
    wn.onkey(return_to_difficulty, "0")

    # Start the game
    try:
        while True:
            if not paused:
                wn.update()
                wn.bgcolor("gray")

                # Check for a collision with the border
                if head.xcor() > 280 or head.xcor() < -290 or head.ycor() > 255 or head.ycor() < -280:
                    wn.bgcolor("khaki")
                    time.sleep(1)
                    head.goto(0, 0)
                    head.direction = "stop"

                    # Hide segments on new game
                    for segment in segments:
                        segment.goto(1000, 1000)

                    # Clear the segments list
                    segments.clear()

                    # Reset score
                    score = 0

                    # Reset the delay
                    #delay = 0.1
                    reset_delay()

                    pen.clear()
                    pen.write("Score: {}          High Score: {}".format(score, high_score), align="center", font=("Calibri", 24, "normal"))


                # Check if snake eats apple
                if head.distance(apple) < 20:
                    # Move the apple to random spot on the screen
                    x = random.randint(-280, 270)
                    y = random.randint(-270, 240)
                    apple.goto(x, y)

                    # Add snake body segment
                    new_segment = turtle.Turtle()
                    new_segment.speed(0)
                    new_segment.shape("square")
                    new_segment.color("lightgray")
                    new_segment.penup()
                    new_segment.pencolor("black")
                    segments.append(new_segment)

                    # Shorten delay
                    delay -= 0.001

                    # Increase score
                    score += 10

                    if score > high_score:
                        high_score = score
                    pen.clear()
                    pen.write("Score: {}          High Score: {}".format(score, high_score), align="center", font=("Calibri", 24, "normal"))
                
                # Move last segment fist in reverse order
                for index in range(len(segments)-1, 0, -1):
                    x = segments[index-1].xcor()
                    y = segments[index-1].ycor()
                    segments[index].goto(x, y)

                # Move segment 0 to head
                if len(segments) > 0:
                    x = head.xcor()
                    y = head.ycor()
                    segments[0].goto(x, y)

                move()

                # Check for head collision with body
                for segment in segments:
                    if segment.distance(head) < 20:
                        wn.bgcolor("khaki")
                        time.sleep(1)
                        head.goto(0, 0)
                        head.direction = "stop"
                        
                        # Hide segments on new game
                        for segment in segments:
                            segment.goto(1000, 1000)

                        # Clear the segments list
                        segments.clear()

                        # Reset score
                        score = 0

                        # Reset the delay
                        #delay = 0.1
                        reset_delay()
                        
                        pen.clear()
                        pen.write("Score: {}          High Score: {}".format(score, high_score), align="center", font=("Calibri", 24, "normal"))

            wn.update()
            time.sleep(delay)
    except (turtle.Terminator, tkinter.TclError):
        print("Window was closed.")

# Run the game
main()
wn.mainloop()