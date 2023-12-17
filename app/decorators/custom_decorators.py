from functools import wraps
import asyncio

def repeat_every(seconds):
    def decorator(task_func):
        @wraps(task_func)
        async def wrapper(*args, **kwargs):
            try:
                while True:
                    await task_func(*args, **kwargs)
                    await asyncio.sleep(seconds)
            except asyncio.CancelledError:
                pass  # Catch CancelledError to exit the loop gracefully on cancellation
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Exiting the loop gracefully.")
        return wrapper
    return decorator