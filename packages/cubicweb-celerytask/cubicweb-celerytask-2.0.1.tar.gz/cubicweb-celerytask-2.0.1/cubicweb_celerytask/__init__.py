"""cubicweb-celerytask application package

Run and monitor celery tasks
"""


class _States:
    """Helper class to create customizable state "lists". Each state is
    accessible as an attribute and the list may be customized by patching the
    resulting object.
    """

    def __init__(self, *args):
        super().__init__()
        for arg in args:
            setattr(self, arg, arg)

    def __contains__(self, item):
        return hasattr(self, item)


STATES = _States("PENDING", "STARTED", "SUCCESS", "FAILURE", "REVOKED")

FINAL_STATES = _States("SUCCESS", "FAILURE", "REVOKED")
