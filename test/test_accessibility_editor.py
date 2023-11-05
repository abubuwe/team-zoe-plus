import unittest, json, os, sys

# Get parent directory for imports
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
 
from accessibility_editor import AccessibilityEditor
from html_modifier import parse_html

class TestAccessibilityEditor(unittest.TestCase):
    def  __init__(self, *args, **kwargs):
        super(TestAccessibilityEditor, self).__init__( *args, **kwargs)
        
        with open('test.html', encoding="utf8") as f:
            self.html_string = f.read()
        
        self.dom = parse_html(self.html_string)
        self.accessibility_editor = AccessibilityEditor(self.dom)
    
    def test_increase_contrast(self):

        # Load example JSON as details dict
        with open('example_contrast_error.json') as f:
            details_dict = json.load(f)
        
        new_html_string, changes = self.accessibility_editor._increase_contrast(details_dict)
        with open("new_html_test.html", "w") as f:
            f.write(new_html_string)

        print(changes)
        with open("html_changes.json", "w") as f:
            json.dump(changes, f, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    unittest.main()