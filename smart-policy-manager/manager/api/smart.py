
from .config import algos_dataset, cat_metrics_dataset,categories
import pandas as pd
from ortools.linear_solver import pywraplp
import json

def get_category_from_metric_name(metric = "Mae"):
    df = pd.read_csv(cat_metrics_dataset, index_col="Metric", sep=";")
    df = df[categories]
    
    for category in categories:
        if df.loc[metric][category] == 1:
            return category

def get_available_algos_based_on_task(task="Time series interpolation"):
    
    df = pd.read_csv(algos_dataset, index_col="Id", sep=";")
    df["Task"] = df["Task"].ffill() # padding

    df = df[df["Task"]==task]
    return list(df["Name"])

def get_all_metrics_of_an_algo(algorithm="ts_linear_interpolation"):
    df = pd.read_csv(algos_dataset, index_col="Id", sep=";")
    df["Task"] = df["Task"].ffill() # padding
    df = df[df["Name"]==algorithm]
    df = df.dropna(axis=1)
    df = df.drop("Task", axis=1)
    df = df.drop("Name", axis=1)
    df = df.drop("Dataset", axis=1)
    return list(df.columns)

def get_metric_of_algo(metric="Mae", algorithm="ts_linear_interpolation"):
    df = pd.read_csv(algos_dataset, index_col="Id", sep=";")
    df = df[df["Name"]==algorithm]
    # df["Task"] = df["Task"].fillna(method='ffill') # padding

    # TODO make it better
    df2 = pd.read_csv(cat_metrics_dataset, index_col="Metric", sep=";")
    if df2.loc[metric]["Objective"] =="Min":
        return 1/df.iloc[0][metric]
    else:
        return df.iloc[0][metric]


def get_execution_config(algo):
    with open('/api/running_config/' + algo + ".json") as f:
        return json.load(f)

def LinearProgrammingExample(algos, parameters):
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    variables = []
    for algo in algos:
        variables.append(solver.NumVar(0, 1, "algo"))
    
        
    normalization_coeffs = {}
        
    algos_metrics = {}
    for algo in algos:
        metrics = get_all_metrics_of_an_algo(algorithm=algo)
        for metric in metrics:
            if algos_metrics.get(algo) is None:
                algos_metrics[algo] = {}
            algos_metrics[algo][metric] = get_metric_of_algo(metric=metric, algorithm=algo)
            if normalization_coeffs.get(metric) is None or normalization_coeffs[metric] < algos_metrics[algo][metric]:
                normalization_coeffs[metric] = algos_metrics[algo][metric]

    # Normalize values
    for algo in algos:
        metrics = get_all_metrics_of_an_algo(algorithm=algo)
        for metric in metrics:
            algos_metrics[algo][metric] = algos_metrics[algo][metric]/normalization_coeffs[metric]

    
    print("Number of variables =", solver.NumVariables())

    solver.Add(sum(variables) == 1)

    print("Number of constraints =", solver.NumConstraints())
    
    # Calc coefficients
    coefficients = []
    for algo in algos:
        metrics = get_all_metrics_of_an_algo(algorithm=algo)
        coeff = 0
        for metric in metrics:
            coeff += algos_metrics[algo][metric] * parameters[get_category_from_metric_name(metric)]
        coefficients.append(coeff)
        
    # print(coefficients)
    # Objective function: 3x + 4y.
    #solver.Maximize( variables[0] * (parameters['Quality']*((1/0.021)/(1/0.021)) + parameters['Speed of execution']*(1/0.001240)/(1/0.001240)) + variables[1] * (parameters['Quality']*((1/0.028)/(1/0.021)) + parameters['Speed of execution']*(1/0.000410)/(1/0.001240)))

    equation = []
    for i in range(0, len(variables)):
        equation.append(coefficients[i] * variables[i])

    solver.Maximize(sum(equation)) # 12x + 2y etc

    # Solve the system.
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    chosen_algorithm = None
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        index = 0
        for algo in algos:
            print(f"{algo} = {variables[index].solution_value():0.1f}")
            if variables[index].solution_value()==1:
                chosen_algorithm = algo
            index+=1
    else:
        print("The problem does not have an optimal solution.")
        
    # print("\nAdvanced usage:")
    # print(f"Problem solved in {solver.wall_time():d} milliseconds")
    # print(f"Problem solved in {solver.iterations():d} iterations")
    return chosen_algorithm



# # From request comes:
# payload = {
#     "task": "Time series interpolation",
#     "parameters": {
#         "Quality": 100,
#         "Speed of execution": 1,
#         "Energy efficiency": 0,
#         "Cost reduction": 0
#     }
# }


# algos = get_available_algos_based_on_task(payload["task"])

# LinearProgrammingExample(algos=algos, parameters=payload['parameters'])
