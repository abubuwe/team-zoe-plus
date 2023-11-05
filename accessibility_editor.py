from lxml import etree
from html_modifier import get_elem_from_path

from claude import complete
from utils import complementary_colour
from prompts import build_heading_prompt
from captioning import caption_image

class AccessibilityEditor:
    def __init__(self, dom: any):
        self._dom = dom
        self._handlers = {
            "alt_missing": self._handle_alt_missing,
            "heading_empty": self._handle_heading_missing,
            "title_invalid": self._handle_heading_missing,
            "contrast": self._increase_contrast
        }
    
    def _increase_contrast(self, details: dict):
        xpaths = details["items"]["contrast"]["xpaths"]
        contrast_data = details["items"]["contrast"]["contrastdata"]
        changes_dict = {}

        for xpath, data in zip(xpaths, contrast_data):
            # Set the text to be complementary to the background:
            opp_colour = complementary_colour(data[2])

            elem = get_elem_from_path(xpath, self._dom)
            elem.set("style", f"colour: {opp_colour}")

            # TODO: Verify this:
            changes_dict[xpath] = etree.tostring(elem).decode()
        
        # TODO: Verify this:
        return etree.tostring(self._dom).decode(), changes_dict
    
    def _handle_alt_missing(self, details: dict):
        # TODO: Get the image somehow
        
        # with open("strictly.png", "rb") as rf:
        #     alt_text = caption_image(rf.read())

        # print(f"ALT_TEXT: {alt_text}")
        # TODO: Add the alt_text to the DOM
        pass
    def _handle_heading_missing(self, _: dict):
        # TODO: This needs to be a string representation of the DOM
        # TODO: Limit the input size
        prompt = build_heading_prompt(self._dom)
        
        # TODO: Use the completed prompt to update the DOM
        return complete(prompt)
    
    def fix(self, error_type: str, details: dict):
        if error_type not in self._handlers:
            raise RuntimeError(f"Handler for error: {error_type} not registered")
        
        self._handlers[error_type](details)
