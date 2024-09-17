

class PsyException(Exception):
    """Base class for exceptions in the psy module."""
    pass

class ExperimentStopped(PsyException):
    """Exception raised when the experiment is stopped."""
    pass