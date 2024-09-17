import time

def execute(func, *args, **kwargs):
    start_time = time.time()

    print(f"Executing: {func.__name__}")
    result = func(*args, **kwargs)  

    end_time = time.time()

    print(f"Time Spent: {(end_time - start_time):2.5f}")
    return result