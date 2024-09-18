# @singleton
# Make a class a singleton. Only one instance of the class will be created and returned.

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


# @private
# Make a class private and raise an exception if it is accessed from outside the module.

def private(cls):
    def wrapper(*args, **kwargs):
        raise Exception("This class is private and cannot be accessed from outside the module!")
    return wrapper

# @static
# Make a class static and raise an exception if it is instantiated. (EXPERIMENTAL)

def static(cls):
    def wrapper(*args, **kwargs):
        raise Exception("This class is static and cannot be instantiated!")
    return wrapper

# @threaded
# Make a class threaded and return a thread object. (EXPERIMENTAL)

def threaded(cls):
    import threading

    def wrapper(*args, **kwargs):
        return threading.Thread(target=cls, args=args, kwargs=kwargs)
    return wrapper

# @trycatch
# Make a piece of code try-catchable without using try-catch blocks.
def trycatch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
    return wrapper

# @loop(condition)
# Make a function loop until a condition is met. (EXPERIMENTAL)
def loop(condition_func):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while condition_func():
                func(*args, **kwargs)
        return wrapper
    return decorator

# @deprecated
# Mark a function as deprecated and print a log when its used for the first time, also raise a warning and show in the editor as a warning.
def deprecated(func):
    import warnings

    def wrapper(*args, **kwargs):
        warnings.warn(f"Function {func.__name__} is deprecated and will be removed in the future.", DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper

# @experimental
# Mark a function as experimental and print a log when its used for the first time, also raise a warning and show in the editor as a warning.
def experimental(func):
    import warnings

    def wrapper(*args, **kwargs):
        warnings.warn(f"Function {func.__name__} is experimental and may not work as expected.", UserWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper

# @notnull
# Make a function not return None, undefined or null.
def notnull(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise Exception("Function returned None!")
        return result
    return wrapper

# @delay(seconds)
# Delay a function by a number of seconds.
def delay(seconds):
    import time

    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# @timeout(seconds)
# Timeout a function after a number of seconds.
class TimeoutException(Exception):
    pass

def timeout(seconds):
    from threading import Thread
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = [TimeoutException('Function timed out!')]
            def target():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=target)
            t.start()
            t.join(seconds)
            if isinstance(res[0], BaseException):
                raise res[0]
            return res[0]
        return wrapper
    return decorator

# @retry(attempts/-1, delay)
# Retry a function a number of times with a delay between each attempt.
def retry(attempts, delay):
    import time
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i} failed: {e}")
                    time.sleep(delay)
            raise Exception("Function failed after all attempts!")
        return wrapper
    return decorator

# @log
# Log a function's arguments and return value.
def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} called with args: {args} and kwargs: {kwargs}, returned: {result}")
        return result
    return wrapper

# @benchmark
# Benchmark a function and print the time it took to execute.
def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start} seconds to execute.")
        return result
    return wrapper

# @ignore
# Ignore a function and do nothing.
def ignore(func):
    def wrapper(*args, **kwargs):
        pass
    return wrapper

# @abstract
# Make a function abstract and raise an exception if it is not implemented in a subclass.
def abstract(func):
    def wrapper(*args, **kwargs):
        raise Exception(f"Function {func.__name__} is abstract and must be implemented in a subclass!")
    return wrapper

# @accepts(*types)
# Check if a function's arguments are of the specified types.
def accepts(*types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i, arg in enumerate(args):
                if not isinstance(arg, types[i]):
                    raise TypeError(f"Argument {i} must be of type {types[i].__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# @returns(type)
# Check if a function's return value is of the specified type.
def returns(type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, type):
                raise TypeError(f"Return value must be of type {type.__name__}")
            return result
        return wrapper
    return decorator

# @webhook(url)
# Send a webhook to a URL with the function's arguments and return value.
def webhook(url):
    import requests
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = {
                "args": args,
                "kwargs": kwargs,
                "result": func(*args, **kwargs)
            }
            requests.post(url, json=data)
        return wrapper
    return decorator

# @yieldable
# Make a function yieldable and return a generator.

def yieldable(func):
    def wrapper(*args, **kwargs):
        def generator():
            yield func(*args, **kwargs)
        return generator()
    return wrapper