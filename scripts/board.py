from math import *
from time import *
from random import *
from copy import deepcopy
from ui import screen
from global_vars import *
from game_rules import valid, decentHeuristic, finalHeuristic, move

class Board:
	def __init__(self):
		#White goes first (0 is white and player,1 is black and computer)
		self.player = 0
		self.passed = False
		self.won = False
		#Initializing an empty board
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append(None)

		#Initializing center values
		self.array[3][3]="w"
		self.array[3][4]="b"
		self.array[4][3]="b"
		self.array[4][4]="w"

		#Initializing old values
		self.oldarray = self.array
	#Updating the board to the screen
	def update(self):
		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.oldarray[x][y]=="w":
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

				elif self.oldarray[x][y]=="b":
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		#Animation of new tiles
		screen.update()
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="w":
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
					screen.update()

				elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")

					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
					screen.update()

		#Drawing of highlight circles
		for x in range(8):
			for y in range(8):
				if self.player == 0:
					if valid(self.array,self.player,x,y):
						screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#008000",outline="#008000")

		if not self.won:
			#Draw the scoreboard and update the screen
			self.drawScoreBoard()
			screen.update()
			#If the computer is AI, make a move
			if self.player==1:
				startTime = time()
				self.oldarray = self.array
				alphaBetaResult = self.alphaBeta(self.array,depth,-float("inf"),float("inf"),1)
				self.array = alphaBetaResult[1]

				if len(alphaBetaResult)==3:
					position = alphaBetaResult[2]
					self.oldarray[position[0]][position[1]]="b"

				self.player = 1-self.player
				deltaTime = round((time()-startTime)*100)/100
				if deltaTime<2:
					sleep(2-deltaTime)
				nodes = 0
				#Player must pass?
				self.passTest()
		else:
			screen.create_text(250,550,anchor="c",font=("Consolas",15), text="The game is done!")

	#Moves to position
	def boardMove(self,x,y):
		global nodes
		#Move and update screen
		self.oldarray = self.array
		self.oldarray[x][y]="w"
		self.array = move(self.array,x,y)
		
		#Switch Player
		self.player = 1-self.player
		self.update()
		
		#Check if ai must pass
		self.passTest()
		self.update()	

	#METHOD: Draws scoreboard to screen
	def drawScoreBoard(self):
		global moves
		#Deleting prior score elements
		screen.delete("score")

		#Scoring based on number of tiles
		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y]=="w":
					player_score+=1
				elif self.array[x][y]=="b":
					computer_score+=1

		if self.player==0:
			player_colour = "green"
			computer_colour = "gray"
		else:
			player_colour = "gray"
			computer_colour = "green"

		screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
		screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)

		#Pushing text to screen
		screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
		screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

		moves = player_score+computer_score

	#METHOD: Test if player must pass: if they do, switch the player
	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					mustPass=False
		if mustPass:
			self.player = 1-self.player
			if self.passed==True:
				self.won = True
			else:
				self.passed = True
			self.update()
		else:
			self.passed = False

	#This contains the minimax algorithm
	#http://en.wikipedia.org/wiki/Minimax
	def minimax(self, node, depth, maximizing):
		global nodes
		nodes += 1
		boards = []
		choices = []

		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([decentHeuristic(node,1-maximizing),node])

		if maximizing:
			bestValue = -float("inf")
			bestBoard = []
			for board in boards:
				val = self.minimax(board,depth-1,0)[0]
				if val>bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

		else:
			bestValue = float("inf")
			bestBoard = []
			for board in boards:
				val = self.minimax(board,depth-1,1)[0]
				if val<bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

	#alphaBeta pruning on the minimax tree
	#http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
	def alphaBeta(self,node,depth,alpha,beta,maximizing):
		global nodes
		nodes += 1
		boards = []
		choices = []

		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([finalHeuristic(node,maximizing),node])

		if maximizing:
			v = -float("inf")
			bestBoard = []
			bestChoice = []
			for board in boards:
				boardValue = self.alphaBeta(board,depth-1,alpha,beta,0)[0]
				if boardValue>v:
					v = boardValue
					bestBoard = board
					bestChoice = choices[boards.index(board)]
				alpha = max(alpha,v)
				if beta <= alpha:
					break
			return([v,bestBoard,bestChoice])
		else:
			v = float("inf")
			bestBoard = []
			bestChoice = []
			for board in boards:
				boardValue = self.alphaBeta(board,depth-1,alpha,beta,1)[0]
				if boardValue<v:
					v = boardValue
					bestBoard = board
					bestChoice = choices[boards.index(board)]
				beta = min(beta,v)
				if beta<=alpha:
					break
			return([v,bestBoard,bestChoice])