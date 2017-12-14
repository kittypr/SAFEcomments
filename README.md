# SAFEcomments

This is script for transferring notes from version to version. Works with .odt files.
Python 3.6.3

## Installing:
*pip install git+https://github.com/kittypr/SAFEcomments.git*

## Usage:
*safe_comments.py input dest output -e A -f B*
Where:
 - **input** - file with notes.
 - **dest** - updated file in which you want to insert notes.
 - **output** - result of script's work - updated file with transferred notes.
 - **-e (-exact)**  A - float value from 0 to 1 - coefficient of acceptable length of substring, when we looking for commented
fragment. Default value - 0.6 (60%).
 - **-f (-fuzzy)**  B - float value from 0 to 1 - coefficient of acceptable fuzzy similarity, when we looking for commented
fragment. Default value - 0.6 (60%).

## More information:
1) It is better to avoid one-letter as commented fragment.
2) It is better to avoid more than one paragraph as commented fragment.
3) It does not support diagrams and figures as commented fragments.
4) All notes that have not appropriate places will be inserted at the end of documents.