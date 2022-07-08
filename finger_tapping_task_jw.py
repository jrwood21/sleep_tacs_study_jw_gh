"""
Title: Explicit finger tapping sequence learning task [replication of Walker et al. 2002]
Author: Julia Wood, the University of Queensland, Australia
Code adapted from Tom Hardwicke's finger tapping task code: https://github.com/TomHardwicke/finger-tapping-task
Developed in Psychopy v2022.1.1
See my GitHub for further details: https://github.com/jrwood21
"""
import time
import pandas as pd
import numpy as np
import sys
import os
from psychopy import visual, event, core, gui, data
from pyglet.window import key
from num2words import num2words

os.chdir(os.path.abspath(''))  # change working directory to script directory
globalClock = core.Clock()  # create timer to track the time since experiment started

# define sequences for finger tapping task
targ_seq_1 = '41324'
targ_seq_2 = '42314'
prac_seq = '12344'

### set up some useful functions ###
# Function to save messages to a log file 
def saveToLog(logString, timeStamp=1):
    f = open(logFile, 'a')  # open our log file in append mode so don't overwrite with each new log
    f.write(logString)  # write the string they typed
    if timeStamp != 0:  # if timestamp has not been turned off
        f.write('// logged at %iseconds' % globalClock.getTime())  # write a timestamp (very coarse)
    f.write('\n')  # create new line
    f.close()  # close and "save" the log file

# An exit function to initiate if the 'end' key is pressed
def quitExp():
    if 'logFile' in globals():  # if a log file has been created
        saveToLog('User aborted experiment')
        saveToLog('..........................................', 0)
    if 'win' in globals():  # if a window has been created
        win.close()  # close the window
    core.quit()  # quit the program

# define function to check if filename exists, then create the next available version number
def uniq_path(path):
    fn, ext = os.path.splitext(path)
    counter = 2
    while os.path.exists(path):
        path = fn + "_" + str(counter) + ext
        counter += 1
    return path

# Finger tapping task function
def fingerTapping(n_trials, tap_targetSequence, sequenceType):
    ## Intro screen ##
    saveToLog('Presenting introduction screen') # save info to log
    win.setColor('#000000', colorSpace='hex')  # set background colour to black
    win.flip()  # display
    generalText.setText(
        'TASK INSTRUCTIONS\n\nPlace the fingers of your LEFT hand on the keys 1, 2, 3, and 4. You will be shown a sequence of 5 digits %(sequence)s, and the computer will start counting down until you start. \n\nOnce the countdown has completed and the screen turns green, type %(sequence)s over and over as QUICKLY and as ACCURATELY as possible. \n\nYou will have 30 seconds to type %(sequence)s as many times as possible. Stop when the screen turns red again. You will get 30 seconds to rest before the next trial. \n\nPress the spacebar when you are ready for the countdown to begin.' % {'sequence': tap_targetSequence})
    generalText.draw()
    win.flip()  # display
    event.waitKeys(keyList=["space"])  # wait for a spacebar press before continuing
    event.clearEvents()  # clear the event buffer

    win.flip()  # blank the screen first
    trials = range(1, n_trials + 1)
    saveToLog('Running finger tapping task. %i trials with target sequence %s' % (len(trials), tap_targetSequence))  # save info to log

    for thisTrial in trials: # begin rest block
        win.setColor('#ff0000', colorSpace='hex')  # set background colour to red
        win.flip()  # display
        if thisTrial == 1:  # if this is first trial
            restClock = core.CountdownTimer(10) # start timer counting down from 10
        else:  # for all other trials
            saveToLog('Resting')  # save info to log
            restClock = core.CountdownTimer(30)  # start timer counting down from 30
        sequenceText.setText(tap_targetSequence)  # set up sequence text
        sequenceText.setAutoDraw(True)  # display sequence text continuously
        timerText.setAutoDraw(True)  #  display timer text continuously
        win.flip() 
        while restClock.getTime() > 0:  # loop continues until trial timer ends
            count = restClock.getTime()  # get current time from clock
            timerText.setText(num2words(np.ceil(count)))  # set timer text to the current time
            win.flip()  # display timer text
            if event.getKeys(['end']):  # checks for the key 'end' on every refresh so user can quit at any point
                quitExp()  # initiate quit routine

        # begin tapping task
        saveToLog('Trial: %i' % thisTrial) # save info to log
        win.setColor('#89ba00', colorSpace='hex')  # set background colour to green
        win.flip()  # display the green background
        tap_stream = []  # clear previous sequence keypresses from the stream 
        event.clearEvents()  # this makes sure the key buffer is cleared, otherwise old key presses might be recorded
        trialClock = core.CountdownTimer(30)  # start timer counting down from 30
        timerText.setText('Tap as fast as you can!')  # set timer text to the current time
        win.flip()  # display the text

        k = 0  # set up marker index
        endTrial = False  # a trigger to end the trial when True (deployed when the timer runs out)
        while endTrial == False:  # while trigger has not been deployed
            # display incremental markers across the screen from left to right as the user presses accepted keys
            if k == 0:  # start at beginning of marker index
                # start markers incrementing from left to right and append key presses to tap_stream
                while k < len(listOfMarkers) - 1 and endTrial == False:  # until the markers reach the far side of the screen
                    if trialClock.getTime() <= 0:  # if timer has run out
                        endTrial = True  # deploy the trigger to end the trial
                        break  # and break out of this loop
                    elif event.getKeys(['end']):  # if user presses end key
                        if thisTrial == 1 and not metaData['practice mode']: # during trial 1: save partial data collected from trial 1
                            quit_dict = {'stream': [tap_stream],
                                         'trial': thisTrial}
                            quit_df = pd.DataFrame(quit_dict, index=[0])
                            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_quitExp_trial1' + '.csv'
                            if os.path.exists(fileName):
                                fileName = uniq_path(fileName)
                            quit_df.to_csv(fileName)
                            saveToLog('User pressed end key during trial 1. Experiment aborted with %s seconds of trial 1 remaining' % trialClock.getTime())
                            saveToLog('Trial 1 data saved with filename: %s' %fileName)
                        elif thisTrial > 1 and not metaData['practice mode']: # or during a later trial: save partial and complete trial data collected
                            quit_dict = {'stream': [tap_stream],
                                         'trial': thisTrial}
                            quit_df = pd.DataFrame(quit_dict, index=[0])
                            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_quitExp' + '.csv'
                            if os.path.exists(fileName):
                                fileName = uniq_path(fileName)
                            quit_df.to_csv(fileName)
                            saveToLog('User pressed end key during trial %s' % thisTrial)
                            saveToLog('Experiment aborted with %s seconds of this trial remaining' % trialClock.getTime())
                            saveToLog('Partial trial data saved with filename: %s' %fileName)
                            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_quitExp_trials' + '.csv'
                            if os.path.exists(fileName):
                                fileName = uniq_path(fileName)
                            store_out.to_csv(fileName)
                            saveToLog('Data from complete trials saved with filename: %s' %fileName)
                        quitExp()  # AND quit the program
                    elif event.getKeys('1'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        tap_stream.append(1)  # record the key press
                        k += 1  # move on to the next marker
                    elif event.getKeys('2'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        tap_stream.append(2)  # record the key press
                        k += 1  # move on to the next marker
                    elif event.getKeys('3'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        tap_stream.append(3)  # record the key press
                        k += 1  # move on to the next marker
                    elif event.getKeys('4'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        tap_stream.append(4)  # record the key press
                        k += 1  # move on to the next marker

            # start markers incrementing from right to left and append keypresses to tap_stream:
            elif k == len(listOfMarkers) - 1 and endTrial == False:
                while k > 0:
                    if trialClock.getTime() <= 0:  # if timer has run out
                        endTrial = True  # deploy the trigger to end the trial
                        break  # and break out of this loop
                    elif event.getKeys(['end']):   # if user presses end key
                        if thisTrial == 1 and not metaData['practice mode']: # during trial 1: save partial data collected from trial 1
                            quit_dict = {'stream': [tap_stream],
                                         'trial': thisTrial}
                            quit_df = pd.DataFrame(quit_dict, index=[0])
                            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_quitExp_trial1' + '.csv'
                            if os.path.exists(fileName):
                                fileName = uniq_path(fileName)
                            quit_df.to_csv(fileName)
                            saveToLog('User pressed end key during trial 1. Experiment aborted with %s seconds of trial 1 remaining' % trialClock.getTime())
                            saveToLog('Trial 1 data saved with filename: %s' %fileName)
                        elif thisTrial > 1 and not metaData['practice mode']: # or during a later trial: save partial and complete trial data collected
                            quit_dict = {'stream': [tap_stream],
                                         'trial': thisTrial}
                            quit_df = pd.DataFrame(quit_dict, index=[0])
                            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_quitExp' + '.csv'
                            if os.path.exists(fileName):
                                fileName = uniq_path(fileName)
                            quit_df.to_csv(fileName)
                            saveToLog('User pressed end key during trial %s' % thisTrial)
                            saveToLog('Experiment aborted with %s seconds of this trial remaining' % trialClock.getTime())
                            saveToLog('Partial trial data saved with filename: %s' %fileName)
                            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_quitExp_trials' + '.csv'
                            if os.path.exists(fileName):
                                fileName = uniq_path(fileName)
                            store_out.to_csv(fileName)
                            saveToLog('Data from complete trials saved with filename: %s' %fileName)
                        quitExp()  # AND quit the program
                    elif event.getKeys('1'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        tap_stream.append(1)  # record the key press
                        k -= 1  # move on to the next marker
                    elif event.getKeys('2'): #checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        tap_stream.append(2)  # record the key press
                        k -= 1  # move on to the next marker
                    elif event.getKeys('3'): #checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        tap_stream.append(3)  # record the key press
                        k -= 1  # move on to the next marker
                    elif event.getKeys('4'): #checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        tap_stream.append(4)  # record the key press
                        k -= 1  # move on to the next marker

        # turn off all markers during the rest block
        for marker in listOfMarkers:  # for each marker
            marker.setAutoDraw(False)  # turn off

        win.setColor('#ff0000', colorSpace='hex')  # set background colour to red
        win.flip()  # display red background

        output = patternDetect(stream_in=tap_stream, targetSequence_in=tap_targetSequence)  # run the pattern detector to calculate correct sequences, errors and accuracy
    
        #  gather all relevant data for this trial
        newRow = {'participant': metaData['participant'], 
                  'allocation': metaData['participant allocation'],
                  'session': metaData['session number'], 
                  'session_time': metaData['session time'],
                  'target_sequence': tap_targetSequence,
                  'sequence_type': sequenceType,
                  'trial': thisTrial, # record which trial number
                  'stream': [tap_stream], # stream of key presses entered by participant
                  'n_correct': output['n_correct']}
#                  'errors': output['errors'], # Unhash these lines if you want them to be reported in the csv output file.
#                  'accuracy': output['accuracy']}

        # store all trial data in df. Each trial is stored in a new row
        if thisTrial == 1:
            store_out = pd.DataFrame(newRow, index=[0])
        elif thisTrial > 1:
            store_out = store_out.append(newRow, ignore_index=True)

    # after all trials are complete:
    sequenceText.setAutoDraw(False)  # turn off the sequence text
    timerText.setAutoDraw(False)  # turn off the timer text
    win.flip()  # clear the display

    return store_out

# Function for analysing the response stream
def patternDetect(stream_in, targetSequence_in):
    # pre-load some variables
    det_targetSequence = list(map(int, list(targetSequence_in))) # convert target sequence to list of integers
    det_stream = list(stream_in) # convert stream of key presses to a list
    n_correct = float(0) # store for number of correct sequences per trial
    '''
    Define stores for error tracking. I did not use these metrics in my study design, but I have left them in the code, in case
    they are appropriate for other experimental designs. Redefine, remove or ignore them as necessary for your study design.
    '''
    contiguousError = 0 # store for cumulative errors
    errors = float(0) # store for errors
    # note that n_correct + errors = total sequences

    i = 0  # start pattern detection at first element of keypress stream:
    while i < len(det_stream):  # search through every item in stream
        # for all key presses up to the final 5 (or any other target sequence length)
        if i <= len(det_stream) - len(det_targetSequence):
            # for any value in the stream where it + the next 4 keypresses match the target sequence:
            if det_stream[i:(i + len(det_targetSequence))] == det_targetSequence:
                n_correct += 1  # record a correct pattern completed
                i += len(det_targetSequence)  # adjust position to skip forward by length of targetSequence

                # Then add any accumulated errors to the total error count and clear the contiguous error count
                if contiguousError >= 1:  # check if there are contiguous errors we have not yet accounted for
                    errors += 1 # add an error to the total count
                    contiguousError = 0 # reset contiguous error count

            # otherwise, if the next sequence length of items in the stream does not match the target sequence:
            elif det_stream[i:(i + len(det_targetSequence))] != det_targetSequence:
                contiguousError += 1  # record a 'contiguous error'
                i += 1  # adjust index forward by 1

                # when contiguous error count reaches 5 incorrect keypresses in a row (i.e., the correct sequence doesn't follow 5 keypresses in a row) 
                # OR if the final item of the stream does not match the target sequence:
                if contiguousError == 5 or i == len(det_stream):
                    errors += 1 # add an error to the total count
                    contiguousError = 0 # reset contiguous error count

        # now deal with last items of the stream (a special case, see 'method' above)
        else:
            # get last items
            lastItems = det_stream[i:]
            # get subset of target sequence of same length as last items
            sequenceSubset = det_targetSequence[:len(lastItems)]

            # Addition of PARTIAL correct sequences at end of stream:
            while lastItems != None:  # while there are additional items left to check
                if lastItems == sequenceSubset:  # if lastItems match target sequence subset
                    n_correct += float(len(lastItems)) / float(len(det_targetSequence))  # record fractional sequence

                    if contiguousError >= 1:  # check if there are errors we have not yet recorded
                        errors += 1  # add an error to total
                        contiguousError = 0  # reset contiguous error count
                    lastItems = None  # force failure of inner while loop by updating lastItems
                    i = len(det_stream)  # force failure of outer while loop by updating i
                else:  # if lastItems do not match target sequence
                    contiguousError += 1  # add 1 to contiguous error count

                    # when contiguous error count reaches 5 incorrect keypresses in a row or if this is final item
                    if contiguousError == 5 or len(lastItems) == 1:
                        errors += 1  # add an error to total
                        contiguousError = 0  # reset contiguous error count
                    if len(lastItems) == 1:  # if this is the final item
                        lastItems = None  # force failure of inner while loop by updating lastItems
                        i = len(det_stream)  # force failure of outer while loop by updating i
                    else:  # else if there are still items left to check
                        lastItems = lastItems[1:]  # drop the first item from lastItems
                        sequenceSubset = sequenceSubset[:-1]  # drop the last item from the sequence subset

    # integrity check
    if n_correct == 0:
        print('Issue with this stream - n_correct is zero')
        accuracy = float('nan')
    else:
        accuracy = 1 - errors / n_correct  # calculate accuracy 
        # NOTE: this accuracy definition matches Hardwicke et al. 2016. I did not use this metric in my study design, but I have
        # left the code in the script case it is suitable for other study designs. Remove, redefine or ignore as necessary.
        
    return {'n_correct': n_correct, 'errors': errors, 'accuracy': accuracy}

### Collect and store meta-data about the experiment session ###
expName = 'Explicit finger tapping sequence task'  # define experiment name
date = time.strftime("%d %b %Y %H:%M:%S", time.localtime())  # get date and time
metaData = {'participant': '',
            'session number': [1, 2],
            'session time': ['pm-a', 'pm-b', 'am'],
            'practice mode': False,
            'use automated counter-balancing': True,
            'researcher': 'JW',
            'location': '304, Seddon North, UQ, Brisbane'}  # set up info for infoBox gui
infoBox = gui.DlgFromDict(dictionary=metaData,
                          title=expName,
                          order=['participant', 'session number', 'session time',
                                 'practice mode','use automated counter-balancing'])  # display gui to get info from user
if not infoBox.OK:  # if user hit cancel
    quitExp()  # quit

# check if participant dir exists, and if not, create one:
if not os.path.isdir('data'):
    os.mkdir('data')
if not os.path.isdir('data' + os.path.sep + 'fingertapping'):
    os.mkdir('data' + os.path.sep + 'fingertapping')
p_dir = 'data' + os.path.sep + 'fingertapping' + os.path.sep + 'P' + str(metaData['participant'])
if not os.path.isdir(p_dir):
    os.mkdir(p_dir)

if not metaData['practice mode']:  # if this is not practice mode:
    if metaData['use automated counter-balancing']:  # and user has chosen to use automated counter-balancing:
        cb = {'participant allocation': ['AJX', 'AJY', 'AKX', 'AKY',
                                         'BJX', 'BJY', 'BKX', 'BKY']}  # set up info for infoBox gui
        infoBox = gui.DlgFromDict(dictionary=cb,
                                  title='Choose counter-balancing parameters')  # display gui to get info from user
        metaData.update({'participant allocation': cb['participant allocation']})
        if not infoBox.OK:  # if user hit cancel
            quitExp()  # quit
    
    elif not metaData['use automated counter-balancing']: # or if user has chosen to manually select sequence type:
        seq_dict = {'use sequence': ['sequence_1', 'sequence_2'],
                    'number of trials': ''}
        infoBox = gui.DlgFromDict(dictionary=seq_dict,
                                  title='Select sequence to run experiment')  # display gui to get info from user
        metaData.update({'participant allocation': 'manual_selection',
                         'sequence type': '%s' % seq_dict['use sequence'],
                         'number of trials': '%s' % seq_dict['number of trials']})
        if not infoBox.OK:  # if user hit cancel
            quitExp()  # quit
    
    # build filename for this participant's data
    fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '.csv'

    # is this an existing participant? If so we will create a new file name to store the data under
    if os.path.exists(fileName):  # if they are an existing participant
        # confirm that user knows sessions already exist for this participant's current session and time and advise filename will be different:
        myDlg = gui.Dlg()
        myDlg.addText(
            "This participant has existing files for this session time in the directory! Click ok to continue or cancel to abort. \n\n NOTE: if you choose to continue, files will be stored under a different file name.")
        myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK:  # if the user pressed cancel
            quitExp()
        
        # redefine file name by iteratively appending a number so that existing files are not overwritten
        fileName = uniq_path(fileName)

    metaData.update({'expName': expName, 'date': date})  # record the experiment date and name in the metaData
    
    # check if logfile exists for this participant. If not, create one:
    logFile = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_" + str(metaData['participant allocation']) +'_log.txt'
    if not os.path.exists(logFile):
        with open(logFile, 'w') as fp:
            pass

    # save metaData to log
    saveToLog('..........................................', 0)
    saveToLog('experiment: %s' % (metaData['expName']), 0)
    saveToLog('researcher: %s' % (metaData['researcher']), 0)
    saveToLog('location: %s' % (metaData['location']), 0)
    saveToLog('date: %s' % (metaData['date']), 0)
    saveToLog('participant: %s' % (metaData['participant']), 0)
    saveToLog('session: %s' % (metaData['session number']), 0)
    saveToLog('session time: %s' % (metaData['session time']), 0)
    saveToLog('participant allocation: %s' % (metaData['participant allocation']), 0)
    saveToLog('                                            ', 0)

else:  # otherwise, if it is practice mode:
    logFile = p_dir + os.path.sep + 'P' + str(metaData['participant']) + '_practice_log.txt'
    if not os.path.exists(logFile):
        with open(logFile, 'w') as fp:
            pass
    
    # ask user to define number of trials
    prac_dict = {'number of trials': ''}
    infoBox = gui.DlgFromDict(dictionary=prac_dict,
                              title='enter number of trials')  # display gui to get info from user
    if not infoBox.OK:  # if user hit cancel
        quitExp()  # quit

    # build filename for this participant's practice data
    fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '_PRACTICE' + '.csv'
    # is this an existing participant? If so we will create a new file name to store the data under
    if os.path.exists(fileName):  # if existing participant
        # check user knows sessions already exist for this participant's current session and time:
        myDlg = gui.Dlg()
        myDlg.addText(
            "This participant has existing files for this session time in the directory! Click ok to continue or cancel to abort. \n\n NOTE: if you choose to continue, files will be stored under a different file name.")
        myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK:  # if the user pressed cancel
            quitExp()
        
        # redefine file name by iteratively appending a number so that the original files are not overwritten
        fileName = uniq_path(fileName)
    
    metaData.update({'participant allocation': 'practice'})
    
    # save metaData to log
    saveToLog('..........................................', 0)
    saveToLog('experiment: %s' % (expName), 0)
    saveToLog('researcher: %s' % (metaData['researcher']), 0)
    saveToLog('location: %s' % (metaData['location']), 0)
    saveToLog('date: %s' % (date), 0)
    saveToLog('participant: %s' % (metaData['participant']), 0)
    saveToLog('session: %s' % (metaData['session number']), 0)
    saveToLog('session time: %s' % (metaData['session time']), 0)
    saveToLog('participant allocation: %s' % (metaData['participant allocation']), 0)
    saveToLog('                                            ', 0)

### Prepare stimuli etc ###
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False, ## UPDATE SIZE TO MATCH YOUR CURRENT MONITOR SETTINGS
                    monitor='testMonitor', color=(-1,-1,-1), colorSpace='rgb', units='pix') # setup the Window
generalText = visual.TextStim(win=win, ori=0, name='generalText', text='', font=u'Arial', pos=[0, 0], height=35,
                              wrapWidth=920, color=(1,1,1), colorSpace='rgb', opacity=1, depth=0.0)  # general text
sequenceText = visual.TextStim(win=win, ori=0, name='sequenceText', text='', font=u'Arial', pos=[0, 250], height=90,
                               wrapWidth=None, color=(1,1,1), colorSpace='rgb', opacity=1, depth=0.0)  # sequence text
timerText = visual.TextStim(win=win, ori=0, name='sequenceText', text='', font=u'Arial', pos=[0, -130], height=40,
                            wrapWidth=800, color=(1,1,1), colorSpace='rgb', opacity=1, depth=0.0)  # timer text

# set up the markers that increment across the screen - generate enough so that they cover the full range of the window
listOfMarkers = []  # store for white markers
windowSize = list(win.size) # get window size
for i in range(int(-windowSize[0] / 2), int(windowSize[0] / 2), int(windowSize[0] / 40)):  # generate markers to cover whole screen
    i += 25  # add a slight horizontal adjustment to ensure markers do not go off screen
    listOfMarkers.append(visual.Circle(win, radius=15, edges=32, pos=[i, 0], fillColor='white'))  # generate the markers

# for monitoring key state (only need this if using markers)
keys = key.KeyStateHandler()
win.winHandle.push_handlers(keys)

saveToLog('Set up complete') # save info to log
### set-up complete ###


### run the experiment ###
if metaData['practice mode']:  # if user has chosen practice mode
    res = fingerTapping(n_trials=int(prac_dict['number of trials']), tap_targetSequence = prac_seq, sequenceType ='practice')  # run practice sequence

elif not metaData['practice mode']: # if it is not practice mode
    if not metaData['use automated counter-balancing']: # AND the user has chosen to manually select the sequence type:
        if seq_dict['use sequence'] == 'sequence_1': # EITHER run task with sequence 1:
            res = fingerTapping(n_trials=int(seq_dict['number of trials']), tap_targetSequence = targ_seq_1, sequenceType = 'sequence_1')
        elif seq_dict['use sequence'] == 'sequence_2': # OR run task with sequence 2:
            res = fingerTapping(n_trials=int(seq_dict['number of trials']), tap_targetSequence = targ_seq_2, sequenceType = 'sequence_2') 

    elif metaData['use automated counter-balancing']: # OR if user has selected to use automated counter balancing:
        # NOTE: these allocations are specific to my study (each letter represents one type of grouping/randomisation variable). Adapt groupings to suit individual experiments
        ####### X ORDER 
        if ((metaData['participant allocation'] == 'AJX') or (metaData['participant allocation'] == 'BJX') or (metaData['participant allocation'] == 'AKX') or (metaData['participant allocation'] == 'BKX')):
            # session 1
            if int(metaData['session number']) == 1:
                if metaData['session time'] == 'pm-a':
                    res = fingerTapping(n_trials = 12, tap_targetSequence = targ_seq_1, sequenceType='sequence_1')  # sequence 1 
                elif metaData['session time'] == 'pm-b' or 'am':
                    res = fingerTapping(n_trials = 4, tap_targetSequence = targ_seq_1, sequenceType='sequence_1') # wordlist 1 
            # session 2
            elif int(metaData['session number']) == 2:
                if metaData['session time'] == 'pm-a':
                    res = fingerTapping(n_trials = 12, tap_targetSequence = targ_seq_2, sequenceType='sequence_2')  # sequence 2 
                elif metaData['session time'] == 'pm-b' or 'am':
                    res = fingerTapping(n_trials = 4, tap_targetSequence = targ_seq_2, sequenceType='sequence_2')  # sequence 2 

        ####### Y ORDER
        elif ((metaData['participant allocation'] == 'AJY') or (metaData['participant allocation'] == 'BJY') or (metaData['participant allocation'] == 'AKY') or (metaData['participant allocation'] == 'BKY')):
            # session 1
            if int(metaData['session number']) == 1:
                if metaData['session time'] == 'pm-a':
                    res = fingerTapping(n_trials = 12, tap_targetSequence = targ_seq_2, sequenceType='sequence_2')  # sequence 2 
                elif metaData['session time'] == 'pm-b' or 'am':
                    res = fingerTapping(n_trials = 4, tap_targetSequence = targ_seq_2, sequenceType='sequence_2')  # sequence 2 
            # session 2
            elif int(metaData['session number']) == 2:
                if metaData['session time'] == 'pm-a':
                    res = fingerTapping(n_trials = 12, tap_targetSequence = targ_seq_1, sequenceType='sequence_1')  # sequence 1 
                elif metaData['session time'] == 'pm-b' or 'am':
                    res = fingerTapping(n_trials = 4, tap_targetSequence= targ_seq_1, sequenceType='sequence_1')  # sequence 1 


## End screen ##
saveToLog('Presenting end screen')  # save info to log
win.setColor('#000000', colorSpace='hex')  # set background colour to black
win.flip()
generalText.setText(u'Thank you. That is the end of this section. Please inform the researcher you have finished.')
generalText.draw()
win.flip()  # present video buffer
event.waitKeys(keyList=['end']) # wait for the end key to be pressed before continuing
event.clearEvents() # clear the event buffer

saveToLog('Experiment presentation over')  # save info to log
### Finished running the experiment ###


### Save and clean up ###
win.close()

'''
Save the data as a csv file. The loop below also checks if saving is not possible, usually because the file is already open, and asks user to close if this is the case
if this does not resolve the situation, attempt is made to save the data with a different filename.
'''
while True:
    try:
        res.to_csv(fileName)
        saveToLog('Data saved with file name: %s' % fileName) # save info to log
        break
    except: # if cannot save data, likely because file is already open, ask user to close
        saveToLog('Problem encountered saving data - requesting user close open data files...') # save info to log
        myDlg = gui.Dlg()
        myDlg.addText(
                "Unable to store data. Try closing open excel files and then click ok. Press cancel to attempt data storage to new file.")
        myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK:  # if the user pressed cancel
            fileName = p_dir + os.path.sep + 'P' + str(metaData['participant']) + "_ProblemSaving_" + str(metaData['participant allocation']) + '_S' + str(metaData['session number']) + '_' + str(metaData['session time']) + '.csv'
            saveToLog('Attempting to save data with different filename: %s' %fileName) # save info to log
            try:
                res.to_csv(fileName)
                print('Data was saved with a different filename: %s' %fileName)
                saveToLog('Data saved with file name: %s' % fileName) # save info to log
                break
            except:
                saveToLog('Major error: Data could not be saved') # save info to log
                quitExp() # quit the experiment

t = globalClock.getTime() # get run time of experiment
saveToLog('Total experiment runtime was %i seconds' % t) # record runtime to log
saveToLog('..........................................', 0)

# Shut down:
core.quit()

