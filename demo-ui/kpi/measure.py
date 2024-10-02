import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error

col = "humidity"

gt = pd.read_csv("DailyDelhiClimateTrain.csv")

nulls = pd.read_csv("DailyDelhiClimateTrain_with_nulls.csv")

# alg1res = nulls[col].interpolate("pad")

# alg2res = nulls[col].interpolate("linear")

# accuracy1 = accuracy_score()

# accuracy2 = accuracy_score()

mae1 = mean_absolute_error(gt[col], nulls[col].interpolate("linear"))
mae2 = mean_absolute_error(gt[col], nulls[col].interpolate("pad"))

print("Linear: ", mae1)

print("Pad: ", mae2)


import time

def measure_execution_time(func, *args, **kwargs):
    """
    Measures the execution time of a given function with arguments.

    Args:
        func (callable): The function to measure.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        float: Elapsed time in seconds.
    """
    start_time = time.time()
    for _ in range(1000):
        func(*args, **kwargs)  # Call the function with provided arguments
    end_time = time.time()

    elapsed_time = end_time - start_time
    return elapsed_time

execution_time_linear = 0
execution_time_pad = 0

num_of_rep = 100
for _ in range(num_of_rep):

    # Call the function with arguments
    execution_time_linear = measure_execution_time(nulls[col].interpolate, "linear")
    execution_time_pad = measure_execution_time(nulls[col].interpolate, "pad")

execution_time_linear = execution_time_linear/num_of_rep
execution_time_pad = execution_time_pad/num_of_rep

print(f"Execution time linear: {execution_time_linear:.6f} seconds")
print(f"Execution time pad: {execution_time_pad:.6f} seconds")


