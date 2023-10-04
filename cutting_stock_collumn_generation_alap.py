
from ortools.linear_solver import pywraplp


pattern_lot = []
pattern = ""
data = [[4, 6, 7], [80, 50, 100], [15]]
ssMvu = data[0]

print(f"Data: {data}")

def Organiser(data):
    
    pattern = SubProblem(data)
    for i in range(len(pattern)-1):
        if(pattern):
            for e in range(len(pattern)-1):
                ssMvu[pattern.index(max(pattern))] = 0
        pattern = SubProblem(data)
        
                

        

    
    

    print("\n")
    # print([sum(values) for values in zip(*pattern_lot)])
    # if(sum(pattern_lot))

    solution = MasterProblem(data, pattern_lot)
    
    return pattern_lot



def SubProblem(data):
    sub_solver = pywraplp.Solver.CreateSolver("CBC_MIXED_INTEGER_PROGRAMMING")

    if not sub_solver:
        return None
    
    variable_values = data[0]
    RHS = data[2]
    
    
    infinity = sub_solver.infinity()
    x1 = sub_solver.IntVar(0, infinity, "x1")
    x2 = sub_solver.IntVar(0, infinity, "x2")
    x3 = sub_solver.IntVar(0, infinity, "x3")

    sub_solver.Maximize(ssMvu[0] * x1 + ssMvu[1] * x2 + ssMvu[2] * x3)
    c1 = sub_solver.Add(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3 <= RHS[0])

    def ExportLpModel(sub_solver, SUBP):
        lp_model2 = sub_solver.ExportModelAsLpFormat(False)
        with open(SUBP, 'w') as file:
            file.write(lp_model2)

    ExportLpModel(sub_solver, "SUBP.lp")

    pattern = SubProblemSolver(sub_solver, [x1, x2, x3], [c1], True)

    
    
    pattern_lot.append(pattern)
    # print(pattern)

    
    return pattern


def SubProblemSolver(sub_solver, variable_list, constraint_list, is_precise):
    result_status = sub_solver.Solve()

    if(result_status != pywraplp.Solver.OPTIMAL):
        print("SsubOtimal")

    if is_precise:
        assert sub_solver.VerifySolution(1e-7, True)

    result = []
    for variable in variable_list:
        result.append(variable.solution_value())
    return result


def MasterProblem(data, pattern_lot):
    master_solver = pywraplp.Solver.CreateSolver("CBC_MIXED_INTEGER_PROGRAMMING")
    if not master_solver:
        return None
    
    RHSF = data[1]
    num_patterns = len(pattern_lot)
    
    # Create variables for each pattern and each item in the pattern
    variables = []
    for i in range(num_patterns):
        pattern = pattern_lot[i]
        pattern_vars = []
        var = master_solver.IntVar(0, master_solver.infinity(), f"x_{i}")
        variables.append(var)
    # print(variables)
    # print(pattern_lot)
    

    
    master_solver.Minimize(sum(variables[i] * pattern_lot[i][j] for i in range(num_patterns) for j in range(len(pattern_lot[i]))))
    
    
    # Add constraints for each RHSF value
    for i in range(len(RHSF)):
        # print(variables[i])
        # print(pattern_lot[i])
        # print(variables)
        constraint = master_solver.Add(sum(variables[j] * pattern_lot[j][i] for j in range(len(pattern))) >= RHSF[i])

    def ExportLpModel(master_solver, MSTR):
        lp_model = master_solver.ExportModelAsLpFormat(False)
        with open(MSTR, 'w') as file:
            file.write(lp_model)

    ExportLpModel(master_solver, "MSTR.lp")

    result_status = master_solver.Solve()

    if result_status != pywraplp.Solver.OPTIMAL:
        print("Master Problem is not optimal")

    # if is_precise:
    #     assert master_solver.VerifySolution(1e-7, True)

    finalresult = []
    
    finalresult.extend([var.solution_value() for var in variables])

    numUsedRods = sum(finalresult)
    # print(f"--------------Variable values :    {finalresult}")
    print(f"Megkezdett rudak :                 {numUsedRods}")
    print(f"Mennyiségek :                      {finalresult}")
    print(f"Minták :                           {pattern_lot}")

    return finalresult
  


if __name__ == '__main__':
    
    subresult = Organiser(data)
    




    
