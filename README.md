- [Wiki](#wiki)
  - [Files](#files)
    - [views.py](#viewspy)
      - [\*CreateView](#createview)
      - [EntryUpdateView](#entryupdateview)
      - [wiki](#wiki-1)
      - [image](#image)
      - [search](#search)
      - [search results](#search-results)
    - [forms.py](#formspy)
      - [\*CreateForm](#createform)
      - [\*UpdateForm](#updateform)
    - [models.py](#modelspy)
      - [Entry](#entry)
      - [Image](#image-1)
    - [util.py](#utilpy)
      - [generic\_search](#generic_search)
    - [wiki\_syntax.py](#wiki_syntaxpy)
      - [EntryLink](#entrylink)
      - [BleachPreprocessor](#bleachpreprocessor)
    - [\_\_init\_\_.py](#__init__py)
    - [search.js](#searchjs)
  - [Full list of new features](#full-list-of-new-features)

# Wiki
This is my final project for CS-33a

## Files

### views.py

#### *CreateView
views for creating new entries/images (inherit from django's CreateView)

#### EntryUpdateView
Updates an entry, titles have a unique constraint, so get_object is overridden to use that instead of pk or slug
get_form_class avoids needing separate views for each of the forms that update entry

#### wiki
Displays entry content and talk pages

#### image
Single image pages

#### search
api endpoint for the autocomplete search bar

#### search results
view for the normal search (accessed by pressing enter in the autocomplete search bar)

### forms.py
Contains all Django forms

#### *CreateForm
Creates new entries/images

#### *UpdateForm
Edits existing pages
(I was unable to find a good way to combine the content and talk forms)

### models.py
Both non-user models use the django-simple-history package to keep track of changes to the pages

#### Entry
Used for storing articles' content and talk pages\

#### Image
Stores image objects (path to the image, stored at images/) with a name and history

### util.py
misc functions used by more than one class or view

#### generic_search
Both api/search/ and search/ use this to retrieve search results

### wiki_syntax.py
contains WikiSyntax, a [python-markdown](https://python-markdown.github.io/) extension

#### EntryLink
Converts [[entry_title]] to a link to /wiki/entry_title/ (and entry_title as text)

#### BleachPreprocessor
uses the 'bleach' library to sanitize input (removes tags not specified in ALLOWED_TAGS)

### \_\_init__.py
fixes issue where bleach broke some markdown syntax

### search.js
Autocomplete search bar, shows top results for the query entered (first title matches, then content)
if part of the title matches the query, that part of it will be bold

## Full list of new features
TODO
