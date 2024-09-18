# decoutilities

A simple python package that allows using decorators for multiple things like easily setting up a singleton or a configuration file for your app.

## Installation

You can install `decoutilities` using pip:

```bash
pip install decoutilities
```

## Usage

### @singleton

The `@singleton` decorator transforms any class into a singleton, ensuring only one instance of the class is created.

```python
from decoutilities import singleton

@singleton
class MyClass:
    pass

instance1 = MyClass()
instance2 = MyClass()

print(instance1 is instance2)  # Output: True
```

### @private

The `@private` decorator transforms any class into a private class, making it inaccessible from outside the module.

```python
from decoutilities import private

@private
class MyPrivateClass:
    pass

# Trying to access MyPrivateClass from outside the module will raise an error
```

### @static

The `@static` decorator transforms any class into a static class, raising an exception if an attempt is made to instantiate it. This feature is experimental and might fail, please report any errors.

```python
from decoutilities import static

@static
class MyStaticClass:
    pass

# Trying to instantiate MyStaticClass will raise an exception
instance = MyStaticClass()  # Raises: Exception: This class is static and cannot be instantiated!
```

### @threaded

The `@threaded` decorator transforms any class into a threaded class, returning a thread object when the class is instantiated. This feature is experimental and might fail, please report any errors.

```python
from decoutilities import threaded

@threaded
class MyThreadedClass:
    def __init__(self, value):
        self.value = value

    def run(self):
        print(f"Running with value {self.value}")

# Instantiate MyThreadedClass, which returns a thread object
thread = MyThreadedClass(5)

# Start the thread
thread.start()

# Outputs: Running with value 5
```

### @trycatch

The `@trycatch` decorator wraps a function in a try-catch block, allowing it to handle exceptions without needing to write explicit try-catch blocks in your code.

```python
from decoutilities import trycatch

@trycatch
def risky_function():
    # Some risky operation that might raise an exception
    return 1 / 0

risky_function()  # Prints: An error occurred: division by zero
```

### @loop(condition_func)

The `@loop` decorator is an experimental feature that allows a function to loop until a certain condition is met. The condition is a function that returns a boolean value.

```python
from decoutilities import loop

var1 = 0

@loop(lambda: var1 > 10)
def increment_var1():
    global var1
    var1 += 1
    print(var1)

increment_var1()  # This will keep running until 'var1' is greater than 10
```

### @deprecated

The `@deprecated` decorator marks a function as deprecated and prints a log when it's used for the first time. It also raises a `DeprecationWarning`.

```python
from decoutilities import deprecated

@deprecated
def old_function():
    print("This function is old.")

old_function()  # Prints a warning and "This function is old."
```

### @experimental

The `@experimental` decorator marks a function as experimental and prints a log when it's used for the first time. It also raises a `UserWarning`.

```python
from decoutilities import experimental

@experimental
def new_function():
    print("This function is new and experimental.")

new_function()  # Prints a warning and "This function is new and experimental."
```

### @notnull

The `@notnull` decorator ensures that a function does not return `None`.

```python
from decoutilities import notnull

@notnull
def function_that_should_not_return_none():
    return None  # Raises an exception

function_that_should_not_return_none()  # Raises an exception
```

### @delay(seconds)

The `@delay` decorator delays the execution of a function by a number of seconds.

```python
from decoutilities import delay

@delay(5)
def delayed_function():
    print("This function was delayed.")

delayed_function()  # Waits 5 seconds, then prints "This function was delayed."
```

### @timeout(seconds)

The `@timeout` decorator causes a function to time out after a number of seconds.

```python
from decoutilities import timeout

@timeout(5)
def long_running_function():
    while True:
        pass  # Raises an exception after 5 seconds

long_running_function()  # Raises an exception after 5 seconds
```

### @retry(attempts, delay)

The `@retry` decorator retries a function a number of times with a delay between each attempt.

```python
from decoutilities import retry

@retry(3, 1)
def unreliable_function():
    import random
    if random.random() < 0.5:
        raise Exception("The function failed.")
    else:
        print("The function succeeded.")

unreliable_function()  # Tries to run the function up to 3 times, with a 1 second delay between attempts
```

### @log

The `@log` decorator logs a function's arguments and return value.

```python
from decoutilities import log

@log
def function_to_log(a, b):
    return a + b
function_to_log(1, 2)  # Prints "Function function_to_log called with args: (1, 2) and kwargs: {}, returned: 3"
```

### @benchmark

The `@benchmark` decorator is used to measure the execution time of a function. It prints the time it took for the function to execute in seconds.

```python
from decoutilities import benchmark

@benchmark
def my_function():
    pass
```

### @ignore

The `@ignore` decorator is used to ignore a function. When a function is decorated with `@ignore`, it does nothing.

```python
from decoutilities import ignore

@ignore
def my_function():
    pass
```

### @abstract

The `@abstract` decorator is used to make a function abstract. If a function decorated with `@abstract` is called, it raises an exception indicating that the function must be implemented in a subclass.

```python
from decoutilities import abstract

@abstract
def my_function():
    pass
```

### @accepts(*types)

The `@accepts` decorator is used to check if the arguments of a function are of the specified types. If an argument is not of the specified type, it raises a `TypeError`.

```python
from decoutilities import accepts

@accepts(int, str)
def my_function(arg1, arg2):
    pass
```

### @returns(type)

The `@returns` decorator is used to check if the return value of a function is of the specified type. If the return value is not of the specified type, it raises a `TypeError`.

```python
from decoutilities import returns

@returns(int)
def my_function():
    return "not an integer"  # Raises a TypeError
```

### @webhook(url)

The `@webhook` decorator is used to send a webhook to a specified URL with the function's arguments and return value. It uses the `requests.post` method to send the data.

```python
from decoutilities import webhook

@webhook("http://my-webhook-url.com")
def my_function(arg1, arg2):
    return arg1 + arg2
```

### @yieldable

The `@yieldable` decorator is used to make a function yieldable. It returns a generator that yields the result of the function.

```python
from decoutilities import yieldable

@yieldable
def my_function():
    return "yielded value"
```



### Config System

`decoutilities` provides a complex config system that allows you to easily manage configuration settings using decorators.

#### configContainer

The `configContainer` class is responsible for loading and saving configuration data from/to JSON or YAML files.

```python
from decoutilities.config import configContainer

# Create a configContainer instance
config_container = configContainer(path="config", filename="settings", type="json")

# Register values
config_container.registerValues({
    "api_key": "your_api_key",
    "timeout": 5
})

# Get a value
api_key = config_container.getValue("api_key")

# Set a value
config_container.setValue("timeout", 10)
```

#### config

The `config` class works in conjunction with `configContainer` to provide a decorator-based approach for registering settings.

```python
from decoutilities.config import config, configContainer

# Create a configContainer instance
config_container = configContainer(path="config", filename="settings", type="json")

# Create a config instance
config_instance = config(config_container)

# Register a setting using the @setting decorator
@config_instance.setting()
def api_key():
    return "your_api_key"

# Access the registered setting
api_key = config_container.getValue("api_key")
```

### Inject System

`decoutilities` comes with an easy to use injector class (EXPERIMENTAL) that allows to easily share information.
Note: The recently added `registerClass` method allows to register classes instead of single functions, recommended combination with `singleton` decorator.

```python
from decoutilities.inject import injector

# Create an instance of the injector
injector_instance = injector()

# Register a function with the injector
@injector_instance.register('greet')
def greet(name):
    return f"Hello, {name}!"

# Use the injector to get the function
greet_func = injector_instance.inject('greet')

# Call the function
print(greet_func('World'))  # Outputs: Hello, World!
```

### Queue

The `Queue` class provides a simple implementation of a queue data structure. It also logs every action performed on the queue.

```python
from decoutilities.queue import Queue

# Create a Queue instance
queue = Queue()

# Add an item to the queue
queue.add_item('item1')

# Remove an item from the queue
removed_item = queue.remove_item()

# Check the first item in the queue without removing it
first_item = queue.check_item()

# Clear the queue
queue.clear_queue()

# Print the log of actions performed on the queue
queue.print_log()
```

#### Methods

- `add_item(item)`: Adds an item to the end of the queue.
- `remove_item()`: Removes and returns the first item in the queue. If the queue is empty, it returns `None`.
- `check_item()`: Returns the first item in the queue without removing it. If the queue is empty, it returns `None`.
- `clear_queue()`: Clears all items from the queue.
- `print_log()`: Prints the log of actions performed on the queue. Each log entry includes the timestamp, action, item, and the size of the queue after the action.

## Data Encryption Module

This module provides a way to encrypt and decrypt data, either in the form of text strings or files. It uses an XOR encryption system with a randomly generated key.

### Classes

The module consists of two main classes:

1. `keyManager`: This class is responsible for generating a unique encryption key. The key is randomly generated each time a `keyManager` instance is created.

2. `dataEncryptor`: This class uses an instance of `keyManager` to encrypt and decrypt data. The data can be a text string or a file.

### Usage

To use this module, you first need to create an instance of `keyManager`:

```python
key_manager = keyManager()
```

Next, you can create an instance of `dataEncryptor` using the `keyManager`:

```python
encryptor = dataEncryptor(key_manager)
```

Now you can encrypt and decrypt data. To encrypt data, use the `encrypt` method:

```python
encrypted_data = encryptor.encrypt(source, 'string')  # To encrypt a text string
encrypted_file = encryptor.encrypt(source, 'file')  # To encrypt a file
```

To decrypt data, use the `decrypt` method:

```python
decrypted_data = encryptor.decrypt(encrypted_data, 'string')  # To decrypt a text string
decrypted_file = encryptor.decrypt(encrypted_file, 'file')  # To decrypt a file
```

### Key Generation

The key generation process in `keyManager` is designed to be secure. It uses a large random number as the basis for the key, which makes it difficult for an attacker to guess. The length of the key also contributes to its security. The longer the key, the more possible combinations there are, making it harder for an attacker to crack.

### Notes

This module uses XOR encryption, which is not secure for most practical uses. It is recommended to use a more secure encryption algorithm for any data that needs protection in the real world.

## Text Utilities

The `textUtils` class provides methods for formatting and decorating text in the console. It includes methods for coloring text, adding decorations such as bold, underline, and italic, and a general format method that replaces aliases with their corresponding ANSI escape codes.

### Usage

To use this class, you must not initialize it, otherwise it will throw an error.

```python
from decoutilities.textUtils import color, formated, decorate
from decoutilities.textUtils import format as textFormat # Recommended importing with other name to prevent conflicts with python's default format funcion

print(color("red", "This is a red-colored text!"))
print(decorate("bold", "This is a bold text!"))

# You can make also a function always output a formated string
@formated
def pig()
    return "{purple}Oink Oink!"

print(pig())

# Or use the format function!
print(textFormat("Hello my {red}red{reset}friends! Ready for a {bold}new {reset}adventure?"))
```

### Methods

- `color(color, text)`: Colors the text with the specified color. The available colors are: red, green, yellow, blue, purple, cyan, white, dark_red, dark_green, gold, gray, dark_gray, black, and reset.

- `decorate(decoration, text)`: Decorates the text with the specified decoration. The available decorations are: bold, underline, and italic.

- `format(text)`: Replaces aliases in the text with their corresponding ANSI escape codes. The available aliases are the same as the colors and decorations listed above.

- `@formated`: Decorator used to make a function's output return always a colorful string.

### Notes

The `format` method applies the ANSI escape codes in the order they appear in the text. If the same alias appears multiple times in the text, all instances will be replaced. The `reset` alias resets all formatting, so it can be used to stop the effect of a previous alias.

## MiniMessage Text Coloring

This feature allows coloring text in a similar way you would format messgaes with MiniMessage from Kyori (Minecraft), this feels an easier way to some users, as consists on tags, meaning you can do something like this:

```python
from decoutilities.textUtils.minimessage.minimessage  import MiniMessage

# Create an instance of the MiniMessage Class
mm = MiniMessage()

# Now use it with the parse method to parse a text, this is the only public method this class contains.
print(mm.parse('<white>I <red>love</red> decoutilities! This function was added on <b>0.3.4</b></white>'))
```

### Components

Components are a powerful feature to use with the MiniMessage text coloring, it allows to store the text information, dividing it in segments with the respective colors.

To create a component:
```python
from decoutilities.textUtils.minimessage.component import Component
from decoutilities.textUtils.minimessage.minimessage  import MiniMessage

mytext = Component().fromText("<red>This is a test <bold>of the <green>MiniMessage<reset> class<red>")
parser = MiniMessage()

print(parser.parse(mytext)) # This will print the text with the colors and styles applied
```

You may also use `.replace` over the Component to replace strings, or print the raw component (a json with all the data and styling information)

## Logger

The `Logger` class provides methods for logging events and messages with different levels of severity. It includes methods for logging info, warning, error, success, debug, and announcement messages. The messages can be formatted using the `textUtils` class and can optionally be written to a log file.

### Usage

To use this class, you first need to create an instance of `Logger`:

```python
from decoutilities.logger import Logger

logger = Logger(prefix='MyApp', debug=True, log='app.log')
```

You can then use the `info`, `warning`, `error`, `success`, `debug`, and `announce` methods to log messages:

```python
# Log an info message
logger.info('This is an info message.')

# Log a warning message
logger.warning('This is a warning message.')

# Log an error message
logger.error('This is an error message.')

# Log a success message
logger.success('This is a success message.')

# Log a debug message
logger.debug('This is a debug message.')

# Log an announcement
logger.announce('This is an announcement.')
```

### Methods

- `info(message)`: Logs an info message.
- `warning(message)`: Logs a warning message.
- `error(message)`: Logs an error message.
- `success(message)`: Logs a success message.
- `debug(message)`: Logs a debug message if the `debug` attribute of the `Logger` instance is `True`.
- `announce(message)`: Logs an announcement.

### Notes

The `Logger` class uses the `textUtils` class to format the messages. The format of the messages can be specified when creating a `Logger` instance with the `format` parameter. The `{event}` placeholder in the format string is replaced with the event type (e.g., "INFO", "WARNING"), and the `{message}` placeholder is replaced with the actual message.

If a `log` parameter is provided when creating a `Logger` instance, the logged messages will also be written to the specified log file.

## Components

`decoutilities` includes a basic component feature that replaces Python default inputs in certain situations. Altrough this feature was not tested on Linux and MacOS, I suppose it should work.

### Selector

The `Selector` component allows to make selections of only ONE item, here is a piece of code.

```python
from decoutilities.components import Selector
from decoutilities.textUtils import format as color # The method to import directly was added on 0.2.9

database = Selector("Please choose a database:", ["{green}MongoDB", "{blue}MariaDB", "{gold}MySQL"])

result = database.display()

print(color("{bold}You selected: "+result))
```

### Checkmarks

Also, as the `Selector` feature, this one works the same way.

```python
from decoutilities.components import Checkmark

features = Checkmark("Which features would you like to install?", ["Dark Mode", "SSR Support"]) # TIP: Add ["| 🟩", "| ⬛"] as the third argument to customize the prefixes of the selected (0) and unselected (1) options.

selected = features.display()

print(selected)

```


### Input

The `Input` class is a utility for creating interactive console inputs with validation rules. 

#### Importing the Class

```python
from decoutilities.components import Input
```

#### Creating an Instance

```python
name = Input('Password', '', 'REQUIRED|PASSWORD', 'The text is hidden')
```

#### Displaying the Input

```python
name.display()
```

#### Validation Rules

The `Input` class supports a variety of validation rules. These rules are passed as a string when creating an instance of the class. Multiple rules can be combined using the pipe character (`|`).

Here are the available rules and their usage:

- `REQUIRED`: The input must not be empty.
- `PASSWORD`: The input will be hidden.
- `EMAIL`: The input must be a valid email address.
- `NUMBER`: The input must be a number.
- `STRING`: The input must be a string.
- `MIN:<number>`: The input must be at least `<number>` characters long.
- `MAX:<number>`: The input must be at most `<number>` characters long.
- `LENGTH:<number>`: The input must be exactly `<number>` characters long.
- `REGEX:<pattern>`: The input must match the regex `<pattern>`.
- `CONTAINS:<value>`: The input must contain `<value>`.
- `NOT_CONTAINS:<value>`: The input must not contain `<value>`.
- `IN:<value1,value2,...>`: The input must be one of the specified values.
- `NOT_IN:<value1,value2,...>`: The input must not be one of the specified values.
- `EQUALS:<value>`: The input must be equal to `<value>`.
- `NOT_EQUALS:<value>`: The input must not be equal to `<value>`.
- `HIGHER:<number>`: The input must be higher than `<number>`.
- `LOWER:<number>`: The input must be lower than `<number>`.
- `HIGHER_OR_EQUAL:<number>`: The input must be higher or equal to `<number>`.
- `LOWER_OR_EQUAL:<number>`: The input must be lower or equal to `<number>`.
- `FLOAT`: The input must be a float.
- `BOOLEAN`: The input must be a boolean (`true` or `false`).
- `JSON`: The input must be a valid JSON string.
- `IP`: The input must be a valid IP address.
- `URL`: The input must be a valid URL.
- `DATE`: The input must be a valid date (`YYYY-MM-DD`).
- `TIME`: The input must be a valid time (`HH:MM:SS`).
- `DATETIME`: The input must be a valid datetime (`YYYY-MM-DD HH:MM:SS`).
- `PHONE`: The input must be a valid phone number (10 digits).
- `PASSWORD`: The input must be a valid password (Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character).

#### Example

```python
email = Input('Email', '', 'REQUIRED|EMAIL', 'Enter your email')
email.display()
```

This will create an input that requires a valid email address.

## Screen Utils

### Screen

Screen is a way to easily know the terminal's size. Altough for the moment it only has this feature, will have more as the development continues. As right now this feature is not long enough to have its own section on the README.md I will not explain it in detail, however you are free to check the source code if wondering to use it.

`0.3.6` > This section is fully untested, code was not finished and some feautres here were discarded because of their complexity.

Problems found:
- This feature is extemely hard to tesst, as it requires a multithreaded or multiprocess environment.

### Titler

This one, relays on the `Screen` feature, and allows to make simple titles.

```python
from decoutilities.screenUtils import Titler

welcome = Titler('Welcome to my program!', '[ Press anything to continue ]')  # last argument is optional

welcome.show()
```

## Experimental Features

All features marked as in `BETA` or being `EXPERIMENTAL` are untested, what means they were only tested below specific condititons and not with all case of uses.

Please report any issues or contribute by making a PR (look for [CONTRIBUTING](CONTRIBUTING) section for details).

### REMEMBER:

This whole project is still in beta, and versions below `0.1.5` might not work. Also syntax changes could be made in a future, so consider creating a `requeriments.txt`file for your project specifying the version you wonder to use.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Quick explanation of MIT license
MIT license is OSI approved, meaning you can do anythihng you wish with this project. Reuploading forks, selling copies (may be legally a scam as this free), modifying on own convenience...

This means you also may copy code from this project if you wish to.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/Reddishye/decoutilities).

### Pull Requests

In case you wonder to make a pull request, please include in the title any of these:
- FEATURE: For new features, include a explanation mentioning why it should be inside `decoutilities`.
- BUGFIX: For general bugfixes.
- SECURITY: For fixes related with security issues.
- QoL: For QoL improvements

## Author

- [Hugo Torres](https://github.com/Reddishye)