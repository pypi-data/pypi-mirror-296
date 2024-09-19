from pathlib import Path

# Modules to test from
import stylemapper.helpers.validate_paths as validate_paths
import stylemapper.helpers.compare as compare
import stylemapper.helpers.read_args as read_args


# USES PYTEST
# set paths as global variables
VALID_CSS = "tests/styles.css" 
INVALID_CSS = "stylesheet.css"
VALID_HTML = "tests/template1.html"
INVALID_HTML = "html_document.html"
FOLDER_ONLY_HTML = "tests/templates"  # Path to folder with ONLY html files
FOLDER_WITH_HTML = "tests/mixed_with_html"  # Folder with multiple file types including HTML files
FOLDER_WITHOUT_HTML = "tests/mixed_without_html"  # Folder with multiple file types NOT including HTML files

def main():
    pass


# Tests for  validate_paths.py
def test_css_validity():
    assert validate_paths.is_css_file(VALID_CSS) == True
    assert validate_paths.is_css_file(INVALID_CSS) == False


def test_html_validity():
    assert validate_paths.is_html_file(VALID_HTML) == True
    assert validate_paths.is_html_file(INVALID_HTML) == False


def test_html_folders():
    folder_only_html_paths = ['tests/templates/template4.html', 'tests/templates/_layout.html']
    folder_with_html_paths = ['tests/mixed_with_html/template3.html', 'tests/mixed_with_html/template2.html']
    assert validate_paths.retrieve_html_paths(FOLDER_ONLY_HTML) == folder_only_html_paths
    assert validate_paths.retrieve_html_paths(FOLDER_WITH_HTML) == folder_with_html_paths
    assert validate_paths.retrieve_html_paths(FOLDER_WITHOUT_HTML) == []


def test_filepath_name_cleaning():
    assert validate_paths.clean_filepath_name(VALID_HTML) == "template1.html"
    assert validate_paths.clean_filepath_name(FOLDER_WITH_HTML) == "mixed_with_html"


# Tests for read_args.py
def test_cssinfo():
    cssobject = read_args.CSSInfo("tests/styles.css")
    classes = ['page-container', 'bg-container', 'title-text', 'protest', 'unused-class']
    ids = ['id-selector1', 'id-selector2']
    media = ['media screen and (max-width: 666px)']
    elements = ['html']


    assert cssobject.get_classes() == classes
    assert cssobject.get_ids() == ids
    assert cssobject.get_media() == media
    assert cssobject.get_elements() == elements


def test_all_cssinfo():
    cssobject = read_args.CSSInfo("tests/styles.css")
    css_info = {'classes' : ['page-container', 'bg-container', 'title-text', 'protest', 'unused-class'],
                'ids' : ['id-selector1', 'id-selector2'],
                'media' : ['media screen and (max-width: 666px)'], 
                'elements' : ['html']}

    assert cssobject.all() == css_info
    


def test_htmlinfo():
    htmlobject = read_args.HTMLInfo("tests/template1.html")
    classes = ['green-text', 'bg-container', 'protest']
    ids = ['bigTextBox', 'testForDupe']
    inline_styling = ['padding: 5px;']

    for each_class in classes:
        assert each_class in htmlobject.get_classes()

    for each_id in ids:
        assert each_id in htmlobject.get_ids()

    for each_style in inline_styling:
        assert each_style in htmlobject.get_inline()


def test_all_htmlinfo():
    htmlobject = read_args.HTMLInfo("tests/template1.html")
    html_info = {'class': {'green-text', 'bg-container', 'protest'}, 
                 'id': {'bigTextBox', 'testForDupe'}, 
                 'style': {'padding: 5px;'}}

    html_output = htmlobject.all()

    for selector in html_info:
        for value in list(html_info[selector]):
            assert value in list(html_output[selector])


# Tests for compare.py
def test_valid_comparisons():
    css_classes = ['1', '2', '3', 'unused']
    html_classes = ['1', '2', '3']
    
    assert compare.compare_classes(css_classes, html_classes) == ['unused']


def test_invalid_comparisons():
    css_classes1 = []
    css_classes2 = ['1', '2', '3', 'unused']
    html_classes1 = ['1', '2', '3']
    html_classes2 = []
    
    assert compare.compare_classes(css_classes1, html_classes1) == []
    assert compare.compare_classes(css_classes2, html_classes2) == ['1', '2', '3', 'unused']


def test_html_object_merging():
    htmlobject1 = read_args.HTMLInfo("tests/template1.html")
    htmlobject2 = read_args.HTMLInfo("tests/mixed_with_html/template2.html")

    expected_output = {'class': {'protest', 'bg-container', 'green-text'}, 
              'id': {'bigTextBox', 'testForDupe'}, 
              'style': {'padding: 5px;'}}
    merged_output = compare.merge_html_objects([htmlobject1, htmlobject2])

    # Convert each set into a list to check if the value is present in merged list
    for selector in expected_output:
        for value in list(expected_output[selector]):
            assert value in list(merged_output[selector])



if __name__ == "__main__":
    main()