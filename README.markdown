`note.py` is a _very_ simple command that tries to make it as quick and easy as
possible to make new notes or to find and open existing notes:

    $ note recipe
    5: Coconut Vegetable Curry Recipe.txt
    4: Spinach Bhaji Recipe.txt
    3: Scrambled Tofu Recipe.txt
    2: Banana Pancakes Recipe.txt
    1: Shepherd's Pie Recipe.txt
    0: Create note: 'recipe.txt'
    Enter a number: [0] _

To open a new or existing note run `note.py [arguments]`. It searches your notes
directory and prints a list of notes that match the words in your argument, and
asks you whether you want to open one of the notes or create a new note with a
filename based on your argument and open that. Type the number of the file you
want to open and hit `<Enter>`, the file will be opened in your `$EDITOR`.

The notes are kept as plain text files in a `~/Notes` directory. (You can use
a command-line option or config file to specify a different notes directory
location).

To list _all_ your notes and open one of them, just run `note.py` without an
argument. In this case the default choice will be to open the most recently
modified note, rather than to create a new note, so this is a quick way to
re-open your last modified note.

To see the command-line options and config file format, run `note.py -h`.


Install
-------

Requires [Python 2](http://www.python.org/). If using Python 2.6 or older, you
also need to install argparse:

    $ pip install argparse

Then just checkout or download `note.py` from GitHub and run it. It can be
convenient to add an alias in your shell config file (e.g. `~/.bashrc` or
`~/.zshrc`):

    alias note="/path/to/note.py"


Details
-------

-  Notes are printed most recently modified last, so if you have a lot of notes
   it's the older ones that scroll off the top of your terminal.

-  If your argument contains spaces you don't have to wrap it in quotes (but
   you can if you want to).

-  You don't have to include the filename extension in your note title, it will
   be appended for you.

-  The search is fuzzy. A note will match a search term if it contains all of
   the given search words anywhere in its filename (including filename
   extension, and subdir names) or file contents, the words don't have to
   appear consecutively or in the same order.

-  The search is smart-case. For each search word, if the word is all
   lower-case then it will be matched case-insensitively. If the word contains
   any upper-case letters then it will be matched case-sensitively.

-  Subdirectories in your notes directory are searched recursively. To create a
   new note in a subdirectory, just give the relative path in the argument to
   the `note.py` command:

        $ note.py 'programming/python/How to use decorators in Python'

-  You can have note files with different filename extensions. All the files in
   your notes directory are searched, regardless of filename extension. To
   create a note with a different filename extension use the `--extension`
   option.

-  The `note.py` command doesn't support renaming or moving notes, but you can
   move note files (and edit their contents) using other tools, this will not
   interfere with the `note.py` command as long as you don't do it while
   `note.py` is running.
