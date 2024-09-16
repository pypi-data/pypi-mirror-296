def hello_world(name: str) -> str:
    """
    This is a simple function that exists just to validate our documentation and building process.

    :param name: The name of the person to greet.
    :return: A greeting string.
    """
    greeting = "Hello, {}".format(name)
    return greeting
