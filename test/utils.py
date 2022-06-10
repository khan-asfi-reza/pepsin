def make_multiple_inputs(inputs):
    """ provides a function to call for every input requested. """

    def next_input(_):
        """ provides the first item in the list. """
        return inputs.popleft()

    return next_input
