# Library of Congress Digital Collections & the Zooniverse Project Builder

Python script to upload Zooniverse subjects from a Library of Congress digital collection item's segments.

## Purpose

The purpose of the `import_subjects.py` script is to create a Zooniverse subject set from a Library of Congress digital collection item. Library of Congress item segments correspond to Zooniverse subjects.

## Resources

- [Library of Congress Digital Collections](https://www.loc.gov/collections/)
- [Library of Congress API documentation](https://libraryofcongress.github.io/data-exploration/index.html)
  - specifically [requesting an item](https://libraryofcongress.github.io/data-exploration/requests.html#requesting-a-specific-item)
- [Library of Congress data exploration](https://github.com/LibraryOfCongress/data-exploration)
- [Zooniverse Project Builder](https://www.zooniverse.org/lab)

## Requirements

- Python 2 or above
- text editor
- patience with JSON
- Library of Congress digital collection item ID
- Zooniverse username, password and project ID

## Instructions

1. Clone/download/copy `import_subjects.py` to your computer, open with editor of choice and review comments in code.
2. Identify a Library of Congress Digital Collection **item** and set `import_subjects.py`'s LIBRARY_OF_CONGRESS_ITEM_ID accordingly - i.e. the [Anna Maria Brodeau Thornton Papers: Diaries and journals; Vol. 1, 1793-1804](https://www.loc.gov/item/mss5186201) ID is `mss5186201`.
    - note that an item is a subset of a collection; our example item is part of the the [Anna Maria Brodeau Thornton Papers collection](https://www.loc.gov/collections/anna-maria-brodeau-thornton-papers/).
3. Add "?fo=json" to the item url to receive [a JSON version of the item](https://www.loc.gov/item/mss5186201?fo=json).
4. Review the JSON version of the item (using https://codebeautify.org/jsonviewer, https://jsonblob.com/ or JSON viewer of choice) to identify the desired subject url (FILE_INDEX) and METADATA fields you wish to be included in your [Zooniverse subject metadata](https://www.zooniverse.org/help#subjects) and update `import_subjects.py`'s FILE_INDEX and METADATA accordingly.
    - **FILE_INDEX**: your item's JSON includes a `resources` array of objects. Each resource object includes a `files` array. Each file is an array of objects representing various types and sizes for each segment. Set the `FILE_INDEX` as the file array index for the segment object that best suits the [Zooniverse subject size guidelines](https://www.zooniverse.org/talk/18/593574?comment=987125&page=1) as well as your project's needs.
5. Configure `import_subjects.py` with your Zooniverse username, password and project ID.
6. Run `python import_subjects.py` from Mac terminal, Windows command line or equivalent.

## Warnings

- the script has only been tested on Library of Congress "manuscript/mixed material" items
- this is a hackday project, with limited support and maintenance, though we'll do our best to help
