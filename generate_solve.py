#Ece Kamer Takmaz - 11823453
import urllib.request
import numpy as np
from bs4 import BeautifulSoup
import pycosat
import os
import sys

solver = str(sys.argv[1]) #solver to use
type_of_sudoku = str(sys.argv[2]) #sudoku types to solve
difficulty = int(sys.argv[3]) #level of difficulty for regular sudokus

def find_regions(borders):
	regions = np.zeros((81)).reshape(9,9)
	regions = regions - 1
	checked = {(0,0):-1, (0,1):-1, (0,2):-1, (0,3):-1, (0,4):-1, (0,5):-1, (0,6):-1, (0,7):-1, (0,8):-1, (1,0):-1, (1,1):-1, (1,2):-1, (1,3):-1, (1,4):-1, (1,5):-1, (1,6):-1, (1,7):-1, (1,8):-1, (2,0):-1, (2,1):-1, (2,2):-1, (2,3):-1, (2,4):-1, (2,5):-1, (2,6):-1, (2,7):-1, (2,8):-1, (3,0):-1, (3,1):-1, (3,2):-1, (3,3):-1, (3,4):-1, (3,5):-1, (3,6):-1, (3,7):-1, (3,8):-1, (4,0):-1, (4,1):-1, (4,2):-1, (4,3):-1, (4,4):-1, (4,5):-1, (4,6):-1, (4,7):-1, (4,8):-1, (5,0):-1, (5,1):-1, (5,2):-1, (5,3):-1, (5,4):-1, (5,5):-1, (5,6):-1, (5,7):-1, (5,8):-1, (6,0):-1, (6,1):-1, (6,2):-1, (6,3):-1, (6,4):-1, (6,5):-1, (6,6):-1, (6,7):-1, (6,8):-1, (7,0):-1, (7,1):-1, (7,2):-1, (7,3):-1, (7,4):-1, (7,5):-1, (7,6):-1, (7,7):-1, (7,8):-1, (8,0):-1, (8,1):-1, (8,2):-1, (8,3):-1, (8,4):-1, (8,5):-1, (8,6):-1, (8,7):-1, (8,8):-1}
	
	stack = []
	regions[0][0] = 0
	checked[(0,0)] = 0
	reg = 0
	stack.append((0,0))
	#print(stack)
	check_neighbours(checked, regions, borders, 0,0,reg, stack)
	stack.remove((0,0))
	#print(stack)
	
	while len(stack) != 0:
		picked = stack[0]
		check_neighbours(checked, regions, borders, picked[0], picked[1],reg, stack)
		stack.pop(0)
		#print(stack)

	itemindex = np.where(regions == -1)

	while(itemindex[0].shape[0] != 0):
		
		reg = reg + 1
		
		#print(reg)

		#print(itemindex[0][0],itemindex[1][0])
		regions[itemindex[0][0]][itemindex[1][0]] = reg
		checked[(itemindex[0][0],itemindex[1][0])] = reg
		stack.append((itemindex[0][0],itemindex[1][0]))
		
		while len(stack) != 0:
			picked = stack[0]
			check_neighbours(checked, regions, borders, picked[0], picked[1],reg, stack)
			stack.pop(0)
			#print(stack)
		itemindex = np.where(regions == -1)
	

	#print(regions) region id starts with 0
	return regions	 
			
def check_neighbours(checked, regions, borders, r,c,reg,stack):
	left = (r,c-1)
	right = (r,c+1)
	below = (r+1,c)
	above = (r-1,c)

	if(borders[r][c] == 0):
		if index_correct(left[0],left[1]):
			if (borders[left[0]][left[1]] == 0 or borders[left[0]][left[1]] == 3) and checked[(left[0],left[1])] == -1 :
				checked[(left[0],left[1])] = reg
				regions[left[0]][left[1]] = reg
				stack.append(left)
				#print("a",left)
		if index_correct(right[0],right[1]) and checked[(right[0],right[1])] == -1:
			regions[right[0]][right[1]] = reg
						
			checked[(right[0],right[1])] = reg
			stack.append(right)
			#print("b",right)
		if index_correct(below[0],below[1]) and checked[(below[0],below[1])] == -1:
			regions[below[0]][below[1]] = reg
			
			checked[(below[0],below[1])] = reg
			stack.append(below)
			#print("c",below)
		if index_correct(above[0],above[1]) and checked[(above[0],above[1])] == -1:
			if borders[above[0]][above[1]] != 2 and  borders[above[0]][above[1]] != 3:
				regions[above[0]][above[1]] = reg
			
				checked[(above[0],above[1])] = reg
				stack.append(above)
			#print("d",above)
	elif(borders[r][c] == 1):
		if index_correct(below[0],below[1]) and checked[(below[0],below[1])] == -1:
			regions[below[0]][below[1]] = reg
			
			checked[(below[0],below[1])] = reg
			stack.append(below)
			#print("e",below, r,c)
		if index_correct(left[0],left[1]) and checked[(left[0],left[1])] == -1:
			if borders[left[0]][left[1]] == 0 or borders[left[0]][left[1]] == 3:
				checked[(left[0],left[1])] = reg
				regions[left[0]][left[1]] = reg
				stack.append(left)
				#print("f",left)
		if index_correct(above[0],above[1]) and checked[(above[0],above[1])] == -1:
			if borders[above[0]][above[1]] != 2 and  borders[above[0]][above[1]] != 3:
				regions[above[0]][above[1]] = reg
			
				checked[(above[0],above[1])] = reg
				stack.append(above)
				#print("g",above)
	elif(borders[r][c] == 2):
		if index_correct(left[0],left[1]) and checked[(left[0],left[1])] == -1:
			if borders[left[0]][left[1]] == 0 or borders[left[0]][left[1]] == 3:
				checked[(left[0],left[1])] = reg
				regions[left[0]][left[1]] = reg
				stack.append(left)
		if index_correct(above[0],above[1]) and checked[(above[0],above[1])] == -1:
			if borders[above[0]][above[1]] != 2 and  borders[above[0]][above[1]] != 3:
				regions[above[0]][above[1]] = reg
			
				checked[(above[0],above[1])] = reg
				stack.append(above)
	elif(borders[r][c] == 3):
		if index_correct(right[0],right[1]) and checked[(right[0],right[1])] == -1:
			regions[right[0]][right[1]] = reg
						
			checked[(right[0],right[1])] = reg
			stack.append(right)
		if index_correct(left[0],left[1]) and checked[(left[0],left[1])] == -1:
			if borders[left[0]][left[1]] == 0 or borders[left[0]][left[1]] == 3:
				checked[(left[0],left[1])] = reg
				regions[left[0]][left[1]] = reg
				stack.append(left)
		if index_correct(above[0],above[1]) and checked[(above[0],above[1])] == -1:
			if borders[above[0]][above[1]] != 2 and  borders[above[0]][above[1]] != 3:
				regions[above[0]][above[1]] = reg
			
				checked[(above[0],above[1])] = reg
				stack.append(above)


def index_correct(r,c):
	if(r>=0 and r<9 and c>=0 and c<9):
		return True
	
#there are 18345 9x9 jigsaw puzzles currently

def get_difficulties():
	fd = open("difficulties.txt","w") 

	for i in range(1,18346):
		f = urllib.request.urlopen("http://www.menneske.no/sudoku/irr/3/eng/utskrift.html?number="+ str(i))
		soup = str(BeautifulSoup(f, 'html.parser'))
		#print(soup[str(soup).find("Difficulty"):].split("<")[0])
		dif = soup[str(soup).find("Difficulty"):].split("<")[0].split(" ")
		fd.write(str(i) + "," + dif[1] + "," + dif[2] + "\n")

def get_sudokus_and_regions(count):
	
	print("Getting " + str(count) + " irregular puzzles")
	for i in range(1,count+1):
		f = urllib.request.urlopen("http://www.menneske.no/sudoku/irr/3/eng/solve.html?number=" + str(i))
		#f = urllib.request.urlopen("http://www.menneske.no/sudoku/irr/3/eng/showpuzzle.html?number=" + str(i))
		soup = BeautifulSoup(f, 'html.parser')
		td = soup.form.find_all("td")
	
		sudoku = np.zeros((81))
		borders = np.zeros((81))
	
		el = 0 #index of element in an array of 81 items

		for t in td:
			tx = t.text
		
			if(len(tx) == 1):
				#print(tx)
				sudoku[el] = int(str(tx))
			else:
				#print("0")
				sudoku[el] = 0
		
			cl = t.get('class')[0]
		
			if(cl == 'normal'):
				borders[el] = 0
			elif(cl == 'rightedge'):
				borders[el] = 1
			elif(cl =='bottomright'):
				borders[el] = 2
			elif(cl =='bottomedge'):
				borders[el] = 3


			el = el + 1

		#print('sudoku',i)

		sudoku = sudoku.reshape(9,9)

		np.savetxt("sudoku_irregular/sudoku_"+str(i), sudoku)

		#print(sudoku)

		#print('borders')

		borders = borders.reshape(9,9)

		#print(borders)

		regions = find_regions(borders)

		np.savetxt("regions_irregular/regions_"+str(i), regions)

		#print('regions',i)
	
		#print(regions)


def get_normal_sudokus_and_regions(diff, count):

	print("Getting " + str(count) + " regular sudoku puzzles of difficulty " + str(diff))
	ids = []
	for i in range(1,count+1):
		#VERY EASY
		f = urllib.request.urlopen("http://www.menneske.no/sudoku/eng/random.html?diff=" + str(diff))
		soup = BeautifulSoup(f, 'html.parser')
		strsoup = str(soup)
		sudoku_id = int(strsoup[strsoup.find("Showing puzzle number"):].split("<")[0].split(" ")[3])
		
		while(sudoku_id in ids):
			f = urllib.request.urlopen("http://www.menneske.no/sudoku/eng/random.html?diff=" + str(diff))
			soup = BeautifulSoup(f, 'html.parser')
			strsoup = str(soup)
			sudoku_id = int(strsoup[strsoup.find("Showing puzzle number"):].split("<")[0].split(" ")[3])
		
		tr = soup.find_all("tr",{"class":"grid"})
		
		sudoku = np.zeros((81))
		
		el = 0 #index of element in an array of 81 items
		
		for t in tr:
			tx = t.text.split("\n")
			txn = np.asarray(tx[1:len(tx)-1])
			txn[txn == ''] = 0
			txn[txn == "\xa0"] = 0
			
			for e in txn:
				sudoku[el] = int(str(e))
			
				el = el + 1
			
		sudoku = sudoku.reshape(9,9)
		
		#print(sudoku_id)
		ids.append(sudoku_id)
		#print(sudoku)		
		np.savetxt("sudoku_regular/sudoku_normal_" + str(diff) + "_" +str(i), sudoku)
		
def convert_to_cnf(ind):
	reg = np.loadtxt("regions_irregular/regions_" + str(ind))
	sud = np.loadtxt("sudoku_irregular/sudoku_" + str(ind))
	
	clauses = []
	regions = {} #key is index tuple
	rev_regions = {} #key is region id

	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			#print(sud[i][j])
			reg_value = int(reg[i][j])
			regions[(i+1,j+1)] = reg_value
			if reg_value in rev_regions:
				rev_regions[reg_value].append((i+1,j+1))
			else:
				rev_regions[reg_value] = [(i+1,j+1)]
			#clues given in the puzzle
			#if they are not 0
			clue = int(sud[i][j])
			if clue != 0:
				clauses.append([int(str(i+1) + str(j+1) + str(clue))])
				#print([str(i+1) + str(j+1) + str(clue)])

	#print(regions)
	#print(rev_regions)

	#rules go here

	#at least one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			disj = []
			for n in range(1,10):
				disj.append(int(str(i+1) + str(j+1) + str(n)))
				
			clauses.append(disj)
			#print(disj)
	
	#exactly one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			for n in range(1,10):
				for m in range(1,10):
					disj = []
				
					if n != m:
						disj.append(int("-" + str(i+1) + str(j+1) + str(m)))
						disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						clauses.append(disj)
						#print(disj)


	#a number exactly once in a row

	#each row contains at least one n
	for n in range(1,10):
			
		for i in range(0,sud.shape[0]):
			disj = []
			for j in range(0,sud.shape[1]):
				disj.append(int(str(i+1) + str(j+1) + str(n)))
				
			clauses.append(disj)
			#print(disj)

	#each row contains at most one n

	for n in range(1,10):
			
			
		for i in range(0,sud.shape[0]):
			for j in range(0,sud.shape[1]):
				for js in range(0,sud.shape[1]):
					disj = []
				
					if j!=js:
						disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						
						disj.append(int("-" + str(i+1) + str(js+1) + str(n)))
						#print(disj)
						clauses.append(disj)



	#a number exactly once in a column

	#each column contains at least one n
	
	for n in range(1,10):
			
		for j in range(0,sud.shape[0]):
			disj = []
			for i in range(0,sud.shape[1]):
				disj.append(int(str(i+1) + str(j+1) + str(n)))
				
			clauses.append(disj)
			#print(disj)

	#each column contains at most one n

	for n in range(1,10):
			
			
		for j in range(0,sud.shape[0]):
			for i in range(0,sud.shape[1]):
				for ins in range(0,sud.shape[1]):
					disj = []
				
					if i!=ins:
						disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						
						disj.append(int("-" + str(ins+1) + str(j+1) + str(n)))
						#print(disj)
						clauses.append(disj)

	#a number exactly once in a block

	#each block contains at least one n
	
	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			disj = []
			for t in rev_regions[r]:
				#print(t)
				disj.append(int(str(t[0]) + str(t[1]) + str(n)))
			#print(disj)
			clauses.append(disj)
				
	#each block contains at most one n

	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			
			for t in rev_regions[r]:
				#print(t)
				for t2 in rev_regions[r]:
					disj = []
					#print(t[0],t2[0],t[1],t2[1])
					if not(t[0] == t2[0] and t[1] == t2[1]):
						disj.append(int("-" + str(t[0]) + str(t[1]) + str(n)))
						disj.append(int("-" + str(t2[0]) + str(t2[1]) + str(n)))
						#print(disj)
						clauses.append(disj)

	#print(clauses)
	#print(len(clauses))
	
	clauses_np = np.asarray(clauses)
	#print(clauses_np.shape)
	cnf = ""
	#set_of_atoms = set()
	
	no_of_variables = "729"
	no_of_clauses = str(len(clauses))
	cnf = cnf + "p cnf " + no_of_variables + " " + no_of_clauses + "\n"
	
	for dsj in clauses:
		#print(dsj)
		for atom in dsj:
			cnf = cnf + str(atom) + " "
			#set_of_atoms.add(atom)
		cnf = cnf + "0\n"
		
	#print(len(set_of_atoms)) #finds 1458 = 729 * 2 including the negated atoms
	
	'''
	for a in sorted(set_of_atoms):
		print(a,"\n")
	'''
		
	return cnf, clauses
	
	
	
def convert_to_cnf_normal(ind,diff):
	reg = np.array([[0,0,0,1,1,1,2,2,2],[0,0,0,1,1,1,2,2,2],[0,0,0,1,1,1,2,2,2],[3,3,3,4,4,4,5,5,5],[3,3,3,4,4,4,5,5,5],[3,3,3,4,4,4,5,5,5],[6,6,6,7,7,7,8,8,8],[6,6,6,7,7,7,8,8,8],[6,6,6,7,7,7,8,8,8]])
	
	sud = np.loadtxt("sudoku_regular/sudoku_normal_" + str(diff) + "_" +str(ind))
	
	clauses = []
	regions = {} #key is index tuple
	rev_regions = {} #key is region id

	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			#print(sud[i][j])
			reg_value = int(reg[i][j])
			regions[(i+1,j+1)] = reg_value
			if reg_value in rev_regions:
				rev_regions[reg_value].append((i+1,j+1))
			else:
				rev_regions[reg_value] = [(i+1,j+1)]
			#clues given in the puzzle
			#if they are not 0
			clue = int(sud[i][j])
			if clue != 0:
				clauses.append([int(str(i+1) + str(j+1) + str(clue))])
				#print([str(i+1) + str(j+1) + str(clue)])

	#print(regions)
	#print(rev_regions)

	#rules go here

	#at least one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			disj = []
			for n in range(1,10):
				disj.append(int(str(i+1) + str(j+1) + str(n)))
				
			clauses.append(disj)
			#print(disj)
	
	#exactly one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			for n in range(1,10):
				for m in range(1,10):
					disj = []
				
					if n != m:
						disj.append(int("-" + str(i+1) + str(j+1) + str(m)))
						disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						clauses.append(disj)
						#print(disj)


	#a number exactly once in a row

	#each row contains at least one n
	for n in range(1,10):
			
		for i in range(0,sud.shape[0]):
			disj = []
			for j in range(0,sud.shape[1]):
				disj.append(int(str(i+1) + str(j+1) + str(n)))
				
			clauses.append(disj)
			#print(disj)

	#each row contains at most one n

	for n in range(1,10):
			
			
		for i in range(0,sud.shape[0]):
			for j in range(0,sud.shape[1]):
				for js in range(0,sud.shape[1]):
					disj = []
				
					if j!=js:
						disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						
						disj.append(int("-" + str(i+1) + str(js+1) + str(n)))
						#print(disj)
						clauses.append(disj)



	#a number exactly once in a column

	#each column contains at least one n
	
	for n in range(1,10):
			
		for j in range(0,sud.shape[0]):
			disj = []
			for i in range(0,sud.shape[1]):
				disj.append(int(str(i+1) + str(j+1) + str(n)))
				
			clauses.append(disj)
			#print(disj)

	#each column contains at most one n

	for n in range(1,10):
			
			
		for j in range(0,sud.shape[0]):
			for i in range(0,sud.shape[1]):
				for ins in range(0,sud.shape[1]):
					disj = []
				
					if i!=ins:
						disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						
						disj.append(int("-" + str(ins+1) + str(j+1) + str(n)))
						#print(disj)
						clauses.append(disj)

	#a number exactly once in a block

	#each block contains at least one n
	
	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			disj = []
			for t in rev_regions[r]:
				#print(t)
				disj.append(int(str(t[0]) + str(t[1]) + str(n)))
			#print(disj)
			clauses.append(disj)
				
	#each block contains at most one n

	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			
			for t in rev_regions[r]:
				#print(t)
				for t2 in rev_regions[r]:
					disj = []
					#print(t[0],t2[0],t[1],t2[1])
					if not(t[0] == t2[0] and t[1] == t2[1]):
						disj.append(int("-" + str(t[0]) + str(t[1]) + str(n)))
						disj.append(int("-" + str(t2[0]) + str(t2[1]) + str(n)))
						#print(disj)
						clauses.append(disj)

	#print(clauses)
	#print(len(clauses))
	
	clauses_np = np.asarray(clauses)
	#print(clauses_np.shape)
	cnf = ""
	#set_of_atoms = set()
	
	no_of_variables = "729"
	no_of_clauses = str(len(clauses))
	cnf = cnf + "p cnf " + no_of_variables + " " + no_of_clauses + "\n"
	
	for dsj in clauses:
		#print(dsj)
		for atom in dsj:
			cnf = cnf + str(atom) + " "
			#set_of_atoms.add(atom)
		cnf = cnf + "0\n"
		
	#print(len(set_of_atoms)) #finds 1458 = 729 * 2 including the negated atoms
	
	'''
	for a in sorted(set_of_atoms):
		print(a,"\n")
	'''
		
	return cnf, clauses


def convert_to_cnf_1_initial_hard(ind,rep_dict, rev_rep_dict):

	#performs dictionary look-ups to start the variable numbers from 1 and not 111 (otherwise, ubcsat does not work properly)
	#string look-up to get value in rev_rep_dict as in dict['111'] = 1
	
	reg = np.loadtxt("regions_irregular/regions_" + str(ind))
	sud = np.loadtxt("sudoku_irregular/sudoku_" + str(ind))
	
	clauses = []
	regions = {} #key is index tuple
	rev_regions = {} #key is region id

	no_of_clues = 0
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			clue = int(sud[i][j])
			if clue != 0:
				no_of_clues = no_of_clues + 1
	
	difference = no_of_clues - 20
	
	remove = 0
	
	if(difference > 0):
		remove = difference
			
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			#print(sud[i][j])
			reg_value = int(reg[i][j])
			regions[(i+1,j+1)] = reg_value
			if reg_value in rev_regions:
				rev_regions[reg_value].append((i+1,j+1))
			else:
				rev_regions[reg_value] = [(i+1,j+1)]
			#clues given in the puzzle
			#if they are not 0
			clue = int(sud[i][j])
			if clue != 0:
				if remove > 0:
					removeClue = int(np.random.randint(2, size=1))
					
					if not removeClue:
						#clauses.append([int(str(i+1) + str(j+1) + str(clue))])
						clauses.append([rev_rep_dict[(str(i+1) + str(j+1) + str(clue))]])
				
						#print([str(i+1) + str(j+1) + str(clue)])
					
					else:
						remove = remove - 1
						#don't add the clue to the clauses
	#print(regions)
	#print(rev_regions)

	#rules go here

	#at least one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			disj = []
			for n in range(1,10):
				#disj.append(int(str(i+1) + str(j+1) + str(n)))
				disj.append(rev_rep_dict[(str(i+1) + str(j+1) + str(n))])
				
			clauses.append(disj)
			#print(disj)
	
	#exactly one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			for n in range(1,10):
				for m in range(1,10):
					disj = []
				
					if n != m:
						#disj.append(int("-" + str(i+1) + str(j+1) + str(m)))
						#disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
												
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(m)])))
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(n)])))
						
						clauses.append(disj)
						#print(disj)


	#a number exactly once in a row

	#each row contains at least one n
	for n in range(1,10):
			
		for i in range(0,sud.shape[0]):
			disj = []
			for j in range(0,sud.shape[1]):
				#disj.append(int(str(i+1) + str(j+1) + str(n)))
				disj.append(rev_rep_dict[(str(i+1) + str(j+1) + str(n))])
				
				
			clauses.append(disj)
			#print(disj)

	#each row contains at most one n

	for n in range(1,10):
			
			
		for i in range(0,sud.shape[0]):
			for j in range(0,sud.shape[1]):
				for js in range(0,sud.shape[1]):
					disj = []
				
					if j!=js:
						#disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						#disj.append(int("-" + str(i+1) + str(js+1) + str(n)))
						
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(n)])))
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(js+1) + str(n)])))
						#print(disj)
						clauses.append(disj)



	#a number exactly once in a column

	#each column contains at least one n
	
	for n in range(1,10):
			
		for j in range(0,sud.shape[0]):
			disj = []
			for i in range(0,sud.shape[1]):
				#disj.append(int(str(i+1) + str(j+1) + str(n)))
				disj.append(rev_rep_dict[(str(i+1) + str(j+1) + str(n))])
				
			clauses.append(disj)
			#print(disj)

	#each column contains at most one n

	for n in range(1,10):
			
			
		for j in range(0,sud.shape[0]):
			for i in range(0,sud.shape[1]):
				for ins in range(0,sud.shape[1]):
					disj = []
				
					if i!=ins:
						#disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						#disj.append(int("-" + str(ins+1) + str(j+1) + str(n)))
						
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(n)])))
						disj.append(int("-" + str(rev_rep_dict[str(ins+1) + str(j+1) + str(n)])))
						
						#print(disj)
						clauses.append(disj)

	#a number exactly once in a block

	#each block contains at least one n
	
	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			disj = []
			for t in rev_regions[r]:
				#print(t)
				#disj.append(int(str(t[0]) + str(t[1]) + str(n)))
				disj.append(rev_rep_dict[(str(t[0]) + str(t[1]) + str(n))])
				
			#print(disj)
			clauses.append(disj)
				
	#each block contains at most one n

	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			
			for t in rev_regions[r]:
				#print(t)
				for t2 in rev_regions[r]:
					disj = []
					#print(t[0],t2[0],t[1],t2[1])
					if not(t[0] == t2[0] and t[1] == t2[1]):
						#disj.append(int("-" + str(t[0]) + str(t[1]) + str(n)))
						#disj.append(int("-" + str(t2[0]) + str(t2[1]) + str(n)))
						
						disj.append(int("-" + str(rev_rep_dict[str(t[0]) + str(t[1]) + str(n)])))
						disj.append(int("-" + str(rev_rep_dict[str(t2[0]) + str(t2[1]) + str(n)])))
						
						#print(disj)
						clauses.append(disj)

	#print(clauses)
	#print(len(clauses))
	
	clauses_np = np.asarray(clauses)
	#print(clauses_np.shape)
	cnf = ""
	#set_of_atoms = set()
	
	no_of_variables = "729"
	no_of_clauses = str(len(clauses))
	cnf = cnf + "p cnf " + no_of_variables + " " + no_of_clauses + "\n"
	
	for dsj in clauses:
		#print(dsj)
		for atom in dsj:
			cnf = cnf + str(atom) + " "
			#set_of_atoms.add(atom)
		cnf = cnf + "0\n"
		
	#print(len(set_of_atoms)) #finds 1458 = 729 * 2 including the negated atoms
	
	'''
	for a in sorted(set_of_atoms):
		print(a,"\n")
	'''
		
	return cnf, clauses
	
	
	
def convert_to_cnf_normal_1_initial_hard(ind,diff,rep_dict,rev_rep_dict):
	
	#performs dictionary look-ups to start the variable numbers from 1 and not 111 (otherwise, ubcsat does not work properly)
	#string look-up to get value in rev_rep_dict as in dict['111'] = 1
	
	reg = np.array([[0,0,0,1,1,1,2,2,2],[0,0,0,1,1,1,2,2,2],[0,0,0,1,1,1,2,2,2],[3,3,3,4,4,4,5,5,5],[3,3,3,4,4,4,5,5,5],[3,3,3,4,4,4,5,5,5],[6,6,6,7,7,7,8,8,8],[6,6,6,7,7,7,8,8,8],[6,6,6,7,7,7,8,8,8]])
	
	sud = np.loadtxt("sudoku_regular/sudoku_normal_" + str(diff) + "_" +str(ind))
	
	clauses = []
	regions = {} #key is index tuple
	rev_regions = {} #key is region id

	no_of_clues = 0
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			clue = int(sud[i][j])
			if clue != 0:
				no_of_clues = no_of_clues + 1
	
	difference = no_of_clues - 20
	
	remove = 0
	
	if(difference > 0):
		remove = difference
		
		
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			#print(sud[i][j])
			reg_value = int(reg[i][j])
			regions[(i+1,j+1)] = reg_value
			if reg_value in rev_regions:
				rev_regions[reg_value].append((i+1,j+1))
			else:
				rev_regions[reg_value] = [(i+1,j+1)]
			#clues given in the puzzle
			#if they are not 0
			clue = int(sud[i][j])
			if clue != 0:
				if remove > 0:
					removeClue = int(np.random.randint(2, size=1))
					
					if not removeClue:
						#clauses.append([int(str(i+1) + str(j+1) + str(clue))])
						clauses.append([rev_rep_dict[(str(i+1) + str(j+1) + str(clue))]])
						#print([str(i+1) + str(j+1) + str(clue)])
					else:
						remove = remove - 1
						#don't add the clue to the clauses
						
						
	#print(regions)
	#print(rev_regions)

	#rules go here

	#at least one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			disj = []
			for n in range(1,10):
				#disj.append(int(str(i+1) + str(j+1) + str(n)))
				disj.append(rev_rep_dict[(str(i+1) + str(j+1) + str(n))])
				
			clauses.append(disj)
			#print(disj)
	
	#exactly one number in each cell
	for i in range(0,sud.shape[0]):
		for j in range(0,sud.shape[1]):
			for n in range(1,10):
				for m in range(1,10):
					disj = []
				
					if n != m:
						#disj.append(int("-" + str(i+1) + str(j+1) + str(m)))
						#disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(m)])))
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(n)])))
						
						
						clauses.append(disj)
						#print(disj)


	#a number exactly once in a row

	#each row contains at least one n
	for n in range(1,10):
			
		for i in range(0,sud.shape[0]):
			disj = []
			for j in range(0,sud.shape[1]):
				#disj.append(int(str(i+1) + str(j+1) + str(n)))
				disj.append(rev_rep_dict[(str(i+1) + str(j+1) + str(n))])
				
			clauses.append(disj)
			#print(disj)

	#each row contains at most one n

	for n in range(1,10):
			
			
		for i in range(0,sud.shape[0]):
			for j in range(0,sud.shape[1]):
				for js in range(0,sud.shape[1]):
					disj = []
				
					if j!=js:
						#disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						#disj.append(int("-" + str(i+1) + str(js+1) + str(n)))
			
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(n)])))
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(js+1) + str(n)])))
						
						#print(disj)
						clauses.append(disj)



	#a number exactly once in a column

	#each column contains at least one n
	
	for n in range(1,10):
			
		for j in range(0,sud.shape[0]):
			disj = []
			for i in range(0,sud.shape[1]):
				#disj.append(int(str(i+1) + str(j+1) + str(n)))
				disj.append(rev_rep_dict[(str(i+1) + str(j+1) + str(n))])
				
			clauses.append(disj)
			#print(disj)

	#each column contains at most one n

	for n in range(1,10):
			
			
		for j in range(0,sud.shape[0]):
			for i in range(0,sud.shape[1]):
				for ins in range(0,sud.shape[1]):
					disj = []
				
					if i!=ins:
						#disj.append(int("-" + str(i+1) + str(j+1) + str(n)))
						#disj.append(int("-" + str(ins+1) + str(j+1) + str(n)))
						
						disj.append(int("-" + str(rev_rep_dict[str(i+1) + str(j+1) + str(n)])))
						disj.append(int("-" + str(rev_rep_dict[str(ins+1) + str(j+1) + str(n)])))

						#print(disj)
						clauses.append(disj)

	#a number exactly once in a block

	#each block contains at least one n
	
	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			disj = []
			for t in rev_regions[r]:
				#print(t)
				#disj.append(int(str(t[0]) + str(t[1]) + str(n)))
				disj.append(rev_rep_dict[(str(t[0]) + str(t[1]) + str(n))])
				
			#print(disj)
			clauses.append(disj)
				
	#each block contains at most one n

	for r in rev_regions:
		#print(r)
		temp_reg = rev_regions[r]
		#print(temp_reg)
		for n in range(1,10):
			
			for t in rev_regions[r]:
				#print(t)
				for t2 in rev_regions[r]:
					disj = []
					#print(t[0],t2[0],t[1],t2[1])
					if not(t[0] == t2[0] and t[1] == t2[1]):
						#disj.append(int("-" + str(t[0]) + str(t[1]) + str(n)))
						#disj.append(int("-" + str(t2[0]) + str(t2[1]) + str(n)))
						
						disj.append(int("-" + str(rev_rep_dict[str(t[0]) + str(t[1]) + str(n)])))
						disj.append(int("-" + str(rev_rep_dict[str(t2[0]) + str(t2[1]) + str(n)])))
						
						#print(disj)
						clauses.append(disj)

	#print(clauses)
	#print(len(clauses))
	
	clauses_np = np.asarray(clauses)
	#print(clauses_np.shape)
	cnf = ""
	#set_of_atoms = set()
	
	no_of_variables = "729"
	no_of_clauses = str(len(clauses))
	cnf = cnf + "p cnf " + no_of_variables + " " + no_of_clauses + "\n"
	
	for dsj in clauses:
		#print(dsj)
		for atom in dsj:
			cnf = cnf + str(atom) + " "
			#set_of_atoms.add(atom)
		cnf = cnf + "0\n"
		
	#print(len(set_of_atoms)) #finds 1458 = 729 * 2 including the negated atoms
	
	'''
	for a in sorted(set_of_atoms):
		print(a,"\n")
	'''
		
	return cnf, clauses
		
		
def convert_cnf_to_sudoku(result):
	
	solution = np.zeros(81).reshape(9,9)
	
	for r in result:
		sr = str(r)
		i = int(sr[0]) - 1
		j = int(sr[1]) - 1
		n = int(sr[2])
		solution[i][j] = n
		
	return solution
	
def solve_normal_puzzles(diff, count, solver, rep_dict, rev_rep_dict):

	if(solver == "pycosat"):
		print("Solving " + str(count) + " regular sudoku puzzles of difficulty " + str(diff) + "with pycosat")
		for puzzle in range(1,count + 1):
			cnf, clauses = convert_to_cnf_normal_1_initial_hard(puzzle,diff,rep_dict,rev_rep_dict)
			
			#cnf, clauses = convert_to_cnf_normal(puzzle, diff)
			#print(cnf)
			#print(clauses)
	
			text_file = open("sudoku_regular/dimacs/dimacs_" + str(diff) + "_" + str(puzzle) + ".cnf", "w")

			text_file.write(cnf)

			text_file.close()
				
			pycosat.solve(clauses, verbose = 1)
	
	
def solve_irregular_puzzles(count, solver, rep_dict, rev_rep_dict):
	
	if(solver == "pycosat"):
		print("Solving " + str(count) + " irregular sudoku puzzles with pycosat")
		for puzzle in range(1,count + 1):
			cnf, clauses = convert_to_cnf_1_initial_hard(puzzle,rep_dict, rev_rep_dict)
			
			#cnf, clauses = convert_to_cnf(puzzle)
			#print(cnf)
			##print(clauses)
	
			text_file = open("sudoku_irregular/dimacs/dimacs_" + str(puzzle) + ".cnf", "w")

			text_file.write(cnf)

			text_file.close()
		
			pycosat.solve(clauses, verbose = 1)
	

'''
#HERE, THE PUZZLES ARE SCRAPED FROM THE WEBSITE
#WHEN SOLVING THE PUZZLES rather than collecting them, COMMENT THIS PART OUT 

count = 10000
get_normal_sudokus_and_regions(1, count) #arg[0] is difficulty, arg[1] is the number of puzzles to be scraped

get_normal_sudokus_and_regions(2, count) #arg[0] is difficulty, arg[1] is the number of puzzles to be scraped

get_normal_sudokus_and_regions(3, count) #arg[0] is difficulty, arg[1] is the number of puzzles to be scraped

get_normal_sudokus_and_regions(4, count) #arg[0] is difficulty, arg[1] is the number of puzzles to be scraped

get_normal_sudokus_and_regions(5, count) #arg[0] is difficulty, arg[1] is the number of puzzles to be scraped

#count = 18345 #current irregular count
#get_sudokus_and_regions(count) #arg[0] is the number of puzzles to be scraped

'''
#dimacs representations starting from 1 instead of 111
# 1:111 2:112 3:113 and so on

text_file = open("rep_dict.txt", "w")

count = 1

rep_dict = {}
rev_rep_dict = {}

for i in range(1, 10):
	for j in range(1,10):
		for k in range(1,10):
			rep_dict[count] = str(i) + str(j) + str(k)
			rev_rep_dict[str(i) + str(j) + str(k)] = count
			count = count + 1

text_file.write(str(rev_rep_dict))

text_file.close()

if(type_of_sudoku == "regular"):
	#solve regular sudokus
	count = 10000
	solve_normal_puzzles(difficulty, count, solver, rep_dict, rev_rep_dict)
	
elif(type_of_sudoku == "irregular"):
	#solve irregular sudokus
	count = 18345 #current irregular count
	solve_irregular_puzzles(count,solver, rep_dict, rev_rep_dict)

