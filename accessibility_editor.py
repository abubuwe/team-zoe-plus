from colorutils import Color
from lxml import etree
from html_modifier import get_elem_from_path

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

    def handle_heading_missing(self, _: dict):
        # TODO: This needs to be a string representation of the DOM
        prompt = build_heading_prompt(self._dom)
        return complete(prompt)
