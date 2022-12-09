- [Wiki](#wiki)
  - [Files](#files)
    - [forms.py](#formspy)
    - [models.py](#modelspy)
      - [Entry](#entry)
      - [Image](#image)
    - [util.py](#utilpy)
      - [generic\_search](#generic_search)
    - [wiki\_syntax.py](#wiki_syntaxpy)
      - [EntryLink](#entrylink)
      - [BleachPreprocessor](#bleachpreprocessor)
      - [\_\_init\_\_.py](#__init__py)

# Wiki
This is my final project for CS-33a

## Files

### forms.py
Contains all Django forms
- login is done with the LoginView view

### models.py

#### Entry
Used for storing the content of the articles\
This uses the django-simple-history package to keep track of changes to the pages

#### Image
Stores image objects (path to the image, stored at images/) with a name and history

### util.py
misc functions used by more than one class or view

#### generic_search
Both api/search/ and search/ use this to retrieve search results

### wiki_syntax.py
Contains WikiSyntax and its processors

#### EntryLink
Converts [[entry_title]] to a link to /wiki/entry_title/ (and entry_title as text)

#### BleachPreprocessor
uses the 'bleach' library to sanitize input (removes tags specified in ALLOWED_TAGS)

#### \_\_init__.py
fixes issue where bleach broke some markdown syntax
