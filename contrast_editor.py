from colorutils import Color
from lxml import etree
from html_modifier import get_elem_from_path

class ContrastEditor():
    def __init__(self, dom: any):
        self._dom = dom
        self._handlers = {
            "contrast": self._handle_contrast_errors
            # TODO: Find contrast error type
        }

    def _increase_contrast(self, details: dict):
        xpaths = details["xpaths"]

        contrast_data = details["contrastdata"]

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
    
    def handle_contrast_errors(self, error_type: str, details: dict):
        if error_type not in self._handlers:
            raise RuntimeError(f"Handler for contrast error: {error_type} not registered")
        
        self._handlers[error_type](details)