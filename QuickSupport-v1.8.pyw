
#######################################################
# QuickSupport-v1.8.py - January 2026 - SRR           #
# Editor for taking notes of incomming phone support. #
#######################################################

#-| import statements |-#
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from PIL import Image
import customtkinter
import datetime
import ctypes
import time
import os

# sets DPI awareness (increases pixel density by increasing scaling)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

#-| global variables |-#
app_info = 'QuickSupport 1.8' # app info string
filepath = os.getcwd() # initiate current working directory
windows_path = os.path.basename(os.path.dirname(__file__))
cursor_pos = 0.0 # initiate cursor position
time_of_day = datetime.datetime.now() # initiate current local time
os_user = os.getlogin() # gets name of logged in user on MS Windows
big_logo_image = customtkinter.CTkImage(dark_image = Image.open('images\\logo-phone.png'), size = (125, 125)) # load bigger image file
small_logo_image = customtkinter.CTkImage(dark_image = Image.open('images\\logo-phone.png'), size = (50, 50)) # load smaller image file
search_list = list()
search_string = " "

###-| functions |-###

#-| main function |-#
def main():
    
    # update cursor position and time every second
    update_status()
    
    # save current working file every three minutes
    auto_save()

#-| update value of variables |-#
def update_status():
    
    # get cursor position
    global cursor_pos
    cursor_pos = float(text_field.index(INSERT))
    
    # get current local time
    global time_of_day
    time_of_day = datetime.datetime.now()
    
    # run repeatedly after set time
    window.after(1000, update_status)

#-| new file |-#
def new_file(event = False):
    
    # check for characters in text box and if file is saved
    if len(text_field.get('1.0', 'end-1c')) != 0 and window.title() == f'{app_info} - Unnamed':
        save_file()
        text_field.delete(1.0, END) # clear text box
        window.title(f'{app_info} - Unnamed') # reset window title
    else:
        text_field.delete(1.0, END) # clear text box
        window.title(f'{app_info} - Unnamed') # reset window title

#-| open file |-#
def open_file(event = False):
    
    global cursor_pos
    
    # open file dialog
    global filepath
    filepath = fd.askopenfilename(filetypes = [('Text File', '*.txt'), ('All Files', '*.*')])
    if not filepath: # abort if file dialog canceled
        return

    # clear text box before reading file content
    text_field.delete(END)

    # reading file content into text box
    with open(filepath, 'r') as input_file:
        text = input_file.read()
        text_field.insert(0.0, text)
    
    text_field.yview(END) # scrolls to end of text box 
    text_field.delete(text_field.index(INSERT), END) # leaves an empty line at end
    text_field.focus() # sets focus to text box
    
    # set window title with file path to correspond
    display_path = filepath.replace("/", "\\")
    window.title(f'{app_info} - {display_path}')

#-| save file |-#
def save_file(event = False):

    # check for characters in text box
    if len(text_field.get('1.0', 'end-1c')) == 0 and window.title() == f'{app_info} - Unnamed':
        mb.showwarning(f'{app_info}', 'Empty Document!') # message box if empty file
    
    # check for characters in text box
    elif len(text_field.get('1.0', 'end-1c')) != 0 and window.title() == f'{app_info} - Unnamed':  
        
        # open file dialog
        global filepath
        filepath = fd.asksaveasfilename(defaultextension = 'txt', filetypes = [('Texst File', '*.txt'), ('All Files', '*.*')])
        if not filepath: # abort if file dialog canceled
            return
        
        # open file in write mode
        with open(filepath, 'w') as output_file:
            output_file.write(text_field.get(0.0, END)) # write text box content to file
            output_file.close() # close file
        
        # set window title with file path to correspond
            display_path = filepath.replace("/", "\\")
            window.title(f'{app_info} - {display_path}')
    
    else:
        save_current()

#-| save open file |-#
def save_current():
    
    with open(filepath, 'w') as current_file:
        current_file.write(text_field.get(1.0, END)) # write text box content to file
        current_file.close() # close file
    
        # set window title with file path to correspond and add [Lagret] message
        display_path = filepath.replace("/", "\\")
        window.title(f'{app_info} - {display_path} [Saved]')
        time.sleep(3) # halt before editing window title once more
        
        # set window title with file path to correspond and remove [Lagret] message
        window.title(f'{app_info} - {display_path}')

#-| save file as |-#
def save_as():
        
        # open file dialog
        global filepath
        filepath = fd.asksaveasfilename(defaultextension = 'txt', filetypes = [('Text File', '*.txt'), ('All Files', '*.*')])
        if not filepath: # abort if file dialog canceled
            return
        
        # open file in write mode
        with open(filepath, 'w') as output_file:
            output_file.write(text_field.get(0.0, END)) # write text box content to file
            output_file.close() # close file
        
        # set window title with file path to correspond
            display_path = filepath.replace("/", "\\")
            window.title(f'{app_info} - {display_path}')

#-| auto save open file |-#
def auto_save():
    
    # check for characters in text box and if file is saved
    if len(text_field.get('1.0', 'end-1c')) != 0 and window.title() != f'{app_info} - Unnamed':
        save_current()
    
    # run function repeatedly after set time
    window.after(130000, auto_save)

#-| quit app |-#
def quit_app(event = False):
    
    # check for characters in text box and if file is saved
    if len(text_field.get('1.0', 'end-1c')) != 0 and window.title() == f'{app_info} - Unnamed':
        save_file() # save file before terminating
        time.sleep(1.5) # halt before termination
        window.destroy() # terminate
    else:
        exit() # terminate app and scheduled jobs
 
 #-| insert boilerplate |-#
def boilerplate(event = False):
    global cursor_pos
    global time_of_day
    text_field.insert(END, f'INCOMING CALL: {time_of_day.strftime("%d.%m.%Y %H:%M")}\n' + \
                           '-' * 135 + '\nCaller: \n\n\nCompany/Municipality/Institution: \n\n\n' + \
                           'Phone: \n\n\nE-mail: \n\n\nTicket: \n\n\n' + \
                           'Department/Product: \n\n\nProblem: \n\n\nConclusion: \n\n\n' + \
                           '=' * 77 + '\n')

    # cursor placement and view in text box
    text_field.mark_set(INSERT, END) # cursor moved to end of schema after insert
    cursor_pos = float(text_field.index(INSERT)) - 24.0 # set value to first label in schema
    text_field.mark_set(INSERT, cursor_pos) # move cursor to first label in schema
    text_field.yview(END) # scrolls down in text box

#-| tabulate vertically |-#
def vertical_tab_up(event = False):
    global cursor_pos
    cursor_pos = float(text_field.index(INSERT)) - 3.0 # set value for movement
    text_field.mark_set(INSERT, cursor_pos) # move cursor up in schema

def vertical_tab_dwn(event = False):
    global cursor_pos
    cursor_pos = float(text_field.index(INSERT)) + 3.0 # set value for movement
    text_field.mark_set(INSERT, cursor_pos) # move cursor down in schema

#-| confirmation text |-#
def status_confirm(event = False):
    global cursor_pos
    # insert confirmation text in schema
    text_field.insert(cursor_pos, '\n' + '-' * 135 + '\n' '*** STATUS: COMPLETED ***')
    #cursor_pos = float(text_field.index(INSERT)) - 24.0 # set value for movement
    text_field.mark_set(INSERT, END) # move cursor to end of schema

#-| text search |-#
def text_search(event = False):
    global search_list
    global search_string
    
    text_field.focus_set() # text field set focus
    search_string = search_field.get() # get search string from search field
    
    if search_string:
        if search_list == []:
            idx = '1.0'
        else: idx = search_list[-1]
    
        idx = text_field.search(search_string, idx, nocase = 1, stopindex = END)
        lastidx = '%s+%dc' % (idx, len(search_string))
        
        try:
            text_field.tag_remove(SEL, 1.0,lastidx)
        except:
            pass
        
        try:
            text_field.tag_add(SEL, idx, lastidx)
            counter_list = []
            counter_list = str(idx).split('.')      
            text_field.mark_set("insert", "%d.%d" % (float(int(counter_list[0])), float(int(counter_list[1]))))
            text_field.see(float(int(counter_list[0])))
            search_list.append(lastidx)
        except:
            mb.showinfo(f'{app_info}', f'Search on text string "{search_string}" completed\n with ' + str(len(search_list)) + ' occurrences.')
            search_list.clear()
            search_field.delete(0, END) # delete search field content
        
#-| search focus |-#
def search_focus(self):
    search_field.focus_set() # search field set focus
    search_field.delete(0, END) # delete search field content

#-| editor focus |-#
def editor_focus(self):
    text_field.focus_set() # text field set focus

#-| about message box |-#
def about():
    
    # text displayed to end user
    text = 'Detailed notetaking of incoming support calls\n\n \
    ------------\n\n \
    Copyleft - Bored Support-technitian'

    # window parameters
    about_box = Toplevel(window)
    about_box.title(f'{app_info} - About')
    about_box_width = 440
    about_box_height = 219

    # finding center of screen and positioning
    screenX = int(screen_width / 2 - about_box_width / 2)
    screenY = int(screen_height / 2 - about_box_height / 2)
    about_box.geometry(f'{about_box_width}x{about_box_height}+{screenX}+{screenY}')

    about_box.resizable(0,0) # disabling abillity to resize
    about_box.focus() # sets focus on window
    logo = customtkinter.CTkLabel(about_box, image = small_logo_image, text = '') # loads logo image
    logo.pack(padx = 10, pady = 15)
    
    message_text = customtkinter.CTkLabel(about_box, text = f'{text}', font = customtkinter.CTkFont(size = 12, weight = 'normal'), justify = 'center')
    message_text.pack(pady = 25, padx = 50)

#-| keys message box |-#
def keys(event = False):
    
    # text displayed to end user
    text = '     Control + N: New\n \
    Control + O: Open\n \
    Control + S: Save\n \
    Control + Q: Quit\n\n \
    \t       ------------\n\n \
    Alt + E: Fokus document\n \
    Alt + T: Fokus search\n \
    Alt + S: Search document\n \
    Alt + M: Insert template\n \
    Alt + N: Next field\n \
    Alt + G: Last field\n \
    Alt + B: Insert confirmation'
    
    # window parameters
    keys_box = Toplevel(window)
    keys_box.title(f'{app_info} - Shortcut Keys')
    keys_box_width = 440
    keys_box_height = 330
    
    # finding center of screen and positioning window
    screenX = int(screen_width / 2 - keys_box_width / 2)
    screenY = int(screen_height / 2 - keys_box_height / 2)
    keys_box.geometry(f'{keys_box_width}x{keys_box_height}+{screenX}+{screenY}')
    
    keys_box.resizable(1,1) # disabling abillity to resize
    keys_box.focus() # sets focus on window
    logo = customtkinter.CTkLabel(keys_box, image = small_logo_image, text = '') # loads logo image
    logo.pack(pady = 15, padx = 10)
    
    message_text = customtkinter.CTkLabel(keys_box, text = f'{text}', font = customtkinter.CTkFont(size = 12, weight = 'normal'), justify = 'left')
    message_text.pack(pady = 25, padx = 50)

#-| end functions |-#

#-| grafical user interface |-#

#-| theme settings |-#
customtkinter.set_appearance_mode("Light")  # available modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # available themes: "blue" (standard), "green", "dark-blue"

#-| main window |-#
window = customtkinter.CTk()
window_width = 800 # main window startup-width in pixels
window_height = 730 # main window startup-height in pixels
window.minsize(800, 730) # minimum main window size when resize enabled
window.resizable(0,0) # disabling abillity to resize main window
window.title(f'{app_info} - Unnamed')

#-| getting screen dimensions |-#
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#-| finding center of screen and positioning main window |-#
screenX = int(screen_width / 2 - window_width / 2)
screenY = int(screen_height / 2 - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{screenX}+{screenY}')

#-| layout of GUI elements |-#
window.grid_columnconfigure(0, weight = 0)
window.grid_columnconfigure(1, weight = 1)
window.grid_rowconfigure(0, weight = 1)

#-| creating menubar |-#
menubar = Menu(window)
window.config(menu = menubar)

file_menu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label="File", menu = file_menu)
file_menu.add_command(label="New                      Ctrl+N", command = new_file)
file_menu.add_command(label="Open...                  Ctrl+O", command = open_file)
file_menu.add_command(label="Save                       Ctrl+S", command = save_file)
file_menu.add_command(label="Save As...                ", command = save_as)
file_menu.add_separator()
file_menu.add_command(label="Quit                       Ctrl+Q", command = quit_app)

help_menu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Help", menu = help_menu)
help_menu.add_command(label="Shortcut Keys...               ", command = keys)
help_menu.add_command(label="About...", command = about)

#-| sidebar |-#
sidebar = customtkinter.CTkFrame(window, corner_radius = 0)
sidebar.grid(row = 0, column = 0, columnspan = 1, sticky = 'nsw')
sidebar.grid_columnconfigure(0, weight = 1)
sidebar.grid_rowconfigure(0, weight = 1)
sidebar.grid_rowconfigure(1, weight = 1)

#-| frame for search elements |-#
sidebar_frame_search = customtkinter.CTkFrame(sidebar, corner_radius = 15)
sidebar_frame_search.grid(row = 1, column = 1, padx = 25, pady = (10, 220), sticky = 'sew')

#-| frame for schema elements |-#
sidebar_frame_edit = customtkinter.CTkFrame(sidebar, corner_radius = 15)
sidebar_frame_edit.grid(row = 1, column = 1, padx = 25, pady = (10, 40), sticky = 'sew')

#-| logo and text in sidebar |-#
intro_logo = customtkinter.CTkLabel(sidebar, image = big_logo_image, text = '')
intro_logo.grid(row = 0, column = 1, columnspan = 2, padx = 10, pady = (70, 50), sticky = 'new')
intro_text = customtkinter.CTkLabel(sidebar, text = 'QuickSupport\n------------\nMake notes of\nincoming support calls', font = customtkinter.CTkFont(size = 12, weight = 'normal'))
intro_text.grid(row = 0, column = 1, columnspan = 2, padx = 10, pady = (200, 5), sticky = 'new')

#-| search field |-#
search_field = customtkinter.CTkEntry(sidebar_frame_search)
search_field.grid(row = 1, column = 0, columnspan = 1, padx = (10, 10), pady = (10, 5), sticky = 'esw')

#-| search button |-#
search_button = customtkinter.CTkButton(sidebar_frame_search, text = 'Search', border_width = 1, command = text_search)
search_button.grid(row = 2, column = 0, columnspan = 1, padx = (10, 10), pady = (5, 10), sticky = 'esw')

#-| insert button |-#
insert_button = customtkinter.CTkButton(sidebar_frame_edit, text = 'Template', border_width = 1, command = boilerplate)
insert_button.grid(row = 3, column = 0, columnspan = 1, padx = (10, 10), pady = (10, 5), sticky = 'esw')

#-| next button |-#
next_button = customtkinter.CTkButton(sidebar_frame_edit, text = 'Next Field', border_width = 1, command = vertical_tab_dwn)
next_button.grid(row = 4, column = 0, columnspan = 1, padx = (10, 10), pady = (5, 5), sticky = 'esw')

#-| back button |-#
back_button = customtkinter.CTkButton(sidebar_frame_edit, text = 'Last Field', border_width = 1, command = vertical_tab_up)
back_button.grid(row = 5, column = 0, columnspan = 1, padx = (10, 10), pady = (5, 5), sticky = 'esw')

#-| confirmation button |-#
insert_button = customtkinter.CTkButton(sidebar_frame_edit, text = 'Completed', border_width = 1, command = status_confirm)
insert_button.grid(row = 6, column = 0, columnspan = 1, padx = (10, 10), pady = (5, 10), sticky = 'esw')

#-| text field |-#
text_field = customtkinter.CTkTextbox(window)
text_field.grid(row = 0, column = 1, columnspan = 4, padx = (10, 10), pady = (10, 10), sticky = 'nesw')
text_field.configure(wrap = 'word')
text_field.focus_set()

#-| end grafical user interface |-# 

#-| hotkey bindings |-#

# text field focus
window.bind('<Alt-e>', editor_focus)

# search field focus
window.bind('<Alt-t>', search_focus)

# execute search
window.bind('<Alt-s>', text_search)

# insert schema
window.bind('<Alt-m>', boilerplate)

# insert status confirmation
window.bind('<Alt-b>', status_confirm)

# tabulate cursor downwards
window.bind('<Alt-n>', vertical_tab_dwn)

# tabulate cursor upwards
window.bind('<Alt-g>', vertical_tab_up)

# new file
window.bind('<Control-n>', new_file)

# open file
window.bind('<Control-o>', open_file)

# save file
window.bind('<Control-s>', save_file)

# quit app
window.bind('<Control-q>', quit_app)

#-| end hotkey bindings |-#

#-| call main function on startup |-#
main()

#-| finalize grafical user interface |-#
window.mainloop()

