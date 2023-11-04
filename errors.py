from colorutils import Color
from lxml import etree
from html_modifier import get_elem_from_path

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

    def handle_contrast_error(self, details: dict):
        xpaths = details["contrast"]["items"]["contrast"]["xpaths"]

        contrast_data = details["contrast"]["items"]["contrast"]["contrastdata"]

        changes_dict = {}

        for xpath, data in zip(xpaths, contrast_data):
            background_colour = data[2]
            colour_obj = Color(background_colour)
            
            opp_colour_obj = colour_obj.commplementary()
            opp_colour = opp_colour_obj.hex

            elem = get_elem_from_path(xpath, self._dom)
            elem.set("style", f"colour: {opp_colour}")

            changes_dict[xpath] = etree.tostring(elem).decode()

        return etree.tostring(self._dom).decode(), changes_dict

    def handle_error(self, error_type: str, details: dict):
        if error_type not in self._handlers:
            raise RuntimeError(f"Handler for error: {error_type} not registered")
        
        self._handlers[error_type]

