#!/usr/bin/env python3
# -*- coding:utf-8 -*-  
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import shlex
import subprocess
import argparse
import locale
import logging
import signal
import sys
import random
import time

from aiy.assistant.testGrpc import AssistantServiceClientWithLed
from aiy.board import Board, Led

CMD_SAY = 'jsay'
isPlaying = False

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def say(text):
    text = CMD_SAY + ' ' + text
    print(text)
    proc = subprocess.Popen(shlex.split(text))
    proc.communicate()
    return

def interval():
    sleepTime = random.uniform(1.5, 10)
    logging.info(sleepTime)
    time.sleep(sleepTime)

def aizuchi():
    aizuchi_list = ['うん', 'うんうん', 'へー', 'ふーん', 'うん、うん']
    text = random.choice(aizuchi_list)
    say(text)
    return

def update_led(board, state, brightness):
    board.led.state = state
    board.led.brightness = brightness

def stop():
    isPlaying = False
    logging.info(isPlaying)

def main():
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    parser.add_argument('--volume', type=volume, default=100)
    args = parser.parse_args()

    global isPlaying

    with Board() as board:
        assistant = AssistantServiceClientWithLed(board=board,
                                                  volume_percentage=args.volume,
                                                  language_code=args.language)
        while True:
            if isPlaying:
                update_led(board, Led.ON, 1.0)
                logging.info('Conversation started!')
                #assistant.detectSpeaking()
                interval()
                aizuchi()
                # board.button.when_pressed = isPlaying = False
            else:
                update_led(board, Led.ON, 0.1)
                logging.info('Press button to start conversation...')
                board.button.wait_for_press()
                isPlaying = True

if __name__ == '__main__':
    main()
