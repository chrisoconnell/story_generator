import time
from functools import wraps

def retry_on_parse_error(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ValueError, AttributeError, IndexError, Exception) as e:
                    retries += 1
                    if retries == max_retries:
                        print(f"Failed after {max_retries} attempts due to invalid response: {e}")
                        return None, None

                    print(f"Attempt {retries} failed with error: {e}. Retrying...")
                    time.sleep(delay)

            return None, None
        return wrapper
    return decorator

def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            return ''
    return wrapper

def catch_refusal(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) is str:
            return result

        if result.refusal:
            print(f"Refusal: {result.refusal}")
            return ''
        return result.content
    return wrapper

# Display how long a function took to execute
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        # Convert to hours, minutes, seconds
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = round(duration % 60)

        time_str = ""
        if hours > 0:
            time_str += f"{hours} hour{'s' if hours != 1 else ''} "
        if minutes > 0:
            time_str += f"{minutes} minute{'s' if minutes != 1 else ''} "
        time_str += f"{seconds} second{'s' if seconds != 1 else ''}"

        print(f"function took {time_str}")
        return result
    return wrapper
