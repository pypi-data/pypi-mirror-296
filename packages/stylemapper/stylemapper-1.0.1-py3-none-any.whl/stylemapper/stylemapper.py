import sys
import argparse

# Program ran as a package needs absolute filepath for imports
# try/except block works to allow program to run as a package and ran from
# terminal using 'python3 stylemapper/stylemapper.py' as a developer
try:
    from stylemapper.helpers import compare, beautify
except ModuleNotFoundError:
    from helpers import compare, beautify

try:
    from stylemapper.helpers.set_argparse import create_flags
except ModuleNotFoundError:
    from helpers.set_argparse import create_flags

try:
    from stylemapper.helpers.read_args import CSSInfo, HTMLInfo
except ModuleNotFoundError:
    from helpers.read_args import CSSInfo, HTMLInfo

try:
    from stylemapper.helpers.usage import usage
except ModuleNotFoundError:
    from helpers.usage import usage
# This solution is not ideal, but it works.


def main():
    arg_count = len(sys.argv)
    parser = create_flags()
    args: argparse.Namespace = parser.parse_args()

    # Gives user a different detailed help guide on how to use programm
    if args.usage:
        print(usage)

    # Compares all selectors in given stylesheet to the provided HTML templates
    # Will tell user which selectors from stylesheet are not being used
    elif args.compare:
        stylesheet_path: str = args.paths[0]
        html_paths: list = args.paths[1:]

        print(f"\nScanning '{stylesheet_path}'")
        cssinfo = CSSInfo(stylesheet_path)
        css_classes: list = cssinfo.get_classes()

        html_classes = set()
        for html_path in html_paths:
            print(f"Scanning '{html_path}'")
            htmlinfo = HTMLInfo(html_path).get_classes()
            for html_class in htmlinfo:
                html_classes.add(html_class)
        print("")
        
        unused_classes: list = compare.compare_classes(css_classes, list(html_classes))
        beautify.comparisons(unused_classes, class_count=len(css_classes))

    # Scans entire stylesheet for selectors
    # User specifies which selector type they want to view
    elif args.getcss:
        cssinfo = CSSInfo(args.stylesheet_path)
        print(f"\n↓↓↓ Scanning '{cssinfo.clean_path}' ↓↓↓")

        # Assert dictionary that maps all --getcss choices to respective functions
        # These will later get called if key has been passed to program
        css_arg_functions = {
            "ids": cssinfo.get_ids,
            "classes_css": cssinfo.get_classes,
            "media": cssinfo.get_media,
            "element": cssinfo.get_elements,
            "all" : cssinfo.all}
        
        # Loop to call each function in CSSInfo based on 'choices' that were previously passed
        for arg in args.getcss:
            try:
                result = css_arg_functions[arg]()
            except:
                print(f"ERROR: No function defined for argument {arg}")

            beautify.css(result, arg) # See 'beautify_css' for docstring         

    # Scans all provided HTML docs, or provided folders for HTML docs.
    # User specifies which style types they want information on.
    # This will print out the sheet, selector name, and line number selector is found on.
    elif args.gethtml:  # checks for --gethtml flag.
        html_paths: list = args.paths

        # Create HTMLInfo object for each path after all conditions are valid/met.
        html_objects = []
        for html_path in html_paths:
            htmlinfo = HTMLInfo(html_path)
            html_objects.append(htmlinfo)


        for arg in args.gethtml: # Iterate over each argument given to argparse.
            if arg == "all":
                merged_html_info: dict = compare.merge_html_objects(html_objects)
                beautify.html(merged_html_info, arg)
            else:
                for object in html_objects: # Iterate over each HTMLInfo object created.
                    # Assert the functions attached to specific arguments
                    html_arg_functions = {
                        "classes_html" : object.get_classes,
                        "ids" : object.get_ids,
                        "inline" : object.get_inline,
                        "all" : object.all}
                    # Call the correct method on each object based on current outer loop argument.
                    try:
                        result = html_arg_functions[arg]()
                    # If program reaches exception, something went very wrong somewhere
                    except KeyError:
                        print(f"ERROR: No function defined for argument {arg}")
                        sys.exit() 
                    
                    print(f"\n↓↓↓ Scanning '{object.clean_path}' ↓↓↓")  # Update user
                    beautify.html(result, arg) # Pass results and arg type to beautify_html to print results

    # UPCOMING VERSION
    # Will scan entire directory for stylesheet and ALL HTML docs.
    # Automatically run --compare on files found.
    else:  # if programm is run without arguments passed
        if arg_count == 1:
            # Create func for scanning directory for HTML and CSS files
            print("FEATURE COMING SOON")
            print("Use 'stylemapper [-u or -h]' for help.")
        else:
            print("Incorrect usage. Use 'stylemapper [-u or -h]' for help.")
            sys.exit()


if __name__ == "__main__":
    main()

