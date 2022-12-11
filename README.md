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
    - [diff\_generator.py](#diff_generatorpy)
    - [\_\_init\_\_.py](#__init__py)
    - [search.js](#searchjs)
    - [timezone.js](#timezonejs)
  - [Full list of new features/changes](#full-list-of-new-featureschanges)

# Wiki
This is my final project for CS-33a

I've included an example database including the entry "Markdown Examples" that documents basic markdown syntax, this entry was created with multiple edits, so the history page has some info, the most recent edit has the most changes. The talk page does not have much on it (as it has no more features than the content page)

## Files

### views.py

#### *CreateView
views for creating new entries/images (inherit from django's CreateView)
  - entry_form.html
  - image_form.html

#### EntryUpdateView
Updates an entry, titles have a unique constraint, so get_object is overridden to use that instead of pk or slug\
get_form_class avoids needing separate views for each of the forms that update entry
  - entry_update_form.html

#### wiki
Displays entry content and talk pages\
Talk pages are differentiated by having the "talk:" prefix

#### image
Single image pages

#### search
api endpoint for the autocomplete search bar
  - search.js

#### search results
view for the normal search (accessed by pressing enter in the autocomplete search bar)

### forms.py
Contains all Django forms

#### *CreateForm
Creates new entries/images
  - entry_form.html
  - image_form.html

#### *UpdateForm
Edits existing pages (I was unable to find a good way to combine the content and talk forms)
  - entry_update_form.html

### models.py
Both non-user models use the django-simple-history package to keep track of changes to the pages

#### Entry
Used for storing articles' content and talk pages

#### Image
Stores image objects (path to the image, stored at images/) with a name and history
file url media/images/

### util.py
misc functions used by more than one class or view

#### generic_search
Both api/search/ and search/ use this to retrieve search results

### wiki_syntax.py
contains WikiSyntax, a [python-markdown](https://python-markdown.github.io/) extension

#### EntryLink
Converts [[entry_title]] to a link to wiki/entry_title/ (and entry_title as text)

#### BleachPreprocessor
uses the 'bleach' library to sanitize input (removes tags not specified in ALLOWED_TAGS)

### diff_generator.py
Contains CustomHtmlDiff, used to generate diffs between 2 historical records for entry or talk pages\
Admittedly, I think this is a very hacky approach, if I had more time, I would rewrite this to generate the html I want without overriding methods not meant to be overridden

### \_\_init__.py
fixes issue where bleach broke some markdown syntax

### search.js
Autocomplete search bar, shows top results for the query entered (first title matches, then content)
if part of the title matches the query, that part of it will be bold

### timezone.js
converts ISO8601 (or any format that can be converted into a Date object) into the user's local timezone

## Full list of new features/changes
- Markdown:
  - Switched to python-markdown from markdown2 because markdown2 is not well documented (and does not have any docs for the extension API as far as I could tell). Although python-markdown
  - added the following markdown extensions:
    - [Abbreviations](https://python-markdown.github.io/extensions/abbreviations/)
    - [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/)
    - [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/)
    - [Fenced Code Blocks](https://python-markdown.github.io/extensions/fenced_code_blocks/)
    - [Footnotes](https://python-markdown.github.io/extensions/footnotes/)
    - [Sane Lists](https://python-markdown.github.io/extensions/sane_lists/)
    - [Tables](https://python-markdown.github.io/extensions/tables/)
    - [Table of Contents](https://python-markdown.github.io/extensions/toc/)
    - WikiSyntax (created by me)
  - In most cases, markdown will not be processed if it is inside of HTML tags (that are inside the markdown document), the extension did not work properly
- Pages are now stored in a database
- User authentication
- History and diffs
- Autocomplete search
- Rewrote most of the views and forms from the original project to inherit from django's classes, I think this makes it more maintainable
- Image hosting (currently, there is no simple way to display an image like with entry links, here's an example of how an image can be linked currently: `![text](/media/images/image.webp){: style="width: 200px; height: auto;"}`)
- Various visual improvements (primarily through use of bootstrap's classes)
- Warning when leaving with unsaved changes
- Talk pages
