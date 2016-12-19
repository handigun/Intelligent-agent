import copy
import time
you = ''
def opp_play(youplay):
	if youplay == 'O':
		return 'X'
	elif youplay == 'X':
		return 'O'

def find_max(lst):
	maximum = float("-inf")
	indice = (-1,-1)
	for i in range(len(lst)):
		if max(lst[i]) > maximum:
			maximum = max(lst[i])
			indice = (i,lst[i].index(maximum))
	return maximum, indice

def write_out(string, indices, board):
	f1 = open("output.txt","w")
	i = indices[0]
	j = indices[1]
	out = chr(j + ord('A')) + str(i+1)
	out +=' '
	out += string
	board[i][j] = you
	if string == "Raid":
		neighbor = find_neighbors(board, i, j)
		mem_state = []
		for mem in neighbor:
			if mem['state'] == opp_play(you):
				board[mem['i']][mem['j']] = you
	n = len(board)
	for i in range(n):
		out += '\n'
		out += ''.join(board[i])
	f1.write(out)


def minimax(cost, state, youplay, depth):
	n = len(cost)
	# value = copy.deepcopy(cost)
	board = copy.deepcopy(state)
	depth_req = depth
	stake_value = [[float("-inf")]*n for k in range(n)]
	raid_value = [[float("-inf")]*n for k in range(n)]
	for i in range(n):
		for j in range(n):
			if board[i][j] == '.':
				board[i][j] = youplay
				stake_value[i][j] = MIN_VALUE(board, opp_play(youplay), cost, depth-1, 0, 0, False)[0]
				board = copy.deepcopy(state)
	for i in range(n):
		for j in range(n):
			if board[i][j] == youplay:
				raid_board = copy.deepcopy(board)
				neighbor = find_neighbors(board, i, j)
				for mem in neighbor:
					if mem['state'] == '.':
						point_neighbour = find_neighbors(board, mem['i'], mem['j'])
						for member in point_neighbour:
							if member['state'] == opp_play(youplay):
								raid_board[member['i']][member['j']] = youplay
								raid_board[mem['i']][mem['j']] = youplay
						if board != raid_board:
							raid_value[mem['i']][mem['j']] = MIN_VALUE(raid_board, opp_play(youplay), cost, depth-1, 0, 0, False)[0]
							raid_board = copy.deepcopy(board)
	max_val,max_index = find_max(stake_value)
	max_raid_val, max_raid_index = find_max(raid_value)
	if max_val >= max_raid_val:
		#print "Stake",max_index,state
		write_out("Stake",max_index,state)
	else:
		#print "Raid", max_raid_index,state
		write_out("Raid", max_raid_index,state)
	#need to find max of all i, j in value
# def is_neighbor(board, i, j):


def alphabeta(cost, state, youplay, depth):
	inp = copy.deepcopy(state)
	v, res = MAX_VALUE(inp, youplay, cost, depth, float("-inf"), float("inf"), True)
	#print(v)
	indices = (res[0], res[1])
	#print(indices)
	write_out(res[2], indices, state)

def MAX_VALUE(board, youplay, cost, depth, alpha, beta, mode):
	if terminal(board) or depth == 0:
		return (calc_utility(board,cost),None)
	v = float("-inf")
	cur = copy.deepcopy(board)
	for i in range(n):
		for j in range(n):
			if board[i][j] == '.':
				board[i][j] = youplay
				stake_res = MIN_VALUE(board, opp_play(youplay), cost, depth-1, alpha, beta, mode)[0]
				#v = max(v, stake_res)
				if v < stake_res:
					v = stake_res
 					res = [i, j, "Stake"]
 				board = copy.deepcopy(cur)
 				if mode:
 					if v >= beta:
 						return (v, res)
					alpha = max(alpha, v)
			#print i,j,v, "stake"
	for i in range(n):
		for j in range(n):
			if board[i][j] == youplay:
				# print i,j
				raid_board = copy.deepcopy(board)
				neighbor = find_neighbors(board, i, j)
				for mem in neighbor:
					if mem['state'] == '.':
						
						point_neighbour = find_neighbors(board, mem['i'], mem['j'])
						for member in point_neighbour:
							if member['state'] == opp_play(youplay):
								raid_board[member['i']][member['j']] = youplay
								raid_board[mem['i']][mem['j']] = youplay
						if board != raid_board:
							raid_res = MIN_VALUE(raid_board, opp_play(youplay), cost, depth-1, alpha, beta, mode)[0]
							#v = max(v, raid_res)
							if v < raid_res:
								v = raid_res
			 					res = [mem['i'], mem['j'], "Raid"]
		 					if mode:
			 					if v >= beta:
			 						return (v, res)
								alpha = max(alpha, v)

							raid_board = copy.deepcopy(board)
			#print i,j,v, "raid"

	return (v, res)


def MIN_VALUE(board, youplay, cost, depth, alpha, beta, mode):
	if terminal(board) or depth == 0:
		return (calc_utility(board,cost),None)
	v = float("inf")
	cur = copy.deepcopy(board)
	for i in range(n):
		for j in range(n):
			if board[i][j] == '.':
				board[i][j] = youplay
				stake_res = MAX_VALUE(board, opp_play(youplay), cost, depth-1, alpha, beta, mode)[0]
 				#v = min(v, stake_res)
 				if v > stake_res:
 					v = stake_res
 					res = [i, j, "Stake"]
 				board = copy.deepcopy(cur)
 				if mode:
 					if v <= alpha:
 						return (v, res)
 					beta = min(beta, v)
 			#print i,j,v, "stake"
 	for i in range(n):
		for j in range(n):
			if board[i][j] == youplay:
				raid_board = copy.deepcopy(board)
				neighbor = find_neighbors(board, i, j)
				for mem in neighbor:

					if mem['state'] == '.':
						point_neighbour = find_neighbors(board, mem['i'], mem['j'])
						for member in point_neighbour:
							if member['state'] == opp_play(youplay):
								raid_board[member['i']][member['j']] = youplay
								raid_board[mem['i']][mem['j']] = youplay
						if board != raid_board:
							raid_res = MAX_VALUE(raid_board, opp_play(youplay), cost, depth-1, alpha, beta, mode)[0]
							#v = min(v, raid_res)
							if v > raid_res:
								v = raid_res
			 					res = [mem['i'], mem['j'], "Raid"]
			 				if mode:
			 					if v <= alpha:
			 						return (v, res)
			 					beta = min(beta, v)

							raid_board = copy.deepcopy(board)
			#print i,j,v, "raid"
	return (v,res)


def find_neighbors(board, i, j):
	n_lst = [[i-1, j],[i+1,j],[i,j-1],[i,j+1]]
	n = len(board)
	neighbours = []
	if j-1 >= 0:
	 	neighbours.append({"state":board[i][j-1],"i":i,"j":j-1})
	if j+1 < n:
	 	neighbours.append({"state":board[i][j+1],"i":i,"j":j+1})
	if i+1 < n:
	 	neighbours.append({"state":board[i+1][j],"i":i+1,"j":j})
	if i-1 >= 0:
		neighbours.append({"state":board[i-1][j],"i":i-1,"j":j})
	return neighbours

def terminal(board):
	n = len(board)
	for i in range(n):
		for j in range(n):
			if board[i][j] == '.':
				return False
	return True

def calc_utility(board,cost):
	global you
	
	n = len(board)
	sum_x = 0
	sum_o = 0
	for i in range(n):
		for j in range(n):
			if board[i][j] == 'X':
				sum_x += cost[i][j]
			elif board[i][j] == 'O':
				sum_o += cost[i][j]
	if you == 'O':
		return sum_o-sum_x
	elif you == 'X':
		return sum_x-sum_o


if __name__ == '__main__':
	start = time.time()
	f = open("input.txt","r")
	s = f.read()
	lst = s.split("\n")
	n = int(lst[0])
	mode = lst[1]
	youplay = lst[2]
	you = lst[2]
	depth = int(lst[3])
	cost = [[0]*n for k in range(n)]
	state = [[0]*n for k in range(n)]
	for i in range(n):
		cost_lst = lst[i+4].split(' ')
		state_lst = lst[i+n+4]
		for j in range(n):
			cost[i][j] = int(cost_lst[j])
			state[i][j] = state_lst[j]
	if mode == 'MINIMAX':
		minimax(cost, state, youplay, depth)
		end = time.time()
		print end - start
	elif mode == "ALPHABETA":
		alphabeta(cost, state, youplay, depth)
		end = time.time()
		print end - start
	f.close()
