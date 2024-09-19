from tabulate import tabulate


"""beautify.py handles the majority of command line outputs. 
The 'all' case for both html and css creates an index based on the largest list of selectors 
found in the entire dictionary provided by stylemapper.py. The tabulate_css/html function is
NOT used on the 'case 'all'' as different parameters are being passed that would make
for a convoluted global function."""

"""Collects the cleaned results from 'result' argument and prints
a formatted answer based on the user arg selection."""
def css(result: list, arg: str):
    # Nested func to process results into a data for tabulate
    def tabulate_css(info, label):
        indexed_data = [[index, selector] for index, selector in enumerate(info, start=1)]
        table = tabulate(indexed_data, headers=['Index', f'{label}: {len(info)}'], tablefmt='rounded_outline')
        print(table)

    # Uses nested function to reduce redundancy and make code easier to maintain
    match arg:
        case 'classes_css':
            tabulate_css(result, 'Class Selectors')

        case 'ids':
            tabulate_css(result, 'ID Selectors')

        case 'media':
            tabulate_css(result, 'Media Queries')
            print("The ability to view each selector in your media queries is coming soon. Please be patient")

        case 'element':
            tabulate_css(result, 'Element Selectors')

        case 'all':
            index = 0
            # Set the index to the value of the longest list in the result dict
            for selector in result:
                value_count = len(result[selector])
                index = value_count if value_count > index else max(index, value_count)

            print(tabulate(result, showindex=range(1, index+1), headers="keys", tablefmt='rounded_outline'))

        case _:
            return ["Error processing chosen arg. Use 'stylemapper [-u or -h]' for help."]
        

def html(result: list, arg: str):
    # Nested func to process results into a data for tabulate
    def tabulate_html(info, label):
        indexed_data = [[index, selector] for index, selector in enumerate(info, start=1)]
        headers = ["Index", f"{label}: {len(info)}"]
        table = tabulate(indexed_data, headers=headers, tablefmt="rounded_outline")
        print(table)

    match arg:
        case 'classes_html':
            tabulate_html(result, 'Classes')

        case 'ids':
            tabulate_html(result, "ID's")

        case 'inline':
            tabulate_html(result, "Inline Styles")

        case 'all':
            index = 0
            for selector in result:
                value_count = len(result[selector])
                # Set index as the value of the longest list in dictionary
                index = value_count if value_count > index else max(value_count, index)

            print(tabulate(result, showindex=range(1, index+1), headers="keys", tablefmt='rounded_outline'))

        case _:
            return ["Error processing chosen arg. Use 'stylemapper [-u or -h]' for help."]

# Creates a table with the information on unused classes in all
# HTML files provided by the user. The table provides info on how
# many classes are being used out of how many have been created. EG: Unused Classes: 4/7
def comparisons(unused_classes, class_count):
    indexed_data = [[data] for data in unused_classes]
    headers = [f"Unused Classes: {len(unused_classes)}/{class_count}"]
    table = tabulate(indexed_data, headers=headers, tablefmt='rounded_outline')
    print(table)