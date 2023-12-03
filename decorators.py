import time

def repeat_every(seconds):
    def decorator(task_func):
        def wrapper():
            while True:
                task_func()
                time.sleep(seconds)
        return wrapper
    return decorator