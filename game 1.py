from tkinter import Tk as makescreen, Canvas, PhotoImage
from random import randint

#screen initialization
screen = makescreen()
screen.title("Hurdling Game")
screen.resizable(0,0)

#canvas control
canvas = Canvas(screen, width=800, height=500)
canvas.pack()
screen.update()

#load image

bgimage = PhotoImage(file='background.png')
jumpimage = PhotoImage(file='jump.png')
run0image = PhotoImage(file='run0.png')
run1image = PhotoImage(file='run1.png')
run2image = PhotoImage(file='run2.png')
hurdleimage = PhotoImage(file='hurdle.png')
brokenimage = PhotoImage(file='broken.png')

#defaultbackground = bgimage

canvas.create_image(400,250,image=bgimage)
label=canvas.create_text(600,250, text='score: 0, level: 0', font=('times new roman', 40), fill='black')

#levels
score = 0
level = 0
SPEED_COEFFICIENT = 5

#human animation

human = canvas.create_image(200, 350, image=run0image)
runlist = [run0image, run1image, run2image,run1image]
index=0

hurdle = canvas.create_image(700, 435, image=hurdleimage)

def hurdle_movement():
    global level
    global score
    canvas.move(hurdle, -10 - SPEED_COEFFICIENT * level, 0)
    canvas.after(50, hurdle_movement)

    hurdle_pos = canvas.coords(hurdle)
    collision()
    if hurdle_pos[0] < -120:
        canvas.coords(hurdle, 700, 435)
        canvas.itemconfig(hurdle, image=hurdleimage)
        score += 100
        level = score // 500
        canvas.itemconfig(label, text='score: ' + str(score) + ', level: ' + str(level))

def collision():
    global level
    global score
    human_pos = canvas.coords(human)
    hurdle_pos = canvas.coords(hurdle)
    diff_x = abs(human_pos[0] - hurdle_pos[0])
    diff_y = abs(human_pos[1] - (hurdle_pos[1] - 85))
    print(diff_x, diff_y)

    if diff_x < 30 and diff_y < 30: #if there is an intersection of hurdle and human
        level = 0
        score = 0
        canvas.itemconfig(hurdle, image=brokenimage)
        canvas.itemconfig(label, text='score: ' + str(score) + ', level: ' + str(level))


def running():
    global index
    index +=1
    canvas.itemconfig(human,image=runlist[index %4])
    canvas.after(300,running)

running()
hurdle_movement()
collision()

jump = False
jumpspeed = -30
gravity = 2
def jumping():
    global jump, jumpspeed, gravity
    jump = True
    pos = canvas.coords(human)
    if pos[1] > 350:
        jump = False
        jumpspeed = -30
        canvas.coords(human, 200, 350)
    else:
        canvas.move(human, 0, jumpspeed)
        jumpspeed += gravity
        canvas.after(50, jumping)
def jumpevent(event):
    global jump
    if not jump:
        jumping()

canvas.bind_all("<KeyRelease-s>", jumpevent)

screen.mainloop()