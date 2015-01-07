import random
import math

n = 9
board = [['0' for x in range(n)] for x in range(n)]
searching = False
okay = True
nope = False
pMoves = []
turn = 1
oppcolor = raw_input("'W' or 'B'|>")
balance = 50

##hardcode for 9x9
walls = [0,8]
corners = [(0,0),(0,8),(8,0),(8,8)]
##

if oppcolor == 'W':
	color = 'B'
else:
	color = 'W'

def boardState (board):
	print "  1  2  3  4  5  6  7  8  9"
	n = 0
	nums = ["1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 "]
	for row in board:
		print nums[n] + '  '.join(map(str, row))
		n += 1

def playerMove ((x, y), cboard, color):
	cboard[y][x] = color

def checkAtari (board, n=3):
	inatari = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			threats = checkAdj(i, j, board, oppcolor)
			inatari += [(j, i)] if len(threats) == n else []
	return inatari

def checkHane (board, n=2):
	return checkAtari(board, n)

def checkAdj (j, i, board, c, n=1):
	adj = []
	
	#hardcode for 9x9
	offhigh = 8 if n == 1 else 7
	offlow = 0 if n == 1 else 1
	##
	
	if i > offlow:
		adj += [(j, i-n)] if board[i-n][j] == c else []
	if i < offhigh:
		adj += [(j, i+n)] if board[i+n][j] == c else []
	if j > offlow:
		adj += [(j-n, i)] if board[i][j-n] == c else []
	if j < offhigh:
		adj += [(j+n, i)] if board[i][j+n] == c else []
	
	return adj

def checkDiag (j, i, board, c, n=1):
	diag = []
	
	#hardcode for 9x9
	offhigh = 8 if n == 1 else 7
	offlow = 0 if n == 1 else 1
	##
	
	if i > offlow and offlow > 0:
		diag += [(j-n, i-n)] if board[i-n][j-n] == c else []
	if i < offhigh and j < offhigh:
		diag += [(j+n, i+n)] if board[i+n][j+n] == c else []
	if i < offhigh and j > offlow:
		diag += [(j-n, i+n)] if board[i+n][j-n] == c else []
	if i > offlow and j < offhigh:
		diag += [(j+n, i-n)] if board[i-n][j+n] == c else []
	
	return diag

def checkConnect ((j, i), board, c):
	adj = checkAdj(j, i, board, c, 2)
	diag = checkDiag(j, i, board, c, 2)
	
	if len(adj) > 0:
		return True
	elif len(diag) > 0:
		return True
	else:
		return False
	
def pMoves (board):
	pMoves = []

	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == '0':
				pMoves = pMoves + [(j, i)]
	
	return pMoves

#this needs to be a more robust definition of being dead
def isDead ((j, i), board):
	friendly = checkAdj(j,i,board,color)
	if friendly < 1:
		return True
	else:
		return False

def distFromWall((j,i), board):
	a = abs(0+j)
	b = abs(8-j)
	c = abs(0+i)
	d = abs(8-i)
	test = [a,b,c,d]
	wdist = 0
	if j in walls or i in walls:
		return 0
	else:
		for n in range(1,len(test)-1):
			if test[n] > test[n-1]:
				wdist = test[n-1]
			else:
				continue
	return wdist
		##hardcode for 9x9
		
		##

def distFromCorner((j,i),board):
	cdist = 0
	if (j,i) in corners:
		return 0
	else:
		for i in range(4):
			if i == 0:
				dist = math.sqrt((j - corners[i][0])**2 + (i - corners[i][1])**2)
			elif cdist > math.sqrt((j - corners[i][0])**2 + (i - corners[i][1])**2):
				cdist = math.sqrt((j - corners[i][0])**2 + (i - corners[i][1])**2)
			else:
				continue
	return cdist

def distFromOpp(board):	
	oppstones = []
	mystones = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == oppcolor:
				oppstones = oppstones + [(j, i)]
			if board[i][j] == color:
				mystones = mystones + [(j, i)]
	hdist = 0
	vdist = 0
	for oppstone in oppstones:
		for mystone in mystones:
			hdist += oppstone[0] - mystone[0]
			vdist += oppstone[1] - mystone[1]
	tdist = vdist/hdist if hdist > 0 else vdist 
	return tdist

def fitness (queue, board):
	# sum up the liberties and distances between stones
	# get a feeling for the board idk
	# 'judge the strength of your shape'
	libs = []
	hdist = 0
	vdist = 0
	i = 1
	wcdist = 0
	#print queue
	for stone in queue:
		libs += checkAdj(stone[1],stone[0],board,'0')
		if i < len(queue):
			wcdist = distFromWall(stone,board) + int(distFromCorner(stone,board))
			hdist += abs(stone[1] - queue[i][1])
			vdist += abs(stone[0] - queue[i][0])
			i += 1
	tdist = vdist / hdist + distFromOpp(board) if hdist != 0 else 0
	return tdist + len(libs) + wcdist

def h (move, board, c):
	inatari = checkAtari(board)
	inhane = checkHane(board)
	
	if len(inatari) > 0:
		inatari_tmp = inatari[:]
		for atari in inatari_tmp:
			if isDead(atari,board):
				inatari.pop(inatari.index(atari))
	
	priorityq = inatari + inhane
	priorityqq = []
	for stone in priorityq:
		if checkConnect(stone, board, c):
			priorityqq += [stone]
	priorityq = priorityqq + [p for p in priorityq if p not in priorityqq]	
	return (move,fitness(priorityq, board))

def bestMove (queue):
	queue = sorted(queue, key=lambda q: q[1])
	#print queue
	bestm = (0,0) if queue == [] else queue[len(queue)-2]
	return bestm

def minimax (board, depth, maximizingPlayer, move):
	testBoard = [row[:] for row in board]
	if depth == 0:
		return h(move, board, color)
	if maximizingPlayer:
		bestValue = (move,-1)
		pmoves = pMoves(board)
		random.shuffle(pmoves)
		for possibleMove in pmoves:
			playerMove(possibleMove, testBoard, color)
			val = minimax(testBoard, depth - 1, nope, possibleMove)
#			print val
			tmpval = max(abs(bestValue[1]),val[1])
			if tmpval == val[1]:
				bestValue = (possibleMove,tmpval)
			else:
				bestValue = (move,tmpval)
	else:
		#hardcode for 9x9
		bestValue = (move,999999)
		###
		for possibleMove in pMoves(board):
			playerMove(possibleMove, testBoard, oppcolor)
			val = minimax(testBoard, depth - 1, okay, possibleMove)
			tmpval = min(abs(bestValue[1]), val[1])
			if tmpval == val[1]:
				bestValue = val
#	if len(moveq) > 0:
#		if bestValue[1] > moveq[len(moveq)-1][1]:
#			moveq += [bestValue]
#	else:
#		moveq += [bestValue]
	return bestValue 

#main
knight = (3,2)
corner = (2,2)
#print distFromWall(knight, board)
depth = int(raw_input("depth|>"))
while(True):
	print "Turn: " + str(turn)
	boardState(board)
	print "Your move."
	oppx = int(raw_input("x|>")) - 1
	oppy = int(raw_input("y|>")) - 1
	oppmove = (oppx,oppy)
	playerMove(oppmove, board, oppcolor)
	turn += 1
	boardState(board)
	print "Searching..."	
	minimove = minimax(board, depth, okay, corner)
	#print minimove
	print ((minimove[0][0] + 1, minimove[0][1] + 1), minimove[1])
	print distFromWall(minimove[0], board)
	print distFromCorner(minimove[0], board)
	print distFromOpp(board)
	playerMove(minimove[0], board, color)
	turn += 1
	if turn == 50:
		break
boardState(board)
#minimove = minimax(board, 3, okay, (1,1))
#print "==============="
#boardState(board)
#playerMove(minimove[0], board, 'B')
#boardState(board)
