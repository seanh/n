`n`: Store and Retrieve Notes
-----------------------------

`n` is a simple command to help you manage a flat directory of plain text
notes. You keep all of your notes as plain text files in a directory and use
the simple command `n [search words]` to list your notes in order of
modification, search your notes, view, edit and create notes.

### Usage

The `n` command with no arguments prints an enumerated list of the filenames of
all files in `~/txt/`, most-recently-modified last:

    $ n
    5: todo
    4: Grocery list
    3: Recipe for miso soup
    2: How to read your email with mutt
    1: How to create HTML with markdown
    Enter a number: [1] _

The most-recently-modified files are printed last so that if you have a lot of
files it'll be the older ones that scroll off the top of your terminal.

Enter the number of a file at the prompt to open that file in your $EDITOR.
The default option (if you enter nothing at the prompt and just press return)
will be to open the most-recently-modified (and last printed) file.  Press
ctrl-c at the prompt if you don't want to open anything.

The `n` command with some arguments prints an enumerated list of the filenames
of those files from `~/txt/` that match all of the given search words:

    $ n how to
    2: How to read your email with mutt
    1: How to create HTML with markdown
    0: Create note: 'how to'
    Enter a number: [0] _

Again, enter the number of a file at the prompt to open it in your $EDITOR.

In this example the default option is to create a new note from the search
term. `n` doesn't actually create the note file, it just opens it in your
$EDITOR, to create the file you have to write it from your $EDITOR.

If an existing note's filename matches the search term exactly then the default
option will be to open that note instead.

#### Details

Only top-level files in `~/txt` are searched, subdirectories are ignored.

Both the file names and the file contents are searched.

The search is fuzzy. A file will match a search term if it contains all of the
search words anywhere in its file name or contents, the words do not have to
appear consecutively or in the same order as they are given in the search term.

The search is smart case. For each search word, if the word is all lower-case
then it will be matched case-insensitively. If the word contains any upper-case
letters then it will be matched case-sensitively.

#### Options

`-e`, `--editor`  
the text editor to use for opening note files (defaults to $EDITOR)

`-d`, `--notes-dir`  
the notes directory to use (defaults to ~/txt/)

`-h`, `--help`  
show a help message and exit
