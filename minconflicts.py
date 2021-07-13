import sys 
import random 

'''
Return true if assignment is a solution 
'''        
def is_solution(assignment, csp): 
    if len(assignment) != len(csp): 
        return False 
        
    # For each variable     
    for var, neighbors in csp.items(): 
        # Check that none of the neighbors have the same value 
        for neighbor in neighbors: 
            if assignment[var] == assignment[neighbor]:                 
                return False 
                
    return True 
''' 
Returns all the variables tht currently violate the constraints 
'''    
def conflicted(assignment, csp): 
    conflict_variables = [] 
    
    for var in csp: 
        # Add variable to conflict_variables if there's a neighbor with the same  value 
        if var in assignment and conflicts(var, assignment[var], assignment, csp) > 0: 
            conflict_variables.append(var) 
     
    return conflict_variables
    
'''
Randomly chooses a variable from the set of conflicted variables  
'''
def random_variable(variables, csp, assignment): 
    # If there's no conflicting variables, then choose a random variable from the list of unassigned variables 
    if len(variables) == 0: 
        vars = [] 
        for var in csp: 
            if var not in assignment: 
                vars.append(var)
        return vars[random.randrange(len(vars))]
        
    return variables[random.randrange(len(variables))]

'''
Counts the number of conflicts when the variable is assigned value v  
'''
def conflicts(var, v, assignment, csp):
    conflict = 0 
    for neighbor in csp[var]: 
        # Conflict if the neighbor has the same value 
        if neighbor in assignment and assignment[neighbor] == v: 
            conflict += 1 
    return conflict    

'''
Selects a value for variable var that results in the minimum number of conflicts  
'''
def min_conflict_value(var, assignment, csp): 
    global domain 
    values = {} 
    
    # For each value, get how many conflicting variables there will be 
    for v in domain[var]: 
        values[v] = conflicts(var, v, assignment, csp) 
    
    # Sort dictionary by values 
    values = dict(sorted(values.items(), key=lambda item: item[1]))
 
    return list(values)[0]

'''
Performs MinConflicts
'''      
def min_conflicts(csp, max_steps, assignment):
    global num_states
    
    for i in range(max_steps): 
        if is_solution(assignment, csp): 
            return assignment
        
        # Get list of conflicting variables and choose a random one 
        conflict_variables = conflicted(assignment, csp) 
        var = random_variable(conflict_variables, csp, assignment) 
        
        # Choose the value that is the least conflicting 
        value = min_conflict_value(var, assignment, csp) 
        assignment[var] = value
        num_states += 1 

    return None 

'''
Read in the data from input file  
'''
domain = dict() 
num_states = 0   
def readData(inpu_file): 
    with open(input_file, 'r') as f: 
        line = f.readline().split()
        N = int(line[0])
        M = int(line[1])
        K = int(line[2]) 
        
        csp = dict() 
        
        for i in range(N): 
            csp[i] = []
            domain[i] = [i for i in range(K)]

        lines = f.read() 
  
        for line in lines.split('\n'): 
            line = line.split()
            if len(line) == 2: 
                one = int(line[0]) 
                two = int(line[1]) 
                csp[one].append(two) 
                csp[two].append(one)
             
    return N, M, K, csp 

'''
Write result to output file 
'''
def outputData(output_file, result): 
    with open(output_file, 'w') as f: 
        if result is None: 
            f.write("No answer") 
        else: 
            keys = sorted(result) 
                
            for k in keys: 
                f.write(str(result[k]) + '\n')    
                
                
'''
Run program 20 times  
'''
num_states = 0 
def multiple_test(input_file, output_file): 
    global num_states
    import os 
    import time 
    # import numpy as np 

    # Keep track of all the times and states
    all_times = [] 
    all_states = [] 

    N, M, K, csp = readData(input_file) 
    start = time.time() 
    
    for i in range(500): 
        result = min_conflicts(csp, N*5, {})
        if result is not None:
            end = time.time() 
            all_states.append(num_states) 
            all_times.append(end-start) 
        
            num_states = 0
            break 
    
    for i in range(19): 
        # Generate a new problem with same N, M, and K 
        string = 'python CSPGenerator.py ' + str(N) + ' ' + str(M) + ' ' + str(K) + ' ' + input_file
        os.system(string)
        N, M, K, csp = readData(input_file) 
        
        start = time.time() 
        for i in range(500): 
            result = min_conflicts(csp, N*5, {})
            if result is not None:
                
                end = time.time() 
                print(result)
                print(is_solution(result, csp))
                all_states.append(num_states) 
                all_times.append(end-start) 
            
                num_states = 0
                break 
    # steps_np = np.array(all_states) 
    # time_np = np.array(all_times) 
  
    # print("Average steps: ", np.mean(steps_np))
    # print("Average time: ", np.mean(time_np))
    # print("St. Dev. steps: ", np.std(steps_np))
    # print("St. Dev. time: ", np.std(time_np))
    
if __name__ == "__main__":
    args = sys.argv 
    
    if len(args) != 3: 
        print("Invalid number args") 
        exit() 
        
    input_file = args[1] 
    output_file = args[2] 

    N, M, K, csp = readData(input_file) 
    
    for i in range(500):
        result = min_conflicts(csp, N * 5, {})
        if result is not None:
            break 
        
    outputData(output_file, result)
    multiple_test(input_file, output_file)
