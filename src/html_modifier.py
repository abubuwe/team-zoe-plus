from lxml import etree, html

def html_accessibility(html_file):
    return html_file


# Returns an lxml ElementTree object
def parse_html(html_string):
    tree = html.fromstring(html_string)
    tree = etree.ElementTree(tree)
    return tree

# Returns a list of lxml Element objects that match the xpath
def get_elem_from_path(xpath, html_string):
    tree = parse_html(html_string)
    elem = tree.xpath(xpath)
    return elem