import argparse
try:
    from stylemapper.helpers.validate_paths import is_css_file, is_html_file, retrieve_html_paths
except ModuleNotFoundError:
    from helpers.validate_paths import is_css_file, is_html_file, retrieve_html_paths


def main():
    pass


class GetHTMLPaths(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        choices = ["classes_html", "inline", "ids", "all"]
        needed_choices = set()
        paths = set()

        # Processing the validity of each file happens through argparse action
        for value in values:
            value = value.strip().lower()
            
            if value in choices:
                needed_choices.add(value)
            
            # Check if the current value is a valid HTML path
            # Program gets here if value is NOT a choice
            else:
                if '.' in value: # Checks if path is a file or a folder
                    if is_html_file(value):
                        paths.add(value)
                else: # Returns a list of exact paths to html files within a folder
                    parsed_paths: list = retrieve_html_paths(value)
                    if parsed_paths:
                        for path in parsed_paths:
                            # Merge all HTML paths from folder into html_paths list
                            paths.add(path)
                    else:
                        print(f"The folder you provided '{value}', did not contain any HTML files.")
                        print("If your HTML file is stacked in a directory deeper than 3, please include a direct path instead.")
        
        if not needed_choices:
            parser.error(f"At least 1 choice from {choices} is required.")

        # Close programm if multiple choices have been passed with an 'all' argument
        for choice in list(needed_choices):
            if len(list(needed_choices)) > 1 and choice == 'all':
                parser.error("Do NOT include 'all' as a choice with other choices.")

        if not paths:
            parser.error("Please provide path to HTML doc, or folder containing HTML doc.")

        setattr(namespace, self.dest, needed_choices)
        setattr(namespace, "paths", list(paths))


class GetCSSPath(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        choices = ["classes_css", "ids", "media", "element", "all"]
        needed_choices = set()
        stylesheet_path = ""

        if values:
            for value in values:
                value = value.strip().lower()
                if value in choices:
                    needed_choices.add(value)
                else:
                    if not is_css_file(value):
                        parser.error(f"'{value}' is an invalid stylesheet path. Use 'stylemapper [-u or -h]' for help.")

                    if stylesheet_path:
                        parser.error(f"Please check your choices are spelt correctly, or make sure you only provide ONE stylesheet path")
                    stylesheet_path = value
        
        
        if not needed_choices:
            parser.error(f"At least 1 choice from {choices} is required.")

        # Close programm if multiple choices have been passed with an 'all' argument
        for choice in list(needed_choices):
            if len(list(needed_choices)) > 1 and choice == 'all':
                parser.error("Do NOT include 'all' as a choice with other choices.")

        if not stylesheet_path:
            parser.error("Please provide path to a CSS stylesheet")

        setattr(namespace, self.dest, needed_choices)
        setattr(namespace, "stylesheet_path", stylesheet_path)


class CheckComparisonPaths(argparse.Action):
    def __call__(self, parser, namespace, values, option_string: str | None = None) -> None:
        if values:
            if len(values) != 2:
                parser.error("Please provide 1 stylesheet and 1 folder containing HTML files.")
            stylesheet: str = values[0]
            html_folder: list = values[1]
            paths = list()

            if not is_css_file(stylesheet):
                parser.error(f"'{stylesheet}' is not a valid CSS file")
            paths.append(stylesheet)

            # Passing a folder is critical as to follow the users expected use of stylemapper
            # Specific error messages can be used, however, due to accepting a folder instead of path.
            try:
                html_paths = retrieve_html_paths(html_folder)
            except NotADirectoryError:
                parser.error("Please provide a valid folder path containing HTML files")

            for path in html_paths:
                if path not in paths:
                    paths.append(path)

        else:
            print("You MUST provide the exact path to file")
            parser.error("Please provide 1 stylesheet and 1 HTML document.")

        setattr(namespace, self.dest, paths)
        setattr(namespace, "paths", paths)



def create_flags():
    parser = argparse.ArgumentParser(
        prog = "stylemapper",
        description = "This script analyzes a stylesheets and templates, providing information regarding classes & styling used.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.usage = """stylemapper [-h / --help | -u / --usage]
       stylemapper --compare 'stylesheet_path' 'html_folder_path'
       stylemapper --getcss [choices] 'stylesheet_path'
       stylemapper --gethtml [choices] 'html_file_path' | 'html_folder_path'
       Use 'stylemapper -u | --usage' for more info."""

    # Group ensures argparse error handles multiple args on command line
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-u', '--usage',
                       help="Details all ways to use programm, including flag usage.",
                       action='store_true')
    
    group.add_argument('--getcss',
                       action=GetCSSPath,
                       metavar="[choice]",
                       nargs='+',
                       help="""CHOICES: ["classes_css", "ids", "media", "element", "all"]
--------------------------------------------
You MUST include at least one choice from 'CHOICES' after --getcss. 
You MUST also include the exact path to your stylesheet you wish to
be scanned, eg: 'templates/styles.css'.
--------------------------------------------
classes_css: gets all classes created within stylesheet
ids: gets name of all ids created within stylesheet
media: gets all @media querise created within stylesheet
element: gets all instances of styling created on specific
elements.\n
""")

    
    group.add_argument('--gethtml',
                       action=GetHTMLPaths,
                       metavar="[choice]",
                       nargs="+",
                       help="""CHOICES: ["classes_html", "inline", "ids", "all"]
--------------------------------------------
You MUST include at least one choice from CHOICES after --gethtml. 
You may also pass '.html' files as extra arguments if you want to 
only scan specific files. If no path or folder is passed an extra 
argument, stylemapper will scan entire directory for all instances 
of '.html' files to read and return info based on your choice.
--------------------------------------------
classes_html: gets all classes used within html files
inline: gets instances of all inline styling used, along with 
line number and file name.
ids: gets name of all ids used within html files.\n
""")
    
    group.add_argument('--compare',
                       action=CheckComparisonPaths,
                       nargs="+",
                       metavar="paths",
                       help="""Use:
 --------------------------------------------
 You MUST include exact path to ONLY one (1) stylesheet/.css file.
 You MUST include exact path to AT LEAST one (1) template/.html file.
 --------------------------------------------
 Compare will retrieve all class selectors from CSS stylesheet,
 and scan the provided HTML files to let you know which selectors
 are not being used in your HTML code.
""")
    
    return parser


if __name__ == "__main__":
    main()