#!/usr/bin/env python2
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
    import argparse
    import ConfigParser

    # Parse the command-line option for the config file.
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", "--config", dest="config", action="store",
            default="~/.noterc",
            help="the config file to use (default: %(default)s)")
    args, remaining_argv = parser.parse_known_args()

    # Parse the config file.
    config_file = os.path.abspath(os.path.expanduser(args.config))
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    defaults = dict(config.items('DEFAULT'))

    # Parse the rest of the command-line options.
    description = """
create a new note and open it:               %(prog)s My New Note
find matching notes and choose one to open:  %(prog)s tofu recipe
list _all_ notes and choose one to open:     %(prog)s"""
    epilog = """
the config file can be used to override the defaults for the optional
arguments, example config file contents:

  [DEFAULT]
  editor = vim
  extension = txt
  notes_dir = ~/Notes

if there is no config file (or an argument is missing from the config file)
the default default will be used"""
    parser = argparse.ArgumentParser(description=description, epilog=epilog,
            parents=[parser],
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-e", "--editor", dest="editor", action="store",
        default=defaults.get("editor", "$EDITOR"),
        help="the text editor to use (default: %(default)s)")
    parser.add_argument("-d", "--directory", dest="notes_dir", action="store",
        default=defaults.get("notes_dir", "~/Notes"),
        help="the notes directory to use (default: %(default)s)")
    parser.add_argument("-x", "--extension", dest="extension", action="store",
        default=defaults.get("extension", "txt"),
        help="the filename extension for new notes (default: %(default)s)")
    parser.add_argument("search_words", action="store", nargs="*",
        help="the list of words to search for in your notes, "
          "also used as the filename if you choose to create a new note "
          "(optional, if no search words are given all notes will be listed)")
    args = parser.parse_args()

    main(notes_dir=args.notes_dir, search_words=args.search_words,
         editor=args.editor, extension=args.extension)
