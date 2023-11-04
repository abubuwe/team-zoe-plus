from colorutils import Color
from lxml import etree
from html_modifier import get_elem_from_path
from colorsys import rgb_to_hsv, hsv_to_rgb

from claude import complete
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
            # TODO: Add more!
        }

    @staticmethod
    def complementary(r, g, b):
        """returns RGB components of complementary color"""
        hsv = rgb_to_hsv(r, g, b)
        return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])

    def _increase_contrast(self, details: dict):
        xpaths = details["xpaths"]
        contrast_data = details["contrastdata"]
        changes_dict = {}

        for xpath, data in zip(xpaths, contrast_data):
            background_colour = data[2]
            colour_obj = Color(background_colour)
            
            opp_colour = self.complementary(colour_obj.rgb)
            elem = get_elem_from_path(xpath, self._dom)
            elem.set("style", f"colour: {opp_colour}")

            changes_dict[xpath] = etree.tostring(elem).decode()

        return etree.tostring(self._dom).decode(), changes_dict
    
    def _handle_alt_missing(self, details: dict):
        # TODO: Get the image somehow
        
        with open("../strictly.png", "rb") as rf:
            alt_text = caption_image(rf.read())

        print(f"ALT_TEXT: {alt_text}")
        # TODO: Add the alt_text to the DOM

    def _handle_heading_missing(self, _: dict):
        # TODO: This needs to be a string representation of the DOM
        prompt = build_heading_prompt(self._dom)
        return complete(prompt)
    
    def handle_accessibility_error(self, error_type: str, details: dict):
        if error_type not in self._handlers:
            raise RuntimeError(f"Handler for error: {error_type} not registered")
        
        self._handlers[error_type](details)
