from tkinter import *
from board import *
from game_rules import clickHandle, keyHandle

#Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#222",highlightthickness=0)
screen.pack()

def drawGridBackground(outline=False):
	#If we want an outline on the board then draw one
	if outline:
		screen.create_rectangle(50,50,450,450,outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50,lineShift,450,lineShift,fill="#111")

		#Vertical line
		screen.create_line(lineShift,50,lineShift,450,fill="#111")

	screen.update()

def create_buttons():
		#Restart button
		#Background/shadow
		screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
		screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

		#Arrow
		screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
		screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

		#Quit button
		#Background/shadow
		screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
		screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
		#"X"
		screen.create_line(455,5,495,45,fill="white",width="3")
		screen.create_line(495,5,455,45,fill="white",width="3")
	
def runGame():
	global running
	running = False
	#Title and shadow
	screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
	screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")
	
	#Creating the difficulty buttons
	for i in range(3):
		#Background
		screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
		screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

		spacing = 130/(i+2)
		for x in range(i+1):
			#Star with double shadow
			screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="\u2605", font=("Consolas", 25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")

	screen.update()

def playGame():
	global board, running
	running = True
	screen.delete(ALL)
	create_buttons()
	board = 0

	#Draw the background
	drawGridBackground()

	#Create the board and update it
	board = Board()
	board.update()

#Binding, setting
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
root.wm_title("AI Reversi Game")
root.mainloop()
