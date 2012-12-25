#!/usr/bin/env python
"""Create and search plain text note files"""

import os
import sys
import subprocess


def get_matching_notes(notes_dir, search_words):
    """Return all note files in notes_dir that match search_words.

    Searches the given notes_dir recursively and returns a list of absolute
    paths to the note files inside.

    """
    paths = []
    for root, dirs, files in os.walk(notes_dir):
        for filename in files:
            if filename.startswith('.') or filename.endswith('~'):
                # Ignore hidden and backup files.
                continue
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, notes_dir)
            contents = open(abs_path, 'r').read()
            discard = False
            for search_word in search_words:
                if search_word.islower():
                    # Search for word case-insensitively.
                    in_path = search_word in rel_path.lower()
                    in_contents = search_word in contents.lower()
                else:
                    # Search for word case-sensitively.
                    in_path = search_word in rel_path
                    in_contents = search_word in contents
                if (not in_path) and (not in_contents):
                    discard = True
                    break
            if not discard:
                paths.append(abs_path)
    return paths


def get_number(prompt, default):
    """Get an int from the user and return it."""

    try:
        answer = raw_input("{0}: [{1}] ".format(prompt, default)).strip()
    except KeyboardInterrupt:
        sys.exit()
    if answer == "":
        answer = default
    try:
        number = int(answer)
    except ValueError:
        sys.exit("That is not a number.")
    return number


def get_boolean(prompt, default):
    """Get a yes/no answer from the user and return it as True or False."""

    try:
        answer = raw_input("{0}: [{1}] ".format(prompt, default)).strip()
    except KeyboardInterrupt:
        sys.exit()
    if answer == "":
        answer = default
    if answer.lower() in ('y', 'yes'):
        return True
    else:
        return False


def system(cmd):
    """Execute a system command in a subshell and return the exit status."""

    p = subprocess.Popen(cmd, shell=True)
    return os.waitpid(p.pid, 0)[1]


def main(notes_dir, search_words, editor, extension):
    """The interactive notes command.

    Search `notes_dir` for note files containing `search_words`, print a list
    of matching files and get a selection from the user, then open the
    selected file with `editor`.

    """
    if not extension.startswith('.'):
        extension = '.' + extension

    # Convert notes_dir to an absolute path.
    notes_dir = os.path.abspath(os.path.expanduser(notes_dir))

    # Offer to creates notes_dir if it doesn't exist.
    if not os.path.isdir(notes_dir):
        if get_boolean("Create directory {0} (y/n)?".format(notes_dir), 'y'):
            os.makedirs(notes_dir)
            print "Created {0}".format(notes_dir)
            if not search_words:
                sys.exit()
        else:
            sys.exit("Okay ... fine then :(")

    # Get the paths of all the note files that match the search words.
    paths = get_matching_notes(notes_dir, search_words)
    if paths == [] and search_words == []:
        sys.exit("You don't have any notes yet")

    # Sort the paths by modification time.
    paths.sort(key=lambda path: os.path.getmtime(path))

    # Construct a file name from the given search terms. If there's a path in
    # paths that matches this constructed filename exactly, move that path
    # to the bottom of paths. If not, append the constructed filename to the
    # bottom of paths.
    is_exact_match = False
    if search_words:
        exact_match = os.path.join(notes_dir,
                " ".join(search_words) + extension)
        if exact_match in paths:
            is_exact_match = True
            paths.remove(exact_match)
        paths.append(exact_match)

    assert len(paths) >= 1

    if len(paths) == 1:
        selected_path = paths[0]
    else:
        # Print the list of matching notes.
        for i, path in enumerate(paths[:-1]):
            print str(
                len(paths) - 1 - i) + ': ' + os.path.relpath(path, notes_dir)
        if is_exact_match or not search_words:
            print "0: %s" % os.path.relpath(paths[-1], notes_dir)
        else:
            print "0: Create note: '{0}'".format(
                    os.path.relpath(paths[-1], notes_dir))

        # Get the user's response.
        selected_number = get_number("Enter a number", 0)
        try:
            selected_path = paths[len(paths) - 1 - selected_number]
        except IndexError:
            sys.exit("That number was out of range.")

    # Create subdirs if they don't already exist.
    subdir = os.path.split(selected_path)[0]
    if not os.path.isdir(subdir):
        os.makedirs(subdir)

    # Call the editor.
    sys.exit(system('{0} "{1}"'.format(editor, selected_path)))


if __name__ == '__main__':

    # Parse the command-line options and arguments and call main().
    from optparse import OptionParser
    usage = "%prog [options] [filename|search words]"
    description = """To create a new note run `%prog My New Note`.
To find notes about tofu recipes and choose one to open run
`%prog tofu recipe`.
To list all notes and choose one to open run `%prog`.
"""
    parser = OptionParser(usage=usage, description=description)
    parser.add_option('-e', '--editor', dest='editor', action='store',
            default='$EDITOR',
            help="the text editor to use (default: %default)")
    parser.add_option('-d', '--directory', dest='notes_dir', action='store',
            default='~/Notes',
            help="the notes directory to use (default: %default)")
    parser.add_option('-x', '--extension', dest='extension', action='store',
            default='txt',
            help="the filename extension for new notes (default: %default)")
    options, args = parser.parse_args()
    main(notes_dir=options.notes_dir, search_words=args,
         editor=options.editor, extension=options.extension)
