#!/usr/bin/env python
import os
import sys
import subprocess
"""n Store and Retrieve Notes.

See the README file or `n --help` for usage.

TODO
----
*	Print out an error msg if notes dir is empty and no search words are given.
*	Handle case-insensitive filesystems.
*	Ask for the user's permission before creating the notes directory.

"""
def get_all_notes(notes_dir):
	"""Return a list of all the note files in notes_dir.

	Note files are top-level .txt files in notes_dir.

	"""
	paths = [os.path.join(notes_dir,path) for path in os.listdir(notes_dir)]
	note_paths = []
	for path in paths:
		head, tail = os.path.split(path)
		if tail.endswith('~') or tail.startswith('.'):
			# Skip backup files and hidden files.
			continue
		root, ext = os.path.splitext(tail)
		if not ext ==  '.txt':
			# Skip non-txt files.
			continue
		if not os.path.isfile(path):
			# Skip non-files.
			continue
		note_paths.append(path)
	return note_paths

def get_matching_notes(notes,search_words):
	"""Filter the list of notes and return only those notes that match all of
	the search words."""
	
	matching_notes = []
	for note in notes:
		path,filename = os.path.split(note)
		contents = open(note,'r').read()
		discard = False
		for search_word in search_words:
			if search_word.islower():
				# Search for word case-insensitively.
				if (not search_word in filename.lower()) and (not search_word in contents.lower()):
					discard = True
					break
			else:
				# Search for word case-sensitively.
				if (not search_word in filename) and (not search_word in contents):
					discard = True
					break
		if not discard:
			matching_notes.append(note)
	return matching_notes

def get_number(prompt,default):
	"""Get an int from the user.

	"""
	try:
		input = raw_input("%s: [%s] " % (prompt,default)).strip()
	except KeyboardInterrupt:
		sys.exit()
	if input == "": input = default
	try:
		number = int(input)
	except ValueError:
		sys.exit("That is not a number.")
	if number < 0:
		sys.exit("That number is out of range.")
	return number

def system(cmd):
	"""Execute a system command in a subshell and return the exit status.

	"""
	p = subprocess.Popen(cmd,shell=True)
	return os.waitpid(p.pid,0)[1]

def main(notes_dir,search_words,editor):

	# Convert notes_dir to an absolute path and create it if it doesn't exist.
	notes_dir = os.path.abspath(os.path.expanduser(notes_dir))
	if not os.path.isdir(notes_dir):
		os.mkdir(notes_dir)

	# Get the paths of all the note files that match the search words.
	paths = get_matching_notes(get_all_notes(notes_dir),search_words)
	# Sort the paths by modification time.
	paths.sort(key = lambda path: os.path.getmtime(path))

	# Check if there is a note whose filename matches the search terms exactly.
	is_exact_match = False
	if search_words:
		exact_match = os.path.join(notes_dir," ".join(search_words) + ".txt")
		if exact_match in paths:
			is_exact_match = True
			paths.remove(exact_match)
		paths.append(exact_match)

	# Print out the menu.
	for i,path in enumerate(paths[:-1]):
		print str(len(paths)-1-i)+': '+os.path.split(path)[1]
	if is_exact_match or not search_words:
		print "0: %s" % os.path.split(paths[-1])[1]
	else:
		print "0: Create note: '%s'" % os.path.split(paths[-1])[1]
	
	# Get the user's response.
	selected_number = get_number("Enter a number",0)
	try:
		selected_path = paths[len(paths)-1-selected_number]
	except IndexError:
		sys.exit("That number was out of range.")

	# Call the editor.
	sys.exit(system('%s "%s"' % (editor,selected_path)))

if __name__ == '__main__':
	from optparse import OptionParser
	usage ="%prog [options] [search words]"
	description="""Search, view, create and edit plain text notes. Prints
a menu listing plain text note files in NOTES_DIR. A note file can be
selected from the menu to open it in EDITOR. If search words are given
then only notes containing all of the search words will be listed."""
	parser = OptionParser(usage=usage,description=description)
	parser.add_option('-e', '--editor', dest='editor', action='store',
			default='$EDITOR', help="the text editor to use for opening note files (defaults to %default)")
	parser.add_option('-d', '--directory', dest='notes_dir',
			action='store', default='~/txt/', help="the notes directory to use (defaults to %default)")
	(options, args) = parser.parse_args()
	main(notes_dir=options.notes_dir, search_words=args, editor=options.editor)
