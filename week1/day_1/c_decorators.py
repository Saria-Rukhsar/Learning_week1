import time
from functools import wraps

def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()        
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"[TIMING] '{func.__name__}' took {duration:.4f} seconds to execute.")
        return result
    return wrapper

def log_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            print(f"[LOG] '{func.__name__}' completed successfully. Returned: {result}")
            return result
        except Exception as e:
            print(f"[LOG] '{func.__name__}' FAILED. Error: {e}")
            raise e            
    return wrapper

@time_it
@log_transaction
def process_payment(username, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return f"Charged ${amount} to {username}"

process_payment("alice_dev", 150)
