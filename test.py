import random as rand

def gen_random_float(n):
    res = []
    for _ in range(n):
        res.append(rand.random())
    arr = [(x / sum(res)) ** 2 for x in res]
    return sum(arr)

def resampling_and_get_distr(k):
    """
    call gen_random_float for k times and get distribution
    """
    res = []
    for _ in range(k):
        res.append(gen_random_float(10))
    return res 

def construct_optimization_problem():
    status = True
    gr_form = gurobi.formuation()
    if not construct_variables(gr_form):
        status = False
    if not construct_obj_functions():
        status = False
    if not construct_contraints():
        status = False
    gr_form.optimize()
    return status

def construct_variables(gr_form):
    for i _ in range(10):
        gr_form.add_variables(f"x_{i}")
    gr_form.add_variables(f"zz")
    return True
        
def construct_obj_functions(gr_form):
    gr_form.addobjective(expression="z", sense = 'Minimize')

def construct_contraints(gr_form):
    lhs1: gurobi.expression = 0
    for i in range(N):
        lhs1 += gurobi.getVar(f"x_{i}")
        lhs2 += gurobi.getVar(f"x_{i}") ** 2

    gr_form.add_constraints(lhr=lhs1,rhs= 1, sense="equal")
    gr_form.add_constraints(lhs=lhs2,rhs=z )




if __name__ == '__main__':
    from matplotlib import pyplot
    test_arr = resampling_and_get_distr(1000)
    print(test_arr)
    print(min(test_arr))
    pyplot.hist(test_arr)

