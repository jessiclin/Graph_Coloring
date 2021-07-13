import sys 
import random 
import copy

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
Returns True if the current assignments don't violate any of the constraints 
'''
def is_valid(assignment, csp, var, value): 
    # For each neighbor of var 
    for neighbor in csp[var]: 
        # Check that the value is not the same 
        if neighbor in assignment and value == assignment[neighbor]: 
            return False 
            
    return True 
    
##### Plain DFS-B #####
'''
Selects a random variables that has not been assigned a value yet 
'''
def select_unassigned_variable(assignment, csp): 
    unassigned = [] 
    
    # Get list of all unassigned variables 
    for var in csp: 
        if var not in assignment: 
            unassigned.append(var) 
    
    return unassigned[random.randrange(len(unassigned))]

'''
Performs Plain DFS-B 
'''    
def dfsb_plain(assignment, csp): 
    global num_states 
    global domain 
    
    if is_solution(assignment, csp): 
        return assignment 
    
    var = select_unassigned_variable(assignment, csp) 
    
    # Attempt to find solution for each value in the domain 
    for value in domain[var]: 
        # Continue if value is valid 
        if is_valid(assignment, csp, var, value): 
            assignment[var] = value 
            num_states += 1 
            
            result = dfsb_plain(assignment, csp) 
            
            if result is not None: 
                return result 
                
            del assignment[var] 
        
    return None 
    

##### DFS-B++#####
'''
Perform arc consistency algorithm 
'''
def ac_3(csp, variable):
    queue = [] 
    
    # Add arcs for the variable that was just assigned a value 
    for n in csp[variable]: 
        queue.append([n,variable])
        queue.append([variable,n])
    # for key, value in csp.items(): 
        # for v in value: 
            # queue.append([key, v])
    while len(queue) > 0: 
        x_i, x_j = queue.pop(0) 
        
        if remove_inconsistent_values(x_i, x_j): 
            for x_k in csp[x_i]: 
                queue.append([x_k,x_i])
   
'''
Remove any inconsistent values 
'''
def remove_inconsistent_values(x_i, x_j): 
    global domain 
    removed = False 
    
    for value in domain[x_i]: 
        # If x_j only has one value in the domain and it's the same as value, then not valid 
        if len(domain[x_j]) == 1 and domain[x_j][0] == value: 
            domain[x_i].remove(value)
            removed = True 

    return removed 

'''
Return the most constrained unassigned variable 
'''    
def most_constrained_variable(assignment, csp): 
    most_constrained_variable = None 
    min_value = float('inf')
    
    for variable in csp: 
        # If variable is not yet assigned, and the amount in domain is less than current minimum, update 
        if variable not in assignment and len(domain[variable]) < min_value:
            min_value = len(domain[variable]) 
            most_constrained_variable = variable 
            
    return most_constrained_variable 

'''
Output domain of variable in order of lest contrainted values 
'''    
def least_constrained_values_order(variable, assignment, csp): 
    global domain 
    count = {} 
    
    # Add domain[variable] values into dictionary 
    for value in domain[variable]: 
        count[value] = 0 
    
    # Count the number of times each value appears 
    for v in csp[variable]: 
        for value in domain[v]: 
            if value in count: 
                count[value] += 1 
                
    # Sort based on values, and return list of the keys              
    return dict(sorted(count.items(), key=lambda item: item[1])).keys()   

''' 
DFSB++ algorithm 
'''
def dfsb_improved(assignment, csp): 
    global domain 
    global num_states
    
    if is_solution(assignment, csp): 
        return assignment
        
    variable = most_constrained_variable(assignment, csp) 
    values = least_constrained_values_order(variable, assignment, csp) 
    domain_cpy = copy.deepcopy(domain) 
    
    # Attempt to find solution for each value 
    for value in values: 
        # Continue if value is valid 
        if is_valid(assignment, csp, variable, value):
            assignment[variable] = value 
            domain[variable] = [value] 
            
            ac_3(csp, variable) # Prune 
            num_states += 1
            
            result = dfsb_improved(assignment, csp) 
            if result is not None: 
                return result 
        domain = domain_cpy
        
    return None 
    
##### Main Function #####
domain = dict() 

'''
Read in the data from input file  
'''
def readData(input_file): 
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
def multiple_test(input_file, output_file, mode_flag): 
    global num_states
    import os 
    import time 
    #import numpy as np 

    # Keep track of all the times and states
    all_times = [] 
    all_states = [] 

    N, M, K, csp = readData(input_file) 
    start = time.time() 
    if mode_flag == 0: 
        result = dfsb_plain(dict(), csp)
    else: 
        result = dfsb_improved(dict(), csp)
    end = time.time() 

    all_states.append(num_states) 
    all_times.append(end-start) 
    num_states = 0 
    
    for i in range(19): 
        # Generate a new problem with same N, M, and K 
        string = 'python CSPGenerator.py ' + str(N) + ' ' + str(M) + ' ' + str(K) + ' ' + input_file
        os.system(string)
        N, M, K, csp = readData(input_file) 
        
        start = time.time() 
        if mode_flag == 0: 
            dfsb_plain(dict(), csp)
        else: 
            dfsb_improved(dict(), csp) 
        end = time.time() 
        
        all_states.append(num_states) 
        all_times.append(end-start) 
        num_states = 0
        
    # steps_np = np.array(all_states) 
    # time_np = np.array(all_times) 
  
    # print("Average steps: ", np.mean(steps_np))
    # print("Average time: ", np.mean(time_np))
    # print("St. Dev. steps: ", np.std(steps_np))
    # print("St. Dev. time: ", np.std(time_np))
    
if __name__ == "__main__": 
    args = sys.argv 
    if len(args) != 4: 
        print("Invalid number args") 
        exit() 
        
    input_file = args[1] 
    output_file = args[2] 
    mode_flag = int(args[3])

    if mode_flag != 0 and mode_flag != 1: 
        print("Invalid Mode") 
        exit() 

    N, M, K, csp = readData(input_file) 

    if mode_flag == 0: 
        result = dfsb_plain(dict(), csp) 
        outputData(output_file, result)
        #multiple_test(input_file, output_file, mode_flag)
    else: 
        result = dfsb_improved(dict(), csp) 
        outputData(output_file, result)
        #multiple_test(input_file, output_file, mode_flag)

