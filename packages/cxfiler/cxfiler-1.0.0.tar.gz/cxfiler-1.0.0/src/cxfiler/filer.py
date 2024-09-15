
import os, pwd, grp
import shutil
from datetime import datetime

from blessed import Terminal

from cerrax import DotDict
from bwk.characters import UnicodeChars as UTF
from bwk import Window, Border, echo, flush

#-==@h1 Classes
#
#-== - *FILER* is built on Blessed ( !https://pypi.org/project/blessed/ )
# -- and uses the Blessed Window Kit ( !https://pypi.org/project/bwk/ ).
#
#-== The application creates a /FileManager object, which has a collection of "modes".
# Each mode is a class which handles both input and output from the terminal.
# The application navigates between different modes by changing the current mode
# that the /FileManager is running.
#
#-== The typical application loop iteration runs as follows:
# //# Render the current mode to the terminal (via /mode.render() )
# //# Wait for input from the user
# //# Process received keystroke from the user
# //# If /running=False , end the application loop,
#     otherwise run the next iteration of the loop.


#-==@class
class FileType:
	#-== Enum class that defines file types.
	# @attributes
	# DIR: directory
	# FILE: non-directory file
	# LINK: symbolic or hard link
	# OTHER: other/unknown

	DIR = 'directory'
	FILE = 'file'
	LINK = 'link'
	OTHER = 'other'


ORDERS_OF_MAGNITUDE = [
	' byte', ' kB', ' MB', ' GB', ' TB',
	' PB', ' EB', ' ZB', ' YB', ' RB', ' QB'
]

FILETYPE_SYMBOL = {
	FileType.DIR: '/',
	FileType.FILE: ' ',
	FileType.LINK: '@',
	FileType.OTHER: '*'
}

PERMS = {
	'0': '---',
	'1': '--x',
	'2': '-w-',
	'3': '-wx',
	'4': 'r--',
	'5': 'r-x',
	'6': 'rw-',
	'7': 'rwx',
}


#-==@class
class ScanDirHelper:
	#-== Helper class which takes in a file and extracts information
	# into a simple and useful data structure.
	# @attributes
	# filename: the name of the file along with its file extension
	# inode: the inode reference for the file
	# path: the absolute path of the file
	# perms: a string indicating the permissions set on the file
	# owner: the owner of the file
	# group: the permission group of the file
	# filetype: one of the types listed in the /FileType enum class
	# size_bytes: the size of the file in bytes
	# size: a string indicating the file size in a human readable format
	# created: the date the file was created
	# modified: the date the file was most recently modified

	#-==@method
	def __init__(self, direntry):
		#-== Takes a file object and extracts all the relevant information about it.
		# @params
		# direntry: the file object to read

		stat = direntry.stat(follow_symlinks=False)
		self.filename = direntry.name
		self.inode = direntry.inode()
		self.path = os.path.abspath(direntry.path)
		self.perms = self.receive_perms(stat.st_mode)
		self.owner = pwd.getpwuid(stat.st_uid)[0]
		self.group = grp.getgrgid(stat.st_gid)[0]
		self.filetype = self.check_file_type(direntry)
		self.size_bytes = stat.st_size
		self.size = self.human_readable_size(stat.st_size)
		self.created = datetime.fromtimestamp(stat.st_ctime)
		try:
			self.created = datetime.fromtimestamp(stat.st_birthtime)
		except:
			pass
		self.modified = datetime.fromtimestamp(stat.st_mtime)

	#-==@method
	def is_hidden_file(self):
		#-== Indicates if the file is a hidden file.
		# @returns
		# /True if the filename starts with a period ( /. ),
		# /False otherwise.

		return self.filename[0] == '.'

	#-==@method
	def receive_perms(self, st_mode):
		#-== Transforms the permissions octet into
		# a more readble string in the format /rwxrwxrwx

		owner = '   '
		group = '   '
		other = '   '
		if st_mode is not None:
	 	perms_mod = '{:o}'.format(st_mode&0o07777)
	 	if len(perms_mod) >= 3:
		 	owner = PERMS[perms_mod[0]]
		 	group = PERMS[perms_mod[1]]
		 	other = PERMS[perms_mod[2]]
		return owner+group+other

	#-==@method
	def check_file_type(self, direntry):
		#-== @returns
		# One of the file types in the /FileType enum class.

		if direntry.is_symlink():
			return FileType.LINK
		if direntry.is_dir(follow_symlinks=False):
			return FileType.DIR
		if direntry.is_file(follow_symlinks=False):
			return FileType.FILE
		return FileType.OTHER

	#-==@method
	def human_readable_size(self, size_bytes, magnitude=0):
		#-== @returns
		# A string of the file size in a human readable format.

		#mag = float(pow(1024, magnitude+1))
		if size_bytes > 1024:
			size = self.human_readable_size(size_bytes/1024, magnitude+1)
		else:
			if magnitude == 0:
				size = str(size_bytes) + ORDERS_OF_MAGNITUDE[magnitude]
				if size_bytes != 1:
					size += 's'
			else:
				size = '{:.1f}'.format(size_bytes) + ORDERS_OF_MAGNITUDE[magnitude]
		return size


	def __str__(self):
		outstr = '\n------------------------------------'
		outstr+= '\nFilename:    '+str(self.filename)
		outstr+= '\niNode:       '+str(self.inode)
		outstr+= '\nPath:        '+str(self.path)
		outstr+= '\nPermissions: '+str(self.perms)
		outstr+= '\nOwner:       '+str(self.owner)
		outstr+= '\nGroup:       '+str(self.group)
		outstr+= '\nSize:        '+str(self.size)
		outstr+= '\nCreated:     '+str(self.created)
		outstr+= '\nModified:    '+str(self.modified)
		return outstr


#-==@class
class FileManagerMode:
	#-== Base class for defining the screens used in the application.
	# Subclasses will override methods provided for processing input
	# and displaying to the terminal screen.

	#-==@method
	def __init__(self, filemanager, name, commands={}):
		#-== Creates a mode for the application.
		# @params
		# filemanager: a /FileManager object
		# name: the name of the mode
		# commands: a dictonary where each key is a keyboard code,
		#						and the value is a function which should execute
		#						when that key is pressed

		self.fileman = filemanager
		self.name = name
		self.commands = commands
		self.set_commands()

	#-==@method
	def set_commands(self):
		#-== Identify keystrokes which correlate with logic to trigger.
		# This should be overridden in subclasses to set the keys used in that mode.
		#
		#-== For each keyboard key, set a string as the key in the /self.commands
		# dictionary and the value as a method to call when the key is pressed.
		# The method which is called is passed no arguments (except /self , if it is a class method).
		#
		#-==@codeblock
		# self.commands['h'] = self.show_help
		# @codeblockend
		#
		#-== If the key is a Unicode printable character, such as a letter, number, or punctuation,
		# use the string representation of that key.
		#
		#-== @note
		# The Space key is a printable character ( /' ' ) and should be indicated as such.
		#
		#-== @note
		# If an uppercase (or otherwised altered via the Shift key, such as the symbols on number keys)
		# is used, this will require the Shift key to be held when pressing the key to get a ppropriate result.
		# This is an easy way to incorporate modifier keys by using Shift as the modifier.
		#
		#-== If the key is a non-printable character (such as the Backspace, Enter, Esc, F# keys),
		# the name of the constant as defined in the Blessed documentation is used.
		# See the documentation for a list of supported names:
		#            !https://blessed.readthedocs.io/en/latest/keyboard.html#keycodes
		#
		#-== @note
		# Keys on the numpad are different keycodes, and as such,
		# they can only be identified by the name of their constant.
		# All numpad key constants start with /Key_KP_ .
		# For example, /9 on the numpad would be /KEY_KP_9 .
		#
		#-== **Example usage:**
		# @table
		# Line                                     | Key(s)
		# -----------------------------------------------------------------
		# self.commands['h'] = self.show_help      | /H
		# self.commands['H'] = self.show_help      | /Shift + /H
		# self.commands['KEY_ESCAPE'] = self.back  | /Esc
		# self.commands['9'] = self.options        | /9
		# self.commands['KEY_KP_9'] = self.options | /9 on the numpad
		# self.commands[' '] = self.select_item    | /Space
		# self.commands['1'] = self.action_menu    | /1
		# self.commands['!'] = self.second_menu    | /Shift + /1

		pass

	#-==@method
	def pre_process_input(self, key):
		#-== Any logic that should run before processing a keystroke.
		# This should be overridden in subclasses if necessary.

		pass

	#-==@method
	def post_process_input(self, key):
		#-== Any logic that should run after processing a keystroke.
		# This should be overridden in subclasses if necessary.
		# @note
		# This method runs, even if the mode is switched for
		# the current iteration of the application loop.
		# This is because the application loop does not actually run
		# any new mode until the next iteration of the loop starts.

		pass

	#-==@method
	def process_input(self, key):
		#-== Method that receives input from the terminal
		# and then activates the corresponding command (if one has been set).
		# @params
		# key: the input received from the terminal
		#
		#-== Subclasses should avoid overriding this method, as necessary
		# logic can usually be done in the /pre_process_input() or
		# /post_process_input() methods.

		keyname = key
		if key.is_sequence:
			keyname = key.name
		self.pre_process_input(key)
		try:
			self.commands[keyname]()
		except KeyError:
			pass
		self.post_process_input(key)

	#-==@method
	def render(self):
		#-== An abstract class for rendering output to the terminal.
		# As this is an abstract method, it *must* be overridden in a subclass
		# if that subclass is expected to display output to the user.
		# By default, this raises a /NotImplementedError .

		raise NotImplementedError


# FILER window sizes
PATH_WINDOW_HEIGHT = 1
FILELIST_WIDTH = 40
FILE_DETAILS_HEIGHT = 10
SCREEN_JUMP = 20

#-==@class
class FileListMode(FileManagerMode):
	#-== The "main" screen of FILER.
	# This screen displays a list of files within
	# the directory on the left side, and displays
	# information about the file the cursor is pointing to
	# on the right side of the screen.
	# The left side is a fixed width, whereas
	# the right side stretches to fill the entire terminal.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# /Up \/ /Down arrows | Navigate up and down the list of files
	# /" \/ /?            | Navigate a full screenful up or down
	# /Left arrow         | Move up one to the parent directory
	# /Right arrow        | Move into the directory (if current file is a directory)
	# /Enter              | Open the action menu (switch to /ActionMenu mode)
	# /.                  | Show/hide hidden files
	# /D                  | Show/hide directories
	# /F                  | Show/hide nondirectory files
	# /Space              | Select/deselect current file
	# /A                  | Select/deselect all files
	# /H                  | Show the help text
	# /Esc \/ /B          | Quit
	# /Q                  | Quit

	def set_commands(self):
		self.commands['KEY_UP'] = self.cursor_up
		self.commands['KEY_DOWN'] = self.cursor_down
		self.commands["'"] = self.jump_up
		self.commands["/"] = self.jump_down
		self.commands['KEY_LEFT'] = self.parent_dir
		self.commands['KEY_RIGHT'] = self.into_dir
		self.commands['KEY_ENTER'] = self.action_menu
		self.commands['KEY_ESCAPE'] = self.fileman.quit
		self.commands['b'] = self.fileman.quit
		self.commands['.'] = self.toggle_hidden_files
		self.commands['d'] = self.toggle_directories
		self.commands['f'] = self.toggle_show_files
		self.commands[' '] = self.toggle_select
		self.commands['a'] = self.select_all
		self.commands['h'] = self.show_help
		self.commands['q'] = self.fileman.quit

	def cursor_up(self):
		if self.fileman.current_index is not None and self.fileman.current_index > 0:
			self.fileman.set_current_file(self.fileman.current_index-1)

	def cursor_down(self):
		if self.fileman.current_index is not None and self.fileman.current_index < len(self.fileman.filelist)-1:
			self.fileman.set_current_file(self.fileman.current_index+1)

	def jump_up(self):
		if self.fileman.current_index is not None and self.fileman.current_index > 0:
			newindex = self.fileman.current_index-SCREEN_JUMP
			if newindex < 0:
				newindex = 0
			self.fileman.set_current_file(newindex)

	def jump_down(self):
		if self.fileman.current_index is not None and self.fileman.current_index < len(self.fileman.filelist)-1:
			newindex = self.fileman.current_index+SCREEN_JUMP
			if newindex > len(self.fileman.filelist)-1:
				newindex = len(self.fileman.filelist)-1
			self.fileman.set_current_file(newindex)

	def parent_dir(self):
		self.fileman.goto_dir('..', set_current_by_name=self.fileman.current_dir)

	def into_dir(self):
		if self.fileman.current_file is not None and self.fileman.current_file.filetype == FileType.DIR:
			self.fileman.goto_dir(self.fileman.current_file.filename)

	def action_menu(self):
		self.fileman.mode = self.fileman.modes.actions

	def show_help(self):
		self.fileman.mode = self.fileman.modes.help

	def toggle_file_display(self, display_param_name):
		man = self.fileman
		dparam = not getattr(man, display_param_name)
		setattr(man, display_param_name, dparam)
		man.collect_dir()
		newindex = man.find_filelist_index_by_name(man.current_file.filename)
		man.set_current_file(newindex)

	def toggle_hidden_files(self):
		self.toggle_file_display('show_hidden_files')

	def toggle_directories(self):
		self.toggle_file_display('show_directories')

	def toggle_show_files(self):
		self.toggle_file_display('show_files')

	def toggle_select(self):
		if self.fileman.current_file in self.fileman.selected_files:
			self.fileman.deselect_current()
		else:
			self.fileman.select_current()

	def select_all(self):
		if len(self.fileman.selected_files) > 0:
			self.fileman.selected_files.clear()
		else:
			self.fileman.selected_files = self.fileman.filelist.copy()

	def filelist_str(self, width, height):
		filelist_str = []
		man = self.fileman
		term = man.term

		for file in man.filelist:
			outstr = ''
			fillchar = ' '
			if man.is_selected(file):
				fillchar = UTF.line.solid.horizontal
			if file == man.current_file:
				outstr += '->'
			else:
				outstr += (fillchar*2)
			symbol = FILETYPE_SYMBOL[file.filetype]
			if file.filetype == FileType.FILE:
				symbol = fillchar
			outstr += symbol+fillchar
			filename = file.filename
			if len(filename) >= width-4:
				filename = filename[:width-6]+'..'
			outstr += term.ljust(filename, width=width, fillchar=fillchar)

			filelist_str.append(outstr)

		scroll_distance = 0
		if man.current_index is not None and man.current_index > height-1:
			scroll_distance = man.current_index - height+1

		return filelist_str[scroll_distance:]

	def current_file_details(self):
		man = self.fileman
		type = 'item'
		if man.show_files and not man.show_directories:
			type = 'file'
		if not man.show_files and man.show_directories:
			type = 'dir'
		suffix = ''
		if man.total_files != 1:
			suffix = 's'
		details_str = 'showing {} of {} {}{}\n'.format(man.displayed_files, man.total_files, type, suffix)

		detail_file = self.fileman.current_file
		if detail_file:
			details_str += '''
 {filename}

   {perms}
   {size}
   created:  {created}
   modified: {modified}
			'''
			details_str = details_str.format(
				filename=detail_file.filename,
				perms=str(detail_file.perms),
				size=detail_file.size,
				created=detail_file.created.strftime("%b %d,%Y %H:%M"),
				modified=detail_file.modified.strftime("%b %d,%Y %H:%M")
			)
		return details_str


	def render(self):
		term = self.fileman.term
		echo(term.clear)

		echo(term.reverse)
		path_border = Border()
		path_border.bottom_border = UTF.line.double.horizontal
		path_window = Window(term, 0, 0, height=PATH_WINDOW_HEIGHT, border=None)
		path_window.content = self.fileman.pwd
		path_window.render()
		echo(term.normal)

		filelist_border = Border()
		filelist_border.right_border = UTF.line.double.vertical
		filelist_window = Window(term, 0, PATH_WINDOW_HEIGHT,
									width=FILELIST_WIDTH, border=filelist_border)
		filelist_window.render_content = self.filelist_str
		filelist_window.render()

		file_details_border = Border()
		file_details_border.bottom_border = UTF.line.double.horizontal
		file_details = Window(term, FILELIST_WIDTH, PATH_WINDOW_HEIGHT,
								height=FILE_DETAILS_HEIGHT, border=file_details_border)
		file_details.content = self.current_file_details()
		file_details.render()


#-==@class
class ActionMenu(FileManagerMode):
	#-== The "action menu" is a menu which opens
	# below the file info panel on the right side of the terminal
	# which allows you to select actions you can perform
	# on the current file or a set of selected files.
	#
	#-== If you have selected one or more files
	# (via the /Space bar or /A key),
	# the action menu is acting upon those files.
	#-== If you do not have any files selected,
	# the action menu is acting upon the file
	# the cursor is currently pointing to.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# /Up \/ /Down arrows | Navigate up and down the list of actions available
	# /Enter              | Select the item the cursor is currently pointing to
	# /Esc \/ /B          | Back out of the action menu (back to /FileListMode mode)
	# /H                  | Show the help text
	# /Q                  | Quit

	#-==@method
	def __init__(self, filemanager, name, commands={}, x=0, y=0):
		#-== Creates the mode for the action menu.
		# @params
		# filemanager: a /FileManager object
		# name: the name of the mode
		# commands: a dictonary where each key is a keyboard code,
		#						and the value is a function which should execute
		#						when that key is pressed
		# x: the X-coordinate of where the action menu should
		#				render in the terminal window
		# y: the Y-coordinate of where the action menu should
		#				render in the terminal window

		super().__init__(filemanager, name, commands)
		self.current_index = 0
		self.x = x
		self.y = y
		self.menu_items = []
		self.set_menu_items()
	
	def pre_process_input(self, key):
		self.set_menu_items()

	def post_process_input(self, key):
		# there's no menu items, then after pressing anything,
		# it should go back
		if len(self.menu_items) == 0:
			self.back_to_main()

	def set_menu_items(self):
		man = self.fileman
		self.menu_items = []
		if self.check_copy_action():
			self.menu_items.append({'label': 'Copy to Here', 'exec': self.copy_items})
		if self.check_move_action():
			self.menu_items.append({'label': 'Move to Here', 'exec': self.move_items})
		if self.check_rename_action():
			self.menu_items.append({'label': 'Rename', 'exec': self.rename_item})
		if self.check_permissions_action():
			self.menu_items.append({'label': 'Change Permissions', 'exec': self.change_permissions})
		if self.check_delete_action():
			self.menu_items.append({'label': 'Delete', 'exec': self.delete_items})

	def set_commands(self):
		self.commands['KEY_UP'] = self.cursor_up
		self.commands['KEY_DOWN'] = self.cursor_down
		self.commands['KEY_ENTER'] = self.select_item
		self.commands['KEY_ESCAPE'] = self.back_to_main
		self.commands['b'] = self.back_to_main
		self.commands['h'] = self.show_help
		self.commands['q'] = self.fileman.quit

	def cursor_up(self):
		if self.current_index > 0:
			self.current_index -= 1

	def cursor_down(self):
		if self.current_index < len(self.menu_items)-1:
			self.current_index += 1

	def select_item(self):
		menu_function = self.menu_items[self.current_index]['exec']
		menu_function()

	def copy_items(self):
		man = self.fileman
		if not os.access(man.pwd, os.X_OK | os.W_OK):
			raise PermissionError('Cannot write to this directory')
		for file in man.selected_files:
			try:
				shutil.copy2(file.path, '.', follow_symlinks=False)
			except PermissionError:
				raise PermissionError('No permission to copy {}'.format(file.filename))
		man.collect_dir()
		new_index = man.find_filelist_index_by_name(getattr(man.current_file, 'filename', ''))
		man.set_current_file(new_index)
		man.selected_files.clear()
		self.back_to_main()

	def move_items(self):
		man = self.fileman
		if not os.access(man.pwd, os.X_OK | os.W_OK):
			raise PermissionError('Cannot write to this directory')
		for file in man.selected_files:
			try:
				shutil.move(file.path, '.')
			except PermissionError:
				raise PermissionError('No permission to move {}'.format(file.filename))
		man.collect_dir()
		new_index = man.find_filelist_index_by_name(getattr(man.current_file, 'filename', ''))
		man.set_current_file(new_index)
		man.selected_files.clear()
		self.back_to_main()

	def rename_item(self):
		self.fileman.mode = self.fileman.modes.rename

	def change_permissions(self):
		# TODO: Add permissions stuff
		pass

	def delete_items(self):
		term = self.fileman.term

		vcenter = int(term.height / 2)
		echo(term.move_xy(0, vcenter - 4))

		echo(term.black_on_bright_red)
		alertwin = Window(term, 0, vcenter - 4, 
							height=7, title='!! DELETE !!')
		alertwin.content = '\n' + term.center('Are you sure?') + \
							'\n \n' + term.center('[Y]es   [N]o')
		alertwin.render()
		echo(term.normal)
		flush()

		waiting_for_valid_input = True
		confirm_delete = False
		while waiting_for_valid_input:
			c = term.inkey()
			if c == 'y':
				waiting_for_valid_input = False
				confirm_delete = True
			elif c == 'n':
				waiting_for_valid_input = False

		if confirm_delete:
			man = self.fileman
			filelist = [man.current_file]
			if len(man.selected_files) > 0:
				filelist = man.selected_files
			for file in filelist:
				if file.filetype == FileType.DIR:
					shutil.rmtree(file.path)
				else:
					os.remove(file.path)
			man.collect_dir()
			man.set_current_file(man.current_index-1)
			man.selected_files.clear()
		self.back_to_main()


	def back_to_main(self):
		self.clear_menu()
		self.fileman.mode = self.fileman.modes.main

	def show_help(self):
		self.fileman.mode = self.fileman.modes.help

	def check_copy_action(self):
		man = self.fileman
		if len(man.selected_files) < 1:
			return False
		return True

	def check_move_action(self):
		man = self.fileman
		if len(man.selected_files) < 1:
			return False
		return True

	def check_rename_action(self):
		man = self.fileman
		if len(man.selected_files) > 0:
			return False
		if man.current_file is None:
			return False
		return True

	def check_permissions_action(self):
		return False

	def check_delete_action(self):
		man = self.fileman
		if len(man.selected_files) == 0 \
					and man.current_file is None:
			return False
		return True

	def render_menu(self, width, height):
		term = self.fileman.term
		rendered_menu = ['']
		i = 0
		for item in self.menu_items:
			item_str = '  '+item['label']
			if i == self.current_index:
				item_str = '  '+term.reverse+item['label']+term.normal
			rendered_menu.append(item_str)
			i += 1
		if len(self.menu_items) == 0:
			rendered_menu = [
				'No actions available.',
				'Press any key to continue..'
			]
		return rendered_menu

	def render(self):
		man = self.fileman
		term = self.fileman.term
		self.set_menu_items()
		menu_title = ''
		num_files = len(man.selected_files)
		if num_files > 0:
			menu_title = '{} file'.format(num_files)
			if num_files > 1:
				menu_title += 's'
			menu_title += ' selected'

		actions = Window(term, self.x, self.y, border=' '*8,
							title=menu_title, title_align='left')
		actions.render_content = self.render_menu
		actions.render()

	def clear_menu(self):
		self.current_index = 0


#-==@class
class RenameMode(FileManagerMode):
	#-== When "Rename" is selected from the action menu,
	# you can type in a new name for the file, and press
	# /Enter to confirm the change.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# /Enter              | Confirm the name typed as the new name of the file
	# /Esc                | Back out of the rename (back to /ActionMenu mode)

	#-==@method
	def __init__(self, filemanager, name, commands={}, x=0, y=0):
		#-== Creates the mode for the "Rename" action.
		# @params
		# filemanager: a /FileManager object
		# name: the name of the mode
		# commands: a dictonary where each key is a keyboard code,
		#						and the value is a function which should execute
		#						when that key is pressed
		# x: the X-coordinate of where the rename action should
		#				render in the terminal window
		# y: the Y-coordinate of where the rename action should
		#				render in the terminal window

		super().__init__(filemanager, name, commands)
		self.x = x
		self.y = y
		self.newname = ''

	def pre_process_input(self, key):
		if not key.is_sequence:
			self.add_char(key)

	def add_char(self, key):
		if key not in """:';"/""":
			self.newname += key

	def delete_char(self):
		self.newname = self.newname[:-1]

	def set_commands(self):
		self.commands['KEY_ENTER'] = self.confirm_rename
		self.commands['KEY_BACKSPACE'] = self.delete_char
		self.commands['KEY_ESCAPE'] = self.back_to_main
		# Note: 'b' is not included here as a command key
		# because it is used in renaming the file.

	def back_to_main(self):
		self.newname = ''
		self.fileman.mode = self.fileman.modes.main

	def confirm_rename(self):
		man = self.fileman
		if not os.access(man.pwd, os.X_OK | os.W_OK):
			raise PermissionError('Cannot write to this directory')
		oldfile = man.current_file
		try:
			shutil.move(oldfile.filename, self.newname)
		except PermissionError:
			raise PermissionError('Invalid permissions')

		man.collect_dir()
		new_index = man.find_filelist_index_by_name(self.newname)
		man.set_current_file(new_index)
		self.back_to_main()

	def render(self):
		man = self.fileman
		term = self.fileman.term

		content = '\n Rename to:\n  ' + self.newname + UTF.block.full

		mywin = Window(term, self.x, self.y, border=' '*8)
		mywin.content = content
		mywin.render()


#-==@class
class HelpText(FileManagerMode):
	#-== When the /H key is pressed,
	# this mode activates to display the help text.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# Any key             | Close the help text window

	HELP_TEXT = '''
         Welcome to FILER

 [Up/Down Arrows]  Navigate list
      ["] and [?]  Jump up/down list (20 lines)
     [Left Arrow]  Go to parent directory
    [Right Arrow]  Go into directory
          [Enter]  Actions menu/Select action
     [B] or [Esc]  Go back
          [Space]  Select/deselect file
              [A]  Select/delect all
              [.]  Show/hide hidden files
              [D]  Show/hide directories
              [F]  Show/hide non-directory files
              [H]  Show help (this window)
              [Q]  Quit'''

	def process_input(self, key):
		self.back_to_main()

	def back_to_main(self):
		self.fileman.mode = self.fileman.modes.main

	def render(self):
		term = self.fileman.term

		helpwin = Window(term, 0, 0, border='*'*8)
		helpwin.content = self.HELP_TEXT
		helpwin.render()


#-==@class
class FileManager:
	#-== The main class which runs the application loop (see the /run() method below).
	# @attributes
	# term:           the Blessed /Terminal object to control input/output
	# running:        a boolean which is set to /True if teh application loop is running
	# modes:          a /DotDict of /FileManagerMode objects, each keyed with a name
	# pwd:            the current absolute path of the running application
	# prev_pwd:       the previous /pwd of the running application
	# show_hidden_files: a boolean indicating if hidden files should be displayed
	# show_files:     a boolean indicating if non-directory files should be displayed
	# show_directories: a boolean indicating if directories should be displayed
	# filelist:       a list of /ScanDirHelper objects, each describing a file in the directory
	# selected_files: the list of selected files; each is a /ScanDirHelper object
	# total_files:    total count of all files within the current directory
	# displayed_files: count of files actually displayed in the window
	# current_dir:    the name of the current directory
	# current_index:  the index of the file the cursor is currently on
	# current_file:   the /ScanDirHelper object referencing the file the cursor is on
	# mode:           the /FileManagerMode currently executing in the application loop

	# currently unused, potentially add ability
	# to see/use navigation history?
	MAX_PATH_HISTORY = 20

	#-==@method
	def __init__(self, term, pwd):
		#-== Creates an instance of the FILER application.
		# @params
		# term: a Blessed /Terminal object to control input and output
		# pwd:  the absolute path to start the application within

		self.term = term
		self.show_hidden_files = False
		self.show_files = True
		self.show_directories = True

		self.pwd = pwd
		self.prev_pwd = pwd
		self.filelist = []
		self.selected_files = []
		self.total_files = 0
		self.displayed_files = 0
		self.current_dir = None
		self.current_index = None
		self.current_file = None

		self.goto_dir(pwd)
		self.running = False
		self.modes = DotDict(
			main = FileListMode(self, 'main'),
			actions = ActionMenu(self, 'actions',
							x=FILELIST_WIDTH,
							y=FILE_DETAILS_HEIGHT+1),
			help= HelpText(self, 'help'),
			rename= RenameMode(self, 'rename',
								x=FILELIST_WIDTH,
								y=FILE_DETAILS_HEIGHT+1),
		)
		self.mode = self.modes.main

	#-==@method
	def find_filelist_index_by_name(self, name):
		#-== @params
		# name: the filename of the file
		# @returns
		# The integer index of the file within /self.filelist .
		# Returns -1 if the /name was not found.

		i = 0
		for file in self.filelist:
			if file.filename == name:
				return i
			i += 1
		return -1

	#-==@method
	def is_selected(self, checkfile):
		#-== @params
		# checkfile: a /ScanDirHelper object
		# @returns
		# A boolean indicating if the file is in /self.selected_files

		for file in self.selected_files:
			if file.inode == checkfile.inode:
				return True
		return False

	#-==@method
	def goto_dir(self, path, set_current_by_name=None, record_history=True):
		#-== Changes the current directory and adjusts
		# all relevant information within /FileManager .
		# @params
		# path: the path to change to
		# set_current_by_name: a name to use when setting the current index
		# record_history: not currently used

		try:
			os.chdir(path)
			self.collect_dir()
			self.pwd = os.getcwd()
			self.current_dir = os.path.basename(self.pwd)
			set_current_index = 0
			if set_current_by_name is not None:
				set_current_index = self.find_filelist_index_by_name(set_current_by_name)
			if set_current_index < 0:
				set_current_index = 0
			self.set_current_file(set_current_index)
		except PermissionError:
			self.goto_dir(self.prev_pwd, set_current_by_name=os.path.basename(path))
			raise PermissionError('Invalid permissions')

	#-==@method
	def quit(self):
		#-== Ends the application loop

		self.running = False

	#-==@method
	def set_current_file(self, index):
		#-== Changes the current file the cursor is on and adjusts
		# all relevant information within /FileManager .

		if index < 0:
			index = 0
		if len(self.filelist) > index:
			self.current_index = index
			self.current_file = self.filelist[index]
		else:
			self.current_index = None
			self.current_file = None

	#-==@method
	def run(self):
		#-== This is the main "application loop" of FILER.
		# This method activates the /Terminal and begins the application loop.
		# Each iteration will display the mode from /self.mode (via /mode.render() )
		# and then wait until an input is received from teh user (via /mode.process_input() ).
		# If /self.running is set to /False , the application will terminate the loop.

		with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
			self.running = True
			while self.running:
				try:
					self.prev_pwd = self.pwd
					self.render()
					c = self.term.inkey()
					self.process_input(c)
				except PermissionError as exc:
					self.render_error(str(exc))
		return self.pwd

	#-==@method
	def collect_dir(self):
		#-== Compiles the list of files in the current directory
		# as a list of /ScanDirHelper objects and stores it in /self.filelist ,
		# then adjusts all relevant information.

		self.total_files = 0
		self.displayed_files = 0
		self.filelist = []
		with os.scandir() as dirlist:
			for file in dirlist:
				self.total_files += 1
				entry = ScanDirHelper(file)
				if entry.is_hidden_file() and not self.show_hidden_files:
					pass
				elif entry.filetype in [FileType.DIR] and not self.show_directories:
					pass
				elif entry.filetype not in [FileType.DIR] and not self.show_files:
					pass
				else:
					self.displayed_files += 1
					self.filelist.append(entry)
		self.filelist.sort(key=lambda x: x.filename.lower())

	#-==@method
	def select_current(self):
		#-== Adds the file the cursor is pointing to
		# (as indicated by /self.current_file ) to /self.selected_files .

		if self.current_file is not None:
			self.selected_files.append(self.current_file)

	#-==@method
	def deselect_current(self):
		#-== Removes the file the cursor is pointing to
		# (as indicated by /self.current_file ) from /self.selected_files .

		if self.current_file is not None:
			self.selected_files.remove(self.current_file)

	#-==@method
	def render(self):
		#-== Runs the /render() method of the current mode
		# (via /self.mode ), and flushes the terminal output.

		self.mode.render()
		flush()

	#-==@method
	def render_error(self, msg):
		#-== Renders an error message in the middle of the terminal.
		# You can press any key to dismiss the error message.

		vcenter = int(self.term.height / 2)
		echo(self.term.move_xy(0, vcenter))
		echo(self.term.black_on_bright_red)
		echo(self.term.center('Error: '+msg+', press any key'))
		echo(self.term.normal)
		flush()
		c = self.term.inkey()

	#-==@method
	def process_input(self, key):
		#-== Runs the /process_input() method of
		# the current mode (via /self.mode )

		self.mode.process_input(key)



#-==@h1 Script Entrypoint

#-==@method
def main():
	#-== The main entrypoint when executing this module as an application.
	# This starts the Blessed /Terminal object and then passes it to a
	# /FilemManager object which will run the application.
	# When the application exits, the directory it was within will be printed
	# as terminal output as well as to a file ( /.cxfilerexit ) within
	# the user's /HOME directory.
	# This file can be used to recall where FILER was when it exited.
	# The shell command below will change directory to where
	# FILER was pointed when it exited.
	#@codeblock
	# cd $(cat ~/.cxfilerexit)
	#@codeblockend

	home = os.environ['HOME']
	term = Terminal()
	pwd = os.getcwd()
	fileman = FileManager(term, pwd)
	# for file in fileman.filelist:
	# 	print(file)
	exit_dir = fileman.run()
	with open(os.path.join(home, '.cxfilerexit'), 'w') as filerout:
		filerout.write(exit_dir)
	print(exit_dir)

if __name__ == '__main__':
	main()
