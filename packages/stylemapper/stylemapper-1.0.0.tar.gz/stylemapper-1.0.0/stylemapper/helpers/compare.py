def main():
    pass


def compare_classes(css_classes: list, html_classes: list):
    unused_classes = []
    for item in css_classes:
        if item not in html_classes:
            unused_classes.append(item)

    return unused_classes


def merge_html_objects(html_objects: list):
    new_dict = {'class' : set(), 
                'id' : set(), 
                'style' : set()}
    selectors = ['class', 'id', 'style']

    # Iterate over each object in html_objects
    for object in html_objects:
        # Get ALL HTML information from object
        result = object.all()
        # Iterate over each selector type in the resulting dictionary
        for selector in selectors:
            # Update the values for each selector in new dictionary
            # Set takes care of duplicate entries for each selector
            for value in result[selector]:
                new_dict[selector].add(value)

    return new_dict



if __name__ == "__main__":
    main()