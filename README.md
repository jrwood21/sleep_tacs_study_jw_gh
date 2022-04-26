# sleep_tacs_study_jw_gh
 finger tapping and word association tasks in psychopy

## Finger tapping task
 I have adapted the code published by Tom Hardwicke (https://github.com/TomHardwicke/finger-tapping-task) to replicate the finger tapping task from Walker et al. 2002 (DOI:https://doi.org/10.1016/S0896-6273(02)00746-8) for a behavioural experiment. I have updated the code with the main amendments:
 > - Updated the code to run in Psychopy v2022.1.1.
 > - Updated the experimental design to assess consolidation, rather than reconsolidation.
 > - Added an option to run the task manually with any number of trials.
 > - Updated the file saving so that all trial data collected so far is saved if the experiment is quit partway through.
 > - Changed the quitexp key to End rather than Esc (too close to 1234).
 > - Updated the automated counterbalancing procedure and the stream analysis function to match my experimental design.
 > - Automated the creation of output data folders based on experimental inputs, and prevented overwriting of output files.

 ## Word association task
 I used the finger tapping task above as a template to replicate the word association task from Marshall et al. 2006 (DOI:https://doi.org/10.1038/nature05278) for a behavioural experiment. Some basic info:
 > - The task has two components: a word learning task and a cued recall task.  
 > - The presentation of word pairs during the learning task is automatic. The order of word presentation is random every time the task is run. The order that word pairs are presented is exported to a .xlsx file.
 > - During the recall task, cue words are presented one at a time in a random order on the computer screen. Only one word is shown at once. The participant is expected to respond verbally to the cue word with the appropriate response word. Once the cue word is displayed, the computer will wait for a mouse click before proceeding. Once the participant has provided their response, click the mouse to proceed. Accuracy feedback will only be provided during the recall task if the pm-a session time is selected, as this is the only time that participants will receive feedback in my experiment. Accuracy feedback is displayed for 2.5sec, and progression to the next cue word is automatic (i.e., no mouse click required). No accuracy feedback will be provided if pm-b or am is selected. 
 > - In the recall task, all verbal responses are audio recorded and saved to .wav files for external analysis (automated voice detection is inappropriate to determine response time in this situation, as it cannot distinguish between umms/ahhs and real responses). The order of word pair presentation during the recall phase is also output to a .xlsx file.
 > - The automated counterbalancing procedure automatically selects the correct combination of tasks/wordlist to match my experimental design. Both the learning and recall tasks can be run manually by deselecting the automated counterbalancing procedure box in the first dialogue box, and then selecting the word list and task type (i.e., learning or recall) in the 2nd dialogue box. Practice sessions can also be run by selecting practice mode.
 > - Participant identifier codes must be numeric - no character input.
