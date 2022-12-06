# Wiki

# forms.py
Contains all Django forms
- login is done with the LoginView view

# models.py
## Entry
Used for storing the content of the articles\
This uses the django-simple-history package to keep track of changes to the pages

# util.py
## generic_search
Both api/search/ and search/ use this to retrieve search results
