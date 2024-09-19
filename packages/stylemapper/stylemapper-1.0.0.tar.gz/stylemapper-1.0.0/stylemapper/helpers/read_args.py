import re
from bs4 import BeautifulSoup

try:
    from stylemapper.helpers.validate_paths import clean_filepath_name
except ModuleNotFoundError:
    from helpers.validate_paths import clean_filepath_name

def main():
    pass


class CSSInfo():
    def __init__(self, path: str) -> None:
        self.path = path
        self.clean_path: str = clean_filepath_name(path)
        self.contents = []
        self.parsed_contents = {'classes' : [],
                                'ids': [],
                                'media' : [],
                                'elements' : []}

        with open(path, 'r') as file:
            self.contents = file.readlines()

        # Call parse_stylesheet to populate attributes
        self.parse_stylesheet()
    

    # One function to populate individual lists instead of copying same
    # for loop in multiple different functions.
    def parse_stylesheet(self):
        for line in self.contents:
            stripped_line = line.strip()

            # strip called again to remove whitespace after removing '{'
            if stripped_line.startswith("."): # Classes
                each_class = stripped_line.lstrip(".").rstrip("{").strip()
                if not re.search(r"[\s:]", each_class) and each_class not in self.parsed_contents['classes']:
                    self.parsed_contents['classes'].append(each_class)

            elif stripped_line.startswith('#'): # ID's
                each_id = stripped_line.lstrip("#").rstrip("{").strip()
                if each_id not in self.parsed_contents['ids']:
                    self.parsed_contents['ids'].append(each_id)

            elif stripped_line.startswith('@'): # Media Query's
                each_media = stripped_line.lstrip("@").rstrip("{").strip()
                if each_media not in self.parsed_contents['media']:
                    self.parsed_contents['media'].append(each_media)
        
            elif stripped_line.endswith("{") and not re.search(r"^\W", stripped_line): # Element Styling
                each_element = stripped_line.rstrip("{").strip()
                if each_element not in self.parsed_contents['elements']:
                    self.parsed_contents['elements'].append(each_element)

            # Anything else is not something tracked in this version of StyleMapper
            else:
                continue
            

    def all(self):
        return self.parsed_contents


    """All below functions return a list, which is the value
    of the specified key."""
    def get_classes(self):
        return self.parsed_contents['classes']


    def get_ids(self):
        return self.parsed_contents['ids']


    def get_media(self):
        return self.parsed_contents['media']

    
    def get_elements(self):
        return self.parsed_contents['elements']



# This class can one or multiple paths to files or folders
class HTMLInfo():
    def __init__(self, path: str) -> None:
        self.path = path
        self.clean_path: str = clean_filepath_name(path)
        self.contents: str = None
        # self.parsed_contents = {selector_type : set(selector_names)}
        self.parsed_contents: dict = {}

        with open(path, 'r') as file:
            self.contents = file.read()

        # Call parse_stylesheet to populate attributes
        self.parse_html_doc()

    
    def parse_html_doc(self):
        soup = BeautifulSoup(self.contents, 'html.parser')
        elements_with_class = soup.find_all(class_=True)
        elements_with_id = soup.find_all(id=True)
        elements_with_inline = soup.find_all(style=True)

        # Populate parsed_content dict with line number and class data
        def populate_parsed_content(elements: list, selector_type: str):
            current_info = set()
            # Iterate over elements soup extracted from contents
            for element in elements:
                try:
                    selector_names: list = element.get(selector_type)
                    if selector_names:
                        if selector_type == "class":
                            for selector in selector_names:
                                current_info.add(str(selector))
                        else:
                            current_info.add(str(selector_names))
                except AttributeError as e:
                    print(f"Error processing element: {e}")

            self.parsed_contents[selector_type] = list(current_info)

        # Run nested function to add the data to data structure
        populate_parsed_content(elements_with_class, 'class')
        populate_parsed_content(elements_with_id, 'id')
        populate_parsed_content(elements_with_inline, 'style')


    def all(self):
        return self.parsed_contents


    def get_classes(self):
        return self.parsed_contents['class']

    def get_ids(self):
        return self.parsed_contents['id']


    def get_inline(self):
        return self.parsed_contents['style']


if __name__ == "__main__":
    main()