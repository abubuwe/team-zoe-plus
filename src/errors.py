from claude import complete
from prompts import build_heading_prompt

class AccessibilityEditor:
    def __init__(self, dom: any):
        self._dom = dom
        self._handlers = {
            "alt_missing": self.handle_alt_missing,
            "heading_empty": self.handle_heading_missing
            # TODO: Add more!
        }

    def handle_alt_missing(self, details: dict):
        # Do something with the DOM to fix the "alt_missing" error
        pass

    def handle_unregistered_error(self, error_type: str, details: dict):
        if error_type not in self._handlers:
            raise RuntimeError(f"Handler for error: {error_type} not registered")
        
        self._handlers[error_type]

    def handle_heading_missing(self, _: dict):
        # TODO: This needs to be a string representation of the DOM
        prompt = build_heading_prompt(self._dom)
        return complete(prompt)