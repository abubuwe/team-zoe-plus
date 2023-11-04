class ErrorHandler:
    def __init__(self, dom: any):
        self._dom = dom
        self._handlers = {
            "alt_missing": self.handle_alt_missing
            # TODO: Add more!
        }

    def handle_alt_missing(self, details: dict):
        # Do something with the DOM to fix the "alt_missing" error
        pass

    def handle_error(self, error_type: str, details: dict):
        if error_type not in self._handlers:
            raise RuntimeError(f"Handler for error: {error_type} not registered")
        
        self._handlers[error_type]
