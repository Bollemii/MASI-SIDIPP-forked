class IdeaAlreadyExistsError(Exception):
    """
    Exception raised when attempting to create an idea that already exists.
    """

    def __init__(self, inner_error: Exception):
        super().__init__()
        self.inner_error = inner_error
