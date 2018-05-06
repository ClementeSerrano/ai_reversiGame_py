from copy import deepcopy
from global_vars import *
from ui import root, screen, create_buttons, playGame, runGame

def move(passedArray,x,y):
	#Must copy the passedArray so we don't alter the original
	array = deepcopy(passedArray)
	#Set colour and set the moved location to be that colour
	if board.player==0:
		colour = "w"
		
	else:
		colour="b"
	array[x][y]=colour
	
	#Determining the neighbours to the square
	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!=None:
				neighbours.append([i,j])
	
	#Which tiles to convert
	convert = []

	#For all the generated neighbours, determine if they form a line
	#If a line is formed, we will add it to the convert array
	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]
		#Check if the neighbour is of a different colour - it must be to form a line
		if array[neighX][neighY]!=colour:
			#The path of each individual line
			path = []
			
			#Determining direction to move
			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			#While we are in the bounds of the board
			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				#If we reach a blank tile, we're done and there's no line
				if value==None:
					break
				#If we reach a tile of the player's colour, a line is formed
				if value==colour:
					#Append all of our path nodes to the convert array
					for node in path:
						convert.append(node)
					break
				#Move the tile
				tempX+=deltaX
				tempY+=deltaY
				
	#Convert all the appropriate tiles
	for node in convert:
		array[node[0]][node[1]]=colour

	return array

#Simple heuristic. Compares number of each tile.
def dumbScore(array,player):
	score = 0
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#+1 if it's player colour, -1 if it's opponent colour
	for x in range(8):
		for y in range(8):
			if array[x][y]==colour:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score

#Less simple but still simple heuristic. Weights corners and edges as more
def slightlyLessDumbScore(array,player):
	score = 0
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#Go through all the tiles	
	for x in range(8):
		for y in range(8):
			#Normal tiles worth 1
			add = 1
			#Edge tiles worth 3
			if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=3
			#Corner tiles worth 5
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 5
			#Add or subtract the value of the tile corresponding to the colour
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

#Heuristic that weights corner tiles and edge tiles as positive, adjacent to corners (if the corner is not yours) as negative
#Weights other tiles as one point
def decentHeuristic(array,player):
	score = 0
	cornerVal = 25
	adjacentVal = 5
	sideVal = 5
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#Go through all the tiles	
	for x in range(8):
		for y in range(8):
			#Normal tiles worth 1
			add = 1
			
			#Adjacent to corners are worth -3
			if (x==0 and y==1) or (x==1 and 0<=y<=1):
				if array[0][0]==colour:
					add = sideVal
				else:
					add = -adjacentVal


			elif (x==0 and y==6) or (x==1 and 6<=y<=7):
				if array[7][0]==colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x==7 and y==1) or (x==6 and 0<=y<=1):
				if array[0][7]==colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x==7 and y==6) or (x==6 and 6<=y<=7):
				if array[7][7]==colour:
					add = sideVal
				else:
					add = -adjacentVal


			#Edge tiles worth 3
			elif (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=sideVal
			#Corner tiles worth 15
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = cornerVal
			#Add or subtract the value of the tile corresponding to the colour
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

#Seperating the use of heuristics for early/mid/late game.
def finalHeuristic(array,player):
	if moves<=8:
		numMoves = 0
		for x in range(8):
			for y in range(8):
				if valid(array,player,x,y):
					numMoves += 1
		return numMoves+decentHeuristic(array,player)
	elif moves<=52:
		return decentHeuristic(array,player)
	elif moves<=58:
		return slightlyLessDumbScore(array,player)
	else:
		return dumbScore(array,player)

#Checks if a move is valid for a given array.
def valid(array,player,x,y):
	#Sets player colour
	if player==0:
		colour="w"
	else:
		colour="b"
		
	#If there's already a piece there, it's an invalid move
	if array[x][y]!=None:
		return False

	else:
		#Generating the list of neighbours
		neighbour = False
		neighbours = []
		for i in range(max(0,x-1),min(x+2,8)):
			for j in range(max(0,y-1),min(y+2,8)):
				if array[i][j]!=None:
					neighbour=True
					neighbours.append([i,j])
		#If there's no neighbours, it's an invalid move
		if not neighbour:
			return False
		else:
			#Iterating through neighbours to determine if at least one line is formed
			valid = False
			for neighbour in neighbours:

				neighX = neighbour[0]
				neighY = neighbour[1]
				
				#If the neighbour colour is equal to your colour, it doesn't form a line
				#Go onto the next neighbour
				if array[neighX][neighY]==colour:
					continue
				else:
					#Determine the direction of the line
					deltaX = neighX-x
					deltaY = neighY-y
					tempX = neighX
					tempY = neighY

					while 0<=tempX<=7 and 0<=tempY<=7:
						#If an empty space, no line is formed
						if array[tempX][tempY]==None:
							break
						#If it reaches a piece of the player's colour, it forms a line
						if array[tempX][tempY]==colour:
							valid=True
							break
						#Move the index according to the direction of the line
						tempX+=deltaX
						tempY+=deltaY
			return valid

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
	global depth
	xMouse = event.x
	yMouse = event.y
	if running:
		if xMouse>=450 and yMouse<=50:
			root.destroy()
		elif xMouse<=50 and yMouse<=50:
			playGame()
		else:
			#Is it the player's turn?
			if board.player==0:
				#Delete the highlights
				x = int((event.x-50)/50)
				y = int((event.y-50)/50)
				#Determine the grid index for where the mouse was clicked
				
				#If the click is inside the bounds and the move is valid, move to that location
				if 0<=x<=7 and 0<=y<=7:
					if valid(board.array,board.player,x,y):
						board.boardMove(x,y)
	else:
		#Difficulty clicking
		if 300<=yMouse<=350:
			#One star
			if 25<=xMouse<=155:
				depth = 1
				playGame()
			#Two star
			elif 180<=xMouse<=310:
				depth = 4
				playGame()
			#Three star
			elif 335<=xMouse<=465:
				depth = 6
				playGame()

def keyHandle(event):
	symbol = event.keysym
	if symbol.lower()=="r":
		playGame()
	elif symbol.lower()=="q":
		root.destroy()
