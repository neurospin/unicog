#! /usr/bin/env python
# Time-stamp: <2018-03-28 16:31:03 cp983411>

import sys
import io
import os.path as op
import argparse
import csv

import expyriment.control
from expyriment import stimuli
from expyriment.misc import Clock

from queue import PriorityQueue

#LAUNCH WITH
#python localizer_standard.py --background-color 0 0 0 --text-color 250 250 250 --rsvp-display-time=250 --rsvp-display-isi=100 --picture-display-time=200 --picture-isi=0 --fs_delay_time=100 --stim-dir stim_files --splash ./instructions_localizer_time.csv 


# constants (which can be modified by optional command line arguments)
WORD_DURATION = 450
WORD_ISI = 200
FS_DELAY = 100
PICTURE_DURATION = 1000
PICTURE_ISI = 0
TEXT_DURATION = 3000
TOTAL_EXPE_DURATION = -1 # time in millisec
BACKGROUND_COLOR=(240, 240, 240)
TEXT_FONT = 'TITUSCBZ.TTF'
TEXT_SIZE = 48
TEXT_COLOR = (0, 0, 0)
WINDOW_SIZE = (1220, 700)
#WINDOW_SIZE = (1280, 1028)


# process command line options

parser = argparse.ArgumentParser()
parser.add_argument("--splash", help="displays a picture (e.g. containing instructions) before starting the experiment")

parser.add_argument('--csv_files',
                    nargs='+',
                    action="append",
                    default=[])
parser.add_argument('--total-duration',
                    type=int,
                    default=-1,
                    help="time to wait for after the end of the stimuli stream")
parser.add_argument("--fs_delay_time",
                    type=int,
                    default=FS_DELAY,
                    help="time between the end of blanck screen and the beginning of fixation cross")
parser.add_argument("--rsvp-display-time",
                    type=int,
                    default=WORD_DURATION,
                    help="set the duration of display of single words \
                          in rsvp stimuli")
parser.add_argument("--rsvp-display-isi",
                    type=int,
                    default=WORD_ISI,
                    help="set the duration of display of single words \
                          in rsvp stimuli")
parser.add_argument("--picture-display-time",
                    type=int,
                    default=PICTURE_DURATION,
                    help="set the duration of display of pictures")
parser.add_argument("--picture-isi",
                    type=int,
                    default=PICTURE_ISI,
                    help="set the ISI between pictures in  pictseq sequence")
parser.add_argument("--text-display-time",
                    type=int,
                    default=TEXT_DURATION,
                    help="set the duration of display of text")
parser.add_argument("--text-font",
                    type=str,
                    default=TEXT_FONT,
                    help="set the font for text stimuli")
parser.add_argument("--text-size",
                    type=int,
                    default=TEXT_SIZE,
                    help="set the vertical size of text stimuli")
parser.add_argument("--text-color",
                    nargs='+',
                    type=int,
                    default=TEXT_COLOR,
                    help="set the font for text stimuli")
parser.add_argument("--background-color",
                    nargs='+',
                    type=int,
                    default=BACKGROUND_COLOR,
                    help="set the background color")
parser.add_argument("--window-size",
                    nargs='+',
                    type=int,
                    default=WINDOW_SIZE,
                    help="in window mode, sets the window size")
parser.add_argument("--stim-dir",
                    type=str,
                    default='STIM_DIR',
                    help="directory in which stim are available")

args = parser.parse_args()
splash_screen = args.splash
FS_DELAY = args.fs_delay_time
WORD_DURATION = args.rsvp_display_time
PICTURE_DURATION = args.picture_display_time
PICTURE_ISI = args.picture_isi
TEXT_DURATION = args.text_display_time
TEXT_SIZE = args.text_size
TEXT_COLOR = tuple(args.text_color)
TEXT_FONT = args.text_font
BACKGROUND_COLOR = tuple(args.background_color)
WINDOW_SIZE = tuple(args.window_size)
TOTAL_EXPE_DURATION = args.total_duration
WORD_ISI = args.rsvp_display_isi
STIM_DIR = args.stim_dir

#csv_files = args.csv_files[0]

expyriment.control.defaults.window_mode=True
expyriment.control.defaults.window_size = WINDOW_SIZE
expyriment.design.defaults.experiment_background_colour = BACKGROUND_COLOR

exp = expyriment.design.Experiment(name="Localizer",
                                   background_colour=BACKGROUND_COLOR,
                                   foreground_colour=TEXT_COLOR,
                                   text_size=TEXT_SIZE,
                                   text_font=TEXT_FONT)
#expyriment.control.defaults.open_gl=1

expyriment.misc.add_fonts('fonts')

#%

expyriment.control.initialize(exp)

#exp.background_colour = BACKGROUND_COLOR
exp._screen_colour = BACKGROUND_COLOR
kb = expyriment.io.Keyboard()
bs = stimuli.BlankScreen(colour=BACKGROUND_COLOR)
fs = stimuli.FixCross(size=(25, 25), line_width=3, colour=TEXT_COLOR)

key_menu = ''

#DISPLAY MENU
def display_menu():
    menu = "Pour effectuer un calibrage, tapez (c) \n"\
            "Pour afficher les instructions, tapez (i) \n"\
            "Pour commencer l'enregistrement, tapez (e) \n"
    width_screen, height_screen =  exp.screen.size
    menu_localizer = stimuli.TextBox(menu, size=(int(width_screen/1.5), int(height_screen/1.5)),
                                      text_font=TEXT_FONT,
                                      text_size=TEXT_SIZE,
                                      text_colour=TEXT_COLOR,
                                      background_colour=BACKGROUND_COLOR)
    menu_localizer.present()
    return kb.wait_char(['c', 'i', 'e'])



key_click = display_menu()
key_menu = key_click[0]
print(key_click)
while (key_menu == 'c' or key_menu == 'i'):
    if key_menu == 'c' :
        calibrage = "Nous allons faire un calibrage"
        calibration = stimuli.TextLine(calibrage, text_font=TEXT_FONT,
                                              text_size=TEXT_SIZE,
                                              text_colour=TEXT_COLOR,
                                              background_colour=BACKGROUND_COLOR)
        calibration.present()
        exp.clock.wait(2000)
    elif key_menu == 'i' :
        if not (splash_screen is None):
            if op.splitext(splash_screen)[1] == '.csv':
                instructions = csv.reader(io.open(splash_screen, 'r', encoding='utf-8-sig'), delimiter='\t')
                for instruction_line in instructions:
                    instruction_duration, stype, instruction_line = instruction_line[0], instruction_line[1], instruction_line[2]
                    if stype == 'text':
                        instruction_line = instruction_line.replace('\BL', '\n')
                        width_screen, height_screen =  exp.screen.size
                        instruction = stimuli.TextBox(instruction_line, size=(int(width_screen/1.5), int(height_screen/1.5)),
                                                          text_font=TEXT_FONT,
                                                          text_size=TEXT_SIZE,
                                                          text_colour=TEXT_COLOR,
                                                          background_colour=BACKGROUND_COLOR)
                        instruction.preload()
                        instruction.present()
                        #exp.clock.wait(WORD_DURATION*10)
                        exp.clock.wait(int(instruction_duration))
                        #fs.present()
                        #exp.clock.wait(WORD_ISI*6)
                    elif stype == 'sound':
                        bp = op.dirname(splash_screen)
                        if not(STIM_DIR==''):
                            bp = op.join(bp, STIM_DIR)
                        print(op.join(bp, instruction_line))
                        instruction = stimuli.Audio(op.join(bp, instruction_line))
                        instruction.preload()
                        instruction.present()
                        fs.present()  
                        exp.clock.wait(int(instruction_duration))
            else:
                splashs = stimuli.Picture(splash_screen)
                splashs.present()
                kb.wait_char(' ')
    key_click = display_menu()
    key_menu = key_click[0]
if key_menu == 'e' :
    choix_session = "Choix de la session \n"\
            "Session 1, tapez (1) \n"\
            "Session 2, tapez (2) \n"\
            "Session 3, tapez (3) \n"\
            "Session 4, tapez (4) \n"
    width_screen, height_screen =  exp.screen.size
    choix_session = stimuli.TextBox(choix_session, size=(int(width_screen/1.5), int(height_screen/1.5)),
                                      text_font=TEXT_FONT,
                                      text_size=TEXT_SIZE,
                                      text_colour=TEXT_COLOR,
                                      background_colour=BACKGROUND_COLOR)
    choix_session.present()
    session = kb.wait_char(['1', '2', '3', '4'])
    if session[0] == '1' :
        csv_files = ['./session1_localizer_standard.csv']
    elif session[0] == '2' :
        csv_files = ['./session2_localizer_standard.csv']
    elif session[0] == '3' :
        csv_files = ['./session3_localizer_standard.csv']
    elif session[0] == '4' :
        csv_files = ['./session4_localizer_standard.csv']
        
    wm = stimuli.TextLine('Waiting for scanner sync (or press \'t\')',
                          text_font=TEXT_FONT,
                          text_size=TEXT_SIZE,
                          text_colour=TEXT_COLOR,
                          background_colour=BACKGROUND_COLOR)
    fs = stimuli.FixCross(size=(25, 25), line_width=3, colour=TEXT_COLOR)
    
    events = PriorityQueue()  # all stimuli will be queued here
    
    
    # load stimuli
    
    mapsounds = dict()
    mapspeech = dict()
    maptext = dict()
    mappictures = dict()
    mapvideos = dict()
    
    for listfile in csv_files:
        stimlist = csv.reader(io.open(listfile, 'r', encoding='utf-8-sig'), delimiter='\t')
        bp = op.dirname(listfile)
        if not(STIM_DIR==''):
            bp = op.join(bp, STIM_DIR)
        for row in stimlist:
            cond, onset, stype, f = row[0], int(row[1]), row[2], row[3]
            if stype == 'sound':
                if not f in mapsounds:
                    mapsounds[f] = stimuli.Audio(op.join(bp, f))
                    mapsounds[f].preload()
                events.put((onset, cond, 'sound', f, mapsounds[f]))
                events.put((onset + TEXT_DURATION, cond, 'blank', 'blank', fs))
            elif stype == 'picture':
                if not f in mappictures:
                    mappictures[f] = stimuli.Picture(op.join(bp, f))
                    mappictures[f].preload()
                events.put((onset, cond, 'picture', f, mappictures[f]))
                events.put((onset + PICTURE_DURATION, cond, 'blank', 'blank', bs))
            elif stype == 'video':
                if not f in mapvideos:
                    mapvideos[f] = stimuli.Video(op.join(bp, f))
                    mapvideos[f].preload()
                events.put((onset, cond, 'video', f, mapvideos[f]))
            elif stype == 'text':
                if not f in maptext:
                    maptext[f] = stimuli.TextLine(f,
                                                  text_font=TEXT_FONT,
                                                  text_size=TEXT_SIZE,
                                                  text_colour=TEXT_COLOR,
                                                  background_colour=BACKGROUND_COLOR)
                    maptext[f].preload()
                events.put((onset, cond, 'text', f, maptext[f]))
                events.put((onset + TEXT_DURATION, cond, 'blank', 'blank', fs))
            elif stype == 'rsvp':
                for i, w in enumerate(f.split(',')):
                    if not w in maptext:
                        maptext[w] = stimuli.TextLine(w,
                                                      text_font=TEXT_FONT,
                                                      text_size=TEXT_SIZE,
                                                      text_colour=TEXT_COLOR,
                                                      background_colour=BACKGROUND_COLOR)
                        maptext[w].preload()
                    events.put((onset + i * (WORD_DURATION + WORD_ISI), cond, 'text', w, maptext[w]))
                    if not (WORD_ISI == 0):
                        events.put((onset + i * (WORD_DURATION + WORD_ISI) + WORD_DURATION, cond, 'blank', 'blank', bs))
                if WORD_ISI == 0:
                    events.put((onset + i * (WORD_DURATION + WORD_ISI) + WORD_DURATION, cond, 'blank', 'blank', bs))
                events.put((onset + i * (WORD_DURATION + WORD_ISI) + WORD_DURATION + FS_DELAY , cond, 'fs', 'fs', fs))
            elif stype == 'pictseq':
                for i, p in enumerate(f.split(',')):
                    if not p in mappictures:
                        mappictures[p] = stimuli.Picture(op.join(bp, p))
                        mappictures[p].preload()
                    events.put((onset + i * (PICTURE_DURATION + PICTURE_ISI), cond, 'picture', p, mappictures[p]))
                    if not (PICTURE_ISI == 0):
                        events.put((onset + i * (PICTURE_DURATION + PICTURE_ISI) + PICTURE_DURATION, cond, 'blank', 'blank', bs))
                if PICTURE_ISI == 0:  # then erase the last picture
                    events.put((onset + i * (PICTURE_DURATION + PICTURE_ISI) + PICTURE_DURATION, cond, 'blank', 'blank', bs))
                events.put((onset + i * (PICTURE_DURATION + PICTURE_ISI) + PICTURE_DURATION + FS_DELAY , cond, 'fs', 'fs', fs))
    
    exp.add_data_variable_names([ 'condition', 'time', 'stype', 'id', 'target_time'])
    
    #%
    expyriment.control.start()
    
    
    
    wm.present()
    kb.wait_char('t')  # wait for scanner TTL
    fs.present()  # clear screen, presenting fixation cross
    
    a = Clock()
    
    while not(events.empty()):
        onset, cond, stype, id, stim = events.get()
        print('{} to {}, id : {}'.format(cond, onset, id))
        while a.time < (onset - 10):
            a.wait(1)
            k = kb.check()
            if k is not None:
                exp.data.add([a.time, 'keypressed,{}'.format(k)])
        stim.present()
        exp.data.add(['{}'.format(cond), a.time, '{},{},{}'.format(stype, id, onset)])
    
        k = kb.check()
        if k is not None:
            exp.data.add([a.time, 'keypressed,{}'.format(k)])
    
    
    fs.present()
    
    if TOTAL_EXPE_DURATION != -1:
        while a.time < TOTAL_EXPE_DURATION:
            kb.process_control_keys()
            a.wait(100)
    
    expyriment.control.end('Merci !', 2000)
