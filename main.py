#Ece Kamer Takmaz - 11823453
import subprocess
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#THIS PART CREATES THE DIMACS BEFORE SOLVING WITH PYCOSAT
#FOLLOWING SOLVERS USE THOSE DIMACS FILES AND ARE PROCESSED VIA SHELL ONE BY ONE

'''
for i in range(1,6):
	print("Solving regular sudoku puzzles of difficulty " + str(i))
	proc = subprocess.Popen(["python generate_solve.py pycosat regular " + str(i)],shell = True, stdout = subprocess.PIPE).communicate()

	text_file = open("all_output_pycosat_regular_" + str(i) + ".txt", "w")
	text_file.write(proc[0].decode("utf-8"))
	text_file.close()

	
print("Solving irregular sudoku puzzles")		
proc = subprocess.Popen(["python generate_solve.py pycosat irregular 10"],shell = True,stdout = subprocess.PIPE).communicate()


text_file = open("all_output_pycosat_irregular.txt", "w")
text_file.write(proc[0].decode("utf-8"))
text_file.close()



#ALSO SOLVE USING UBCSAT
out = ""

for i in range(1,6):
	print("Solving regular sudoku puzzles of difficulty " + str(i))
	for c in range(1,10001):
		out = out + subprocess.Popen(["cd sudoku_regular/dimacs; ./ubcsat -alg saps -i dimacs_" + str(i) + "_" + str(c) + ".cnf"], shell = True, stdout = subprocess.PIPE).communicate()[0].decode("utf-8")

	text_file = open("all_output_ubcsat_regular_" + str(i) +".txt", "w")
	text_file.write(out)
	text_file.close()
	
	out = ""

	
proc = ""	
print("Solving irregular sudoku puzzles")		
for c in range(1, 18346):
	proc = proc + subprocess.Popen(["cd sudoku_irregular/dimacs; ./ubcsat -alg saps -i dimacs_" + str(c) + ".cnf"],shell = True, stdout = subprocess.PIPE).communicate()[0].decode("utf-8")


text_file = open("all_output_ubcsat_irregular.txt", "w")
text_file.write(proc)
text_file.close()



#ALSO SOLVE USING WALKSAT
out = ""

for i in range(1,6):
	print("Solving regular sudoku puzzles of difficulty " + str(i))
	for c in range(1,10001):
		out = out + subprocess.Popen(["cd sudoku_regular/dimacs; ./walksat dimacs_" + str(i) + "_" + str(c) + ".cnf"], shell = True, stdout = subprocess.PIPE).communicate()[0].decode("utf-8")

	text_file = open("all_output_walksat_regular_" + str(i) +".txt", "w")
	text_file.write(out)
	text_file.close()
	
	out = ""

	
proc = ""	
print("Solving irregular sudoku puzzles")		
for c in range(1, 18346):
	proc = proc + subprocess.Popen(["cd sudoku_irregular/dimacs; ./walksat dimacs_" + str(c) + ".cnf"],shell = True, stdout = subprocess.PIPE).communicate()[0].decode("utf-8")


text_file = open("all_output_walksat_irregular.txt", "w")
text_file.write(proc)
text_file.close()



#ALSO SOLVE USING ZCHAFF
out = ""

for i in range(1,6):
	print("Solving regular sudoku puzzles of difficulty " + str(i))
	for c in range(1,10001):
		out = out + subprocess.Popen(["cd sudoku_regular/dimacs; ./zchaff dimacs_" + str(i) + "_" + str(c) + ".cnf"], shell = True, stdout = subprocess.PIPE).communicate()[0].decode("utf-8")

	text_file = open("all_output_zchaff_regular_" + str(i) +".txt", "w")
	text_file.write(out)
	text_file.close()
	
	out = ""

	
proc = ""	
print("Solving irregular sudoku puzzles")		
for c in range(1, 18346):
	proc = proc + subprocess.Popen(["cd sudoku_irregular/dimacs; ./zchaff dimacs_" + str(c) + ".cnf"],shell = True, stdout = subprocess.PIPE).communicate()[0].decode("utf-8")


text_file = open("all_output_zchaff_irregular.txt", "w")
text_file.write(proc)
text_file.close()

'''
def parse_pycosat():
	values = []
	
	pycosat_irregular_metrics = []
	pycosat_regular_metrics = []
	
	with open("all_output_pycosat_irregular.txt", "r") as f:
		for line in f:
			if(line[0:3] == "c 1"):
				values = line.split(" ")
			
				results = values[2:len(values) - 1] #removing c 1 at the beginning and \n at the end
				pycosat_irregular_metrics.append([float(x) for x in results if x != ''])
	
	for c in range(1,6):
		with open("all_output_pycosat_regular_" + str(c) + ".txt", "r") as f:
			for line in f:
				if(line[0:3] == "c 1"):
					values = line.split(" ")
			
					results = values[2:len(values) - 1] #removing c 1 at the beginning and \n at the end
					pycosat_regular_metrics.append([float(x) for x in results if x != ''])
	
	
	return pycosat_irregular_metrics, pycosat_regular_metrics
	
	'''
	c 
	c  seconds     variables   original    learned     agility
	c         level        used      conflicts    limit          MB
	c 
	c s   0.0   0.0   558  84.1   296     0   107     0   0.0   0.5 
	c 
	c initial reduction limit 100 clauses
	c 
	c 1   0.0  31.2   558  84.6   296     3   110  100   0.2   0.5 
	c 
	c  seconds     variables   original    learned     agility
	c         level        used      conflicts    limit          MB
	c 
	'''
				
			
def parse_zchaff():
	values = []
	
	zchaff_irregular_metrics = []
	zchaff_regular_metrics = []
	
	level = []
	num_decisions = []
	original_num_vars = []
	original_num_clauses = []
	original_num_literals = []
	added_conflict_clauses = []
	num_of_shrinkings = []
	deleted_conflict_clauses = []
	deleted_clauses = []
	added_conflict_literals = []
	deleted_literals = []
	num_implication = []
	runtime = []
	results = []
	
	
	with open("all_output_zchaff_irregular.txt", "r") as f:
		for line in f:
			if("Max Decision Level" in line):
				values = line.split("\t")
			
				level.append(float(values[4]))
			elif("Num. of Decisions" in line):
				
				values = line.split("\t")
				num_decisions.append(int(values[4]))
				
			elif("Original Num Variables" in line):

				values = line.split("\t")
				original_num_vars.append(int(values[4]))
			elif("Original Num Clauses" in line):

				values = line.split("\t")
				original_num_clauses.append(int(values[4]))
			elif("Original Num Literals" in line):

				values = line.split("\t")
				original_num_literals.append(int(values[4]))
				
			elif("Added Conflict Clauses" in line):

				values = line.split("\t")
				added_conflict_clauses.append(int(values[4]))
			elif("Num of Shrinkings" in line):

				values = line.split("\t")
				num_of_shrinkings.append(int(values[4]))
			elif("Deleted Conflict Clauses" in line):

				values = line.split("\t")
				deleted_conflict_clauses.append(int(values[3]))
			elif("Deleted Clauses" in line):

				values = line.split("\t")
				deleted_clauses.append(int(values[5]))
			elif("Added Conflict Literals" in line):

				values = line.split("\t")
				added_conflict_literals.append(int(values[4]))
			elif("Deleted (Total) Literals" in line):

				values = line.split("\t")
				deleted_literals.append(int(values[3]))
			elif("Number of Implication" in line):

				values = line.split("\t")
				num_implication.append(int(values[4]))
			elif("Total Run Time" in line):

				values = line.split("\t")
				runtime.append(float(values[5]))
			elif("RESULT:" in line):

				values = line.split("\t")
				results.append(values[1].split("\n")[0])
			
	level = np.asarray(level, dtype=np.float64)
	num_decisions = np.asarray(num_decisions, dtype=np.int64)
	original_num_vars = np.asarray(original_num_vars)
	original_num_clauses = np.asarray(original_num_clauses)
	original_num_literals = np.asarray(original_num_literals)
	added_conflict_clauses = np.asarray(added_conflict_clauses)
	num_of_shrinkings = np.asarray(num_of_shrinkings)
	deleted_conflict_clauses = np.asarray(deleted_conflict_clauses) 
	deleted_clauses = np.asarray(deleted_clauses)
	added_conflict_literals = np.asarray(added_conflict_literals)
	deleted_literals = np.asarray(deleted_literals)
	num_implication = np.asarray(num_implication)
	runtime = np.asarray(runtime)
	results = np.asarray(results)
	
	zchaff_irregular_metrics = np.stack((level,num_decisions,original_num_vars,original_num_clauses,original_num_literals,added_conflict_clauses,num_of_shrinkings,deleted_conflict_clauses,deleted_clauses,added_conflict_literals,deleted_literals,num_implication,runtime,results), axis = 1)
	
	
	#REGULAR
	
	
	level = []
	num_decisions = []
	original_num_vars = []
	original_num_clauses = []
	original_num_literals = []
	added_conflict_clauses = []
	num_of_shrinkings = []
	deleted_conflict_clauses = []
	deleted_clauses = []
	added_conflict_literals = []
	deleted_literals = []
	num_implication = []
	runtime = []
	results = []
	
	for c in range(1,6):
		with open("all_output_zchaff_regular_" + str(c) + ".txt", "r") as f:
			for line in f:
				if("Max Decision Level" in line):
					values = line.split("\t")
					
					level.append(float(values[4]))
				elif("Num. of Decisions" in line):
				
					values = line.split("\t")
					num_decisions.append(int(values[4]))
				
				elif("Original Num Variables" in line):

					values = line.split("\t")
					original_num_vars.append(int(values[4]))
				elif("Original Num Clauses" in line):

					values = line.split("\t")
					original_num_clauses.append(int(values[4]))
				elif("Original Num Literals" in line):

					values = line.split("\t")
					original_num_literals.append(int(values[4]))
				
				elif("Added Conflict Clauses" in line):

					values = line.split("\t")
					added_conflict_clauses.append(int(values[4]))
				elif("Num of Shrinkings" in line):

					values = line.split("\t")
					num_of_shrinkings.append(int(values[4]))
				elif("Deleted Conflict Clauses" in line):

					values = line.split("\t")
					deleted_conflict_clauses.append(int(values[3]))
				elif("Deleted Clauses" in line):

					values = line.split("\t")
					deleted_clauses.append(int(values[5]))
				elif("Added Conflict Literals" in line):

					values = line.split("\t")
					added_conflict_literals.append(int(values[4]))
				elif("Deleted (Total) Literals" in line):

					values = line.split("\t")
					deleted_literals.append(int(values[3]))
				elif("Number of Implication" in line):

					values = line.split("\t")
					num_implication.append(int(values[4]))
				elif("Total Run Time" in line):

					values = line.split("\t")
					runtime.append(float(values[5]))
				elif("RESULT:" in line):

					values = line.split("\t")
					results.append(values[1].split("\n")[0])
			
	level = np.asarray(level, dtype=np.float64)
	num_decisions = np.asarray(num_decisions, dtype=np.int64)
	original_num_vars = np.asarray(original_num_vars)
	original_num_clauses = np.asarray(original_num_clauses)
	original_num_literals = np.asarray(original_num_literals)
	added_conflict_clauses = np.asarray(added_conflict_clauses)
	num_of_shrinkings = np.asarray(num_of_shrinkings)
	deleted_conflict_clauses = np.asarray(deleted_conflict_clauses) 
	deleted_clauses = np.asarray(deleted_clauses)
	added_conflict_literals = np.asarray(added_conflict_literals)
	deleted_literals = np.asarray(deleted_literals)
	num_implication = np.asarray(num_implication)
	runtime = np.asarray(runtime)
	results = np.asarray(results)
	
	zchaff_regular_metrics = np.stack((level,num_decisions,original_num_vars,original_num_clauses,original_num_literals,added_conflict_clauses,num_of_shrinkings,deleted_conflict_clauses,deleted_clauses,added_conflict_literals,deleted_literals,num_implication,runtime,results), axis = 1)
	
	return zchaff_irregular_metrics, zchaff_regular_metrics
	
	'''
	Max Decision Level				38
	Num. of Decisions				40
	( Stack + Vsids + Shrinking Decisions )		0 + 39 + 0
	Original Num Variables				729
	Original Num Clauses				23668
	Original Num Literals				49588
	Added Conflict Clauses				1
	Num of Shrinkings				0
	Deleted Conflict Clauses			0
	Deleted Clauses					0
	Added Conflict Literals				15
	Deleted (Total) Literals			0
	Number of Implication				765
	Total Run Time					0
	RESULT:	SAT
	'''
	
	
def parse_ubcsat():
	
	
	values = []
	
	ubcsat_irregular_metrics = []
	ubcsat_regular_metrics = []
	
	
	with open("all_output_ubcsat_irregular.txt", "r") as f:
		for line in f:
			if("Steps_Mean =" in line):
				values = line.split(" ")
			
				ubcsat_irregular_metrics.append(float(values[2]))
		
	for c in range(1,6):
		with open("all_output_ubcsat_regular_" + str(c) + ".txt", "r") as f:
			for line in f:
				if("Steps_Mean =" in line):
					values = line.split(" ")
			
					ubcsat_regular_metrics.append(float(values[2]))
	
	return ubcsat_irregular_metrics, ubcsat_regular_metrics
		
	'''
	flipspersecond inf?
	Variables = 729
	Clauses = 23660
	TotalLiterals = 49580
	Steps_Mean = 994
	'''
	
def parse_walksat():

	
	values = []
	
	walksat_irregular_metrics = []
	walksat_regular_metrics = []
	
	avg_length_successful_tries = []
	
	avg_flips_per_assign = [] #? total flips
		
	with open("all_output_walksat_irregular.txt", "r") as f:
		for line in f:
			if("average length successful tries = " in line):
				values = line.split(" ")
			
				avg_length_successful_tries.append(float(values[5]))
			elif("average flips per assign (over all runs) = " in line):
				values = line.split(" ")
			
				avg_flips_per_assign.append(float(values[8]))
				
				
	avg_length_successful_tries = np.asarray(avg_length_successful_tries[:15000])
	avg_flips_per_assign = np.asarray(avg_flips_per_assign[:15000])
	
	walksat_irregular_metrics = np.stack((avg_length_successful_tries, avg_flips_per_assign), axis = 1)
	
	
	avg_length_successful_tries = []
	
	avg_flips_per_assign = [] #? total flips
		
	for c in range(1,6):
	
		with open("all_output_walksat_regular_" + str(c) + ".txt", "r") as f:
			for line in f:
				if("average length successful tries = " in line):
					values = line.split(" ")
			
					avg_length_successful_tries.append(float(values[5]))
				elif("average flips per assign (over all runs) = " in line):
					values = line.split(" ")
			
					avg_flips_per_assign.append(float(values[8]))
				
				
	avg_length_successful_tries = np.asarray(avg_length_successful_tries[:15000])
	avg_flips_per_assign = np.asarray(avg_flips_per_assign[:15000])
	
	walksat_regular_metrics = np.stack((avg_length_successful_tries, avg_flips_per_assign), axis = 1)
	
		
	#print(avg_length_successful_tries, avg_flips_per_assign)
	
	return walksat_irregular_metrics, walksat_regular_metrics 
	
	
	'''
	average flips per second = 1475350
	average length successful tries = 2950
	average flips per assign (over all runs) = 2950.700000
	mean flips until assign = 2950.700000
	'''
	
	
pycosat_irregular_metrics, pycosat_regular_metrics = parse_pycosat() #seconds  level   variables  used  original conflicts  learned  limit   agility MB

zchaff_irregular_metrics, zchaff_regular_metrics = parse_zchaff()
#level,num_decisions,original_num_vars,original_num_clauses,original_num_literals,added_conflict_clauses,num_of_shrinkings,deleted_conflict_clauses,deleted_clauses,added_conflict_literals,deleted_literals,num_implication,runtime,results)

ubcsat_irregular_metrics, ubcsat_regular_metrics = parse_ubcsat() #Steps_Mean

walksat_irregular_metrics, walksat_regular_metrics = parse_walksat()	#avg_length_successful_tries, avg_flips_per_assign HANDLE ASSIGNMENT NOT FOUND
#12 assignment not found 10 trials with cutoff

pycosat_irregular_metrics = np.asarray(pycosat_irregular_metrics[:15000]).T
pycosat_regular_metrics = np.asarray(pycosat_regular_metrics[:15000]).T

plt.text(0.5, 0.5, '', ha='center', va='center',
        size=20, alpha=.5)

###

plt.subplot(3, 2, 1)

plt.hist(pycosat_irregular_metrics[6], bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - Pycosat', size = 15)

plt.ylabel('Learned', size = 15)

plt.subplot(3, 2, 2)
plt.hist(pycosat_regular_metrics[6], bins='auto',edgecolor = 'black')

plt.xlabel('Regular - Pycosat', size = 15)


###

plt.subplot(3, 2, 3)

plt.hist(pycosat_irregular_metrics[1], bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - Pycosat', size = 15)

plt.ylabel('Level', size = 15)

plt.subplot(3, 2, 4)
plt.hist(pycosat_regular_metrics[1], bins='auto',edgecolor = 'black')

plt.xlabel('Regular - Pycosat', size = 15)

###

plt.subplot(3, 2, 5)

plt.hist(pycosat_irregular_metrics[1], bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - Pycosat', size = 15)

plt.ylabel('Conflicts', size = 15)

plt.subplot(3, 2, 6)
plt.hist(pycosat_regular_metrics[5], bins='auto',edgecolor = 'black')

plt.xlabel('Regular - Pycosat', size = 15)


plt.tight_layout()

plt.savefig("pycoplot.png")



ubcsat_irregular_metrics = np.asarray(ubcsat_irregular_metrics[:15000])
ubcsat_regular_metrics = np.asarray(ubcsat_regular_metrics[:15000])

plt.text(0.5, 0.5, '', ha='center', va='center',
        size=20, alpha=.5)

###


plt.subplot(1, 2, 1)

plt.hist(ubcsat_irregular_metrics, bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - UBCSAT', size = 15)

plt.ylabel('Steps', size = 15)
plt.subplot(1, 2, 2)

plt.hist(ubcsat_regular_metrics, bins='auto',edgecolor = 'black')

plt.xlabel('Regular - UBCSAT', size = 15)

plt.tight_layout()

plt.savefig("ubcsteps.png")



zchaff_irregular_metrics = np.asarray(zchaff_irregular_metrics[:15000]).T
zchaff_regular_metrics = np.asarray(zchaff_regular_metrics[:15000]).T


plt.text(0.5, 0.5, '', ha='center', va='center',
        size=20, alpha=.5)

###



plt.subplot(2, 2, 1)

plt.hist(zchaff_irregular_metrics[0].astype(float), bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - zchaff', size = 15)

plt.ylabel('Level', size = 15)

plt.subplot(2, 2, 2)
plt.hist(zchaff_regular_metrics[0].astype(float), bins='auto',edgecolor = 'black')

plt.xlabel('Regular - zchaff', size = 15)


###
plt.subplot(2, 2, 3)

plt.hist(zchaff_irregular_metrics[1].astype(int), bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - zchaff', size = 15)

plt.ylabel('Num of decisions', size = 15)

plt.subplot(2, 2, 4)
plt.hist(zchaff_regular_metrics[1].astype(int), bins='auto',edgecolor = 'black')

plt.xlabel('Regular - zchaff', size = 15)

plt.savefig("zchaff.png")


plt.clf()

walksat_irregular_metrics = np.asarray(walksat_irregular_metrics[:15000]).T
walksat_regular_metrics = np.asarray(walksat_regular_metrics[:15000]).T

plt.text(0.5, 0.5, '', ha='center', va='center',
        size=20, alpha=.5)

###

plt.subplot(1, 2, 1)

plt.hist(walksat_irregular_metrics[0], bins='auto',edgecolor = 'black')

plt.xlabel('Irregular - walksat', size = 15)

plt.ylabel('Avg length of successful trials', size = 15)

plt.subplot(1, 2, 2)
plt.hist(walksat_regular_metrics[0], bins='auto',edgecolor = 'black')

plt.xlabel('Regular - walksat', size = 15)


plt.savefig("walksat.png")
	
	
#means

mean_learned_pycosat_irregular = np.mean(pycosat_irregular_metrics[6])
mean_learned_pycosat_regular = np.mean(pycosat_regular_metrics[6])

mean_level_pycosat_irregular = np.mean(pycosat_irregular_metrics[1])
mean_level_pycosat_regular = np.mean(pycosat_regular_metrics[1])

mean_conflicts_pycosat_irregular = np.mean(pycosat_irregular_metrics[5])
mean_conflicts_pycosat_regular = np.mean(pycosat_regular_metrics[5])

mean_steps_irregular = np.mean(ubcsat_irregular_metrics)
mean_steps_regular = np.mean(ubcsat_regular_metrics)

mean_level_zchaff_irregular = np.mean(zchaff_irregular_metrics[0].astype(float))
mean_level_zchaff_regular = np.mean(zchaff_regular_metrics[0].astype(float))

mean_num_decisions_zchaff_irregular = np.mean(zchaff_irregular_metrics[1].astype(float))
mean_num_decisions_zchaff_regular = np.mean(zchaff_regular_metrics[1].astype(float))

mean_avg_length_trials_walksat_irregular = np.mean(walksat_irregular_metrics[0])
mean_avg_length_trials_walksat_regular = np.mean(walksat_regular_metrics[0])


print(mean_learned_pycosat_irregular)
print(mean_learned_pycosat_regular)

print(mean_level_pycosat_irregular)
print(mean_level_pycosat_regular)

print(mean_conflicts_pycosat_irregular)
print(mean_conflicts_pycosat_regular)

print(mean_steps_irregular)
print(mean_steps_regular)

print(mean_level_zchaff_irregular)
print(mean_level_zchaff_regular)

print(mean_num_decisions_zchaff_irregular)
print(mean_num_decisions_zchaff_regular)

print(mean_avg_length_trials_walksat_irregular)
print(mean_avg_length_trials_walksat_regular)


#standard deviations
std_learned_pycosat_irregular = np.std(pycosat_irregular_metrics[6])
std_learned_pycosat_regular = np.std(pycosat_regular_metrics[6])

std_level_pycosat_irregular = np.std(pycosat_irregular_metrics[1])
std_level_pycosat_regular = np.std(pycosat_regular_metrics[1])

std_conflicts_pycosat_irregular = np.std(pycosat_irregular_metrics[5])
std_conflicts_pycosat_regular = np.std(pycosat_regular_metrics[5])

std_steps_irregular = np.std(ubcsat_irregular_metrics)
std_steps_regular = np.std(ubcsat_regular_metrics)

std_level_zchaff_irregular = np.std(zchaff_irregular_metrics[0].astype(float))
std_level_zchaff_regular = np.std(zchaff_regular_metrics[0].astype(float))

std_num_decisions_zchaff_irregular = np.std(zchaff_irregular_metrics[1].astype(float))
std_num_decisions_zchaff_regular = np.std(zchaff_regular_metrics[1].astype(float))

std_avg_length_trials_walksat_irregular = np.std(walksat_irregular_metrics[0])
std_avg_length_trials_walksat_regular = np.std(walksat_regular_metrics[0])

res_file = open("pycosat_irregular_learned.csv", "w")

for e in range(0,15000):
	res_file.write(str(pycosat_irregular_metrics[6][e]) + "\n")
		
res_file = open("pycosat_regular_learned.csv", "w")

for e in range(0,15000):
	res_file.write(str(pycosat_regular_metrics[6][e]) + "\n")

res_file = open("pycosat_irregular_level.csv", "w")

for e in range(0,15000):
	res_file.write(str(pycosat_irregular_metrics[1][e]) + "\n")
		
		
res_file = open("pycosat_regular_level.csv", "w")

for e in range(0,15000):
	res_file.write(str(pycosat_regular_metrics[1][e]) + "\n")
		
res_file = open("pycosat_irregular_conflicts.csv", "w")

for e in range(0,15000):
	res_file.write(str(pycosat_irregular_metrics[5][e]) + "\n")
		
		
res_file = open("pycosat_regular_conflicts.csv", "w")

for e in range(0,15000):
	res_file.write(str(pycosat_regular_metrics[5][e]) + "\n")		
		
		
###


res_file = open("ubcsat_irregular_steps.csv", "w")

for e in range(0,15000):
	res_file.write(str(ubcsat_irregular_metrics[e]) + "\n")
	

res_file = open("ubcsat_regular_steps.csv", "w")

for e in range(0,15000):
	res_file.write(str(ubcsat_regular_metrics[e]) + "\n")
	
###
res_file = open("zchaff_irregular_level.csv", "w")

for e in range(0,15000):
	res_file.write(str(zchaff_irregular_metrics[0][e].astype(float)) + "\n")
		
		
res_file = open("zchaff_regular_level.csv", "w")

for e in range(0,15000):
	res_file.write(str(zchaff_irregular_metrics[0][e].astype(float)) + "\n")
	
	

res_file = open("zchaff_irregular_decisions.csv", "w")

for e in range(0,15000):
	res_file.write(str(zchaff_irregular_metrics[1][e].astype(float)) + "\n")
		
		
res_file = open("zchaff_regular_decisions.csv", "w")

for e in range(0,15000):
	res_file.write(str(zchaff_irregular_metrics[1][e].astype(float)) + "\n")
	
	
###
	
		
res_file = open("walksat_irregular_avglength.csv", "w")

for e in range(0,15000):
	res_file.write(str(walksat_irregular_metrics[0][e]) + "\n")
		
		
res_file = open("walksat_regular_avglength.csv", "w")

for e in range(0,15000):
	res_file.write(str(walksat_regular_metrics[0][e]) + "\n")
	
	
###

print(std_learned_pycosat_irregular)
print(std_learned_pycosat_regular)

print(std_level_pycosat_irregular)
print(std_level_pycosat_regular)

print(std_conflicts_pycosat_irregular)
print(std_conflicts_pycosat_regular)

print(std_steps_irregular)
print(std_steps_regular)

print(std_level_zchaff_irregular)
print(std_level_zchaff_regular)

print(std_num_decisions_zchaff_irregular)
print(std_num_decisions_zchaff_regular)

print(std_avg_length_trials_walksat_irregular)
print(std_avg_length_trials_walksat_regular)




#NORMALITY TESTS KOLMOGOROV SMIRNOV
print(stats.kstest((pycosat_irregular_metrics[6] - np.mean(pycosat_irregular_metrics[6]))/np.std(pycosat_irregular_metrics[6]), cdf = 'norm', N=15000))

print(stats.kstest((pycosat_regular_metrics[6] - np.mean(pycosat_regular_metrics[6]))/np.std(pycosat_regular_metrics[6]), cdf = 'norm', N=15000))


print(stats.kstest((pycosat_irregular_metrics[1] - np.mean(pycosat_irregular_metrics[1]))/np.std(pycosat_irregular_metrics[1]), cdf = 'norm', N=15000))

print(stats.kstest((pycosat_regular_metrics[1] - np.mean(pycosat_regular_metrics[1]))/np.std(pycosat_regular_metrics[1]), cdf = 'norm', N=15000))


print(stats.kstest((pycosat_irregular_metrics[5] - np.mean(pycosat_irregular_metrics[5]))/np.std(pycosat_irregular_metrics[5]), cdf = 'norm', N=15000))

print(stats.kstest((pycosat_regular_metrics[5] - np.mean(pycosat_regular_metrics[5]))/np.std(pycosat_regular_metrics[5]), cdf = 'norm', N=15000))




print(stats.kstest((ubcsat_irregular_metrics - np.mean(ubcsat_irregular_metrics))/np.std(ubcsat_irregular_metrics), cdf = 'norm', N=15000))

print(stats.kstest((ubcsat_regular_metrics - np.mean(ubcsat_regular_metrics))/np.std(ubcsat_regular_metrics), cdf = 'norm', N=15000))



print(stats.kstest((zchaff_irregular_metrics[0].astype(float) - np.mean(zchaff_irregular_metrics[0].astype(float)))/np.std(zchaff_irregular_metrics[0].astype(float)), cdf = 'norm', N=15000))

print(stats.kstest((zchaff_regular_metrics[0].astype(float) - np.mean(zchaff_regular_metrics[0].astype(float)))/np.std(zchaff_regular_metrics[0].astype(float)), cdf = 'norm', N=15000))


print(stats.kstest((zchaff_irregular_metrics[1].astype(float) - np.mean(zchaff_irregular_metrics[1].astype(float)))/np.std(zchaff_irregular_metrics[1].astype(float)), cdf = 'norm', N=15000))

print(stats.kstest((zchaff_regular_metrics[1].astype(float) - np.mean(zchaff_regular_metrics[1].astype(float)))/np.std(zchaff_regular_metrics[1].astype(float)), cdf = 'norm', N=15000))


print(stats.kstest((walksat_irregular_metrics[0] - np.mean(walksat_irregular_metrics[0]))/np.std(walksat_irregular_metrics[0]), cdf = 'norm', N=15000))

print(stats.kstest((walksat_regular_metrics[0] - np.mean(walksat_regular_metrics[0]))/np.std(walksat_regular_metrics[0]), cdf = 'norm', N=15000))


#levene test for variance
#independent ttest to compare group means
print(stats.levene(pycosat_irregular_metrics[6],pycosat_regular_metrics[6]))
print(stats.ttest_ind(pycosat_irregular_metrics[6],pycosat_regular_metrics[6]))


print(stats.levene(pycosat_irregular_metrics[1],pycosat_regular_metrics[1]))
print(stats.ttest_ind(pycosat_irregular_metrics[1],pycosat_regular_metrics[1]))


print(stats.levene(pycosat_irregular_metrics[5],pycosat_regular_metrics[5]))
print(stats.ttest_ind(pycosat_irregular_metrics[5],pycosat_regular_metrics[5]))


print(stats.levene(ubcsat_irregular_metrics, ubcsat_regular_metrics))
print(stats.ttest_ind(ubcsat_irregular_metrics, ubcsat_regular_metrics))

print(stats.levene(zchaff_irregular_metrics[0].astype(float),zchaff_regular_metrics[0].astype(float)))
print(stats.ttest_ind(zchaff_irregular_metrics[0].astype(float),zchaff_regular_metrics[0].astype(float)))

print(stats.levene(zchaff_irregular_metrics[1].astype(float),zchaff_regular_metrics[1].astype(float)))
print(stats.ttest_ind(zchaff_irregular_metrics[1].astype(float),zchaff_regular_metrics[1].astype(float)))


print(stats.levene(walksat_irregular_metrics[0],walksat_regular_metrics[0]))
print(stats.ttest_ind(walksat_irregular_metrics[0],walksat_regular_metrics[0]))


'''
KstestResult(statistic=0.075965363447865725, pvalue=1.3033473530971269e-75)
KstestResult(statistic=0.14080118553292936, pvalue=1.0109452140129837e-258)
KstestResult(statistic=0.028766609968171708, pvalue=3.3070208264513844e-11)
KstestResult(statistic=0.02709673518868988, pvalue=5.4303651253397432e-10)
KstestResult(statistic=0.21077063612258454, pvalue=0.0)
KstestResult(statistic=0.29393692411451966, pvalue=0.0)
KstestResult(statistic=0.30613108363496166, pvalue=0.0)
KstestResult(statistic=0.18572647870782211, pvalue=0.0)
KstestResult(statistic=0.13331680537362667, pvalue=5.4290865898289205e-232)
KstestResult(statistic=0.034522107831503557, pvalue=5.9371593469280756e-16)
KstestResult(statistic=0.24950250200731455, pvalue=0.0)
KstestResult(statistic=0.025929018595601372, pvalue=3.4798627646907861e-09)
KstestResult(statistic=0.13197117557451604, pvalue=2.4308179717900551e-227)
KstestResult(statistic=0.1576422818097355, pvalue=0.0)
LeveneResult(statistic=7790.6504425037328, pvalue=0.0)
Ttest_indResult(statistic=-121.11490529709558, pvalue=0.0)
LeveneResult(statistic=405.71768334152733, pvalue=1.2292949884571001e-89)
Ttest_indResult(statistic=88.334791764162148, pvalue=0.0)
LeveneResult(statistic=2996.3097640950286, pvalue=0.0)
Ttest_indResult(statistic=79.054483213678623, pvalue=0.0)
LeveneResult(statistic=1208.6513473176894, pvalue=1.156480604059433e-259)
Ttest_indResult(statistic=42.735426211486867, pvalue=0.0)
LeveneResult(statistic=197.00028386016092, pvalue=1.3053634714879245e-44)
Ttest_indResult(statistic=92.298180421448677, pvalue=0.0)
LeveneResult(statistic=2294.6203731955447, pvalue=0.0)
Ttest_indResult(statistic=69.925388753460027, pvalue=0.0)
LeveneResult(statistic=3917.2223488272525, pvalue=0.0)
Ttest_indResult(statistic=95.901447628819056, pvalue=0.0)
'''

