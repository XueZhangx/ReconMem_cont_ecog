# Import necessary libraries
from psychopy import visual, core, event  # , sound
import os, sys, configparser
import pandas as pd
import numpy as np
from datetime import datetime

# Read config
exp_config = configparser.ConfigParser()
exp_config.read('config')
sub = int(sys.argv[1])
block = 13

exp_dir = exp_config['DIR']['exp_dir']
stimuli_dir = exp_config['DIR']['stimuli_dir']
curr_sub_dir = os.path.join(exp_dir, 'sub-%02d' % sub)
curr_block_dir = os.path.join(curr_sub_dir, 'Block%02d_info.csv' % block)
stimulus_duration = float(exp_config['EXP']['stimulus_duration'])
stimulus_blank = float(exp_config['EXP']['stimulus_blank'])

key_list = exp_config['EXP']['key_list'].split(', ')
pre_exp_time = float(exp_config['EXP']['pre_exp_time'])
post_exp_time = float(exp_config['EXP']['post_exp_time'])
exp_mode = bool(exp_config['EXP']['exp_mode'])
print(exp_mode)
test_screen_size = (int(exp_config['EXP']['test_screen_width']), int(exp_config['EXP']['test_screen_height']))
exp_screen_size = (int(exp_config['EXP']['exp_screen_width']), int(exp_config['EXP']['exp_screen_height']))

# Load dataframe
exp_df = pd.read_csv(curr_block_dir).iloc[:20]
# Add a correct response column
exp_df['Correct'] = np.nan
for curr_row in exp_df.iterrows():
    if curr_row[0] == 0:
        exp_df.loc[curr_row[0], 'Correct'] = 0
    else:
        curr_img = curr_row[1]['image']
        if curr_img in exp_df.iloc[:curr_row[0]]['image'].values:
            exp_df.loc[curr_row[0], 'Correct'] = 1
        else:
            exp_df.loc[curr_row[0], 'Correct'] = 0

# Create a logfile for current run
timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')google translate
ses_info = 'Subject: {} \n BLock: {} \n'.format(sub, block)
log_file = open(os.path.join(curr_sub_dir,
                             'experiment_log_block%02d_%s.txt' % (block, timestamp)), 'a')
# Log info about this run
date_line = 'Session Start Time: {}\n'.format(datetime.now())
log_file.write(date_line)
log_file.write(ses_info)

# Create a window for your experiment
if not exp_mode:
    win = visual.Window(size=test_screen_size, fullscr=exp_mode, color='gray', screen=1)
    print(win.getActualFrameRate())
    screen_size = test_screen_size
else:
    win = visual.Window(size=exp_screen_size, fullscr=exp_mode, color='gray', screen=1)
    print(win.getActualFrameRate())
    screen_size = exp_screen_size

# Create a fixation dot
fixation_dot = visual.Circle(win, size=(0.02 * (screen_size[1] / screen_size[0]), 0.02),
                             fillColor='white', lineColor='white')
red_fixation_dot = visual.Circle(win, size=(0.02 * (screen_size[1] / screen_size[0]), 0.02),
                                 fillColor='red', lineColor='red')
fixation_cross = visual.TextStim(win, text="+", color='white')

# Create a clock to measure time
stimulus_clock = core.Clock()

# Check button press
for current_key in key_list:
    key_text = visual.TextStim(win, text="{} 请按.".format(current_key), color='white', font='MS Gothic')
    keys = event.getKeys(keyList=key_list)
    while current_key not in keys:
        key_text.draw()
        win.flip()
        keys = event.getKeys(keyList=key_list)
    win.flip()

# Countdown to start experiment
countdown_start = stimulus_clock.getTime()
while stimulus_clock.getTime() - countdown_start < pre_exp_time:
    count_down = int(np.ceil(pre_exp_time - (stimulus_clock.getTime() - countdown_start)))
    instruction_text = visual.TextStim(win,
                                       text="实验将在{}秒后开始。\n 请准备好。\n没见过的图片=0， 见过的图片=1。".format(count_down),
                                       color='white')
    # Display instructions
    instruction_text.draw()
    # Make mouse invisible
    mouse = event.Mouse(visible=False)
    win.flip()

# Log experiment start time
exp_startTime = stimulus_clock.getTime()
line_info = 'Experiment started at {}\n'.format(exp_startTime)
log_file.write(line_info)

print('Starting Block {}...'.format(block))
curr_block_df = exp_df
stimuli_list = []
# Preload the image list
for curr_row in curr_block_df.iterrows():
    img_ind = curr_row[1]['Image Index']
    img_type = img_ind.split('-')[0]
    img_num = img_ind.split('-')[1]
    img_dir = os.path.join(stimuli_dir, '{}s'.format(img_type), '{}.jpg'.format(img_num))
    img_obj = visual.ImageStim(win, image=img_dir)
    stimuli_list.append(img_obj)

# Present a fixation dot to indicate the start of a block
red_fixation_dot.draw()
win.flip()
fixation_start = stimulus_clock.getTime()
while True:
    if stimulus_clock.getTime() - fixation_start >= 0.2:
        break

# Now present the images
onset_times = np.ones((len(stimuli_list), 1)) * np.nan
offset_times = np.ones((len(stimuli_list), 1)) * np.nan
responses = np.ones((len(stimuli_list), 1)) * np.nan
RTs = np.ones((len(stimuli_list), 1)) * np.nan
correct_responses = exp_df['Correct'].values
for trial_count, stimulus in enumerate(stimuli_list):

    # Start a trial and present stimulus
    img_startTime = stimulus_clock.getTime() - exp_startTime
    onset_times[trial_count] = img_startTime
    firstKeypress = True

    # Presentation loop
    while True:
        # Check for user input to stop the script
        hault_keys = event.getKeys(keyList=['escape'])
        if 'escape' in hault_keys:
            win.close()
            core.quit()


        stimulus.draw()
        win.flip()
        #TODO trigger（stim_on)

        keys = event.getKeys(keyList=key_list)
        if keys:
            # TODO trigger（keypress)
            log_file.write('{}, {}, {}, {}, {}\n'.format(block,
                                                         trial_count,
                                                         img_startTime,
                                                         stimulus_clock.getTime() - exp_startTime - img_startTime,
                                                         keys[0]))
            print('Trial {}, Responded {}'.format(trial_count,
                                                       keys[0]))
            text_pos = (0, 0.5)
            if firstKeypress:
                responses[trial_count] = keys[0]
                RTs[trial_count] = stimulus_clock.getTime() - exp_startTime - img_startTime
                if int(correct_responses[trial_count]) == int(keys[0]):
                    text_acc = visual.TextStim(win, text="正确", color='blue', pos=text_pos)
                elif int(correct_responses[trial_count]) != int(keys[0]):
                    text_acc = visual.TextStim(win, text="错误", color='red', pos=text_pos)
                stimulus.draw()
                text_acc.draw()
                win.flip()
                firstKeypress = False


        if stimulus_clock.getTime() - exp_startTime - img_startTime >= stimulus_duration:
            break  # Exit the loop after presenting for the specified duration
    # TODO trigger（stim_off)
    # Present ISI
    offset_times[trial_count] = stimulus_clock.getTime() - exp_startTime
    isi_startTime = stimulus_clock.getTime() - exp_startTime
    # ITI loop
    while True:
        # Check for user input to stop the script
        hault_keys = event.getKeys(keyList=['escape'])
        if 'escape' in hault_keys:
            win.close()
            core.quit()

        # for frame in range(int(ISI / frame_duration)):
        fixation_dot.draw()
        win.flip()
        keys = event.getKeys(keyList=key_list)
        if keys:
            # TODO trigger（keypress)
            log_file.write('{}, {}, {}, {}, {}\n'.format(block,
                                                         trial_count,
                                                         img_startTime,
                                                         stimulus_clock.getTime() - exp_startTime - img_startTime,
                                                         keys[0]))
            print('Trial {}, Responded {}'.format(trial_count,
                                                        keys[0]))
            if firstKeypress:
                responses[trial_count] = keys[0]
                RTs[trial_count] = stimulus_clock.getTime() - exp_startTime - img_startTime
                firstKeypress = False

        if stimulus_clock.getTime() - exp_startTime - isi_startTime >= stimulus_blank:
            break  # Exit the loop after presenting for the specified duration
    if np.isnan(responses[trial_count]):
        print('Trial {}, No response'.format(trial_count))


# Save the data from this block
block_output_dir = os.path.join(curr_sub_dir, 'response_df_block{}_{}.csv'.format(block, timestamp))
# Save the experiment log and results
curr_block_df['Onset'] = onset_times
curr_block_df['Offset'] = offset_times
curr_block_df['Response'] = responses
curr_block_df['RT'] = RTs
curr_block_df.to_csv(block_output_dir)

exp_endTime = stimulus_clock.getTime()

log_file.close()

# Countdown to end the experiment
while stimulus_clock.getTime() - exp_endTime < post_exp_time:
    count_down = int(np.ceil(post_exp_time - (stimulus_clock.getTime() - exp_endTime)))
    instruction_text = visual.TextStim(win,
                                       text="本回实验将在{}秒后结束。\n请稍等。".format(
                                           count_down),
                                       color='white')
    # Display instructions
    instruction_text.draw()

    win.flip()

# Make mouse visible
mouse.setVisible(True)
# win.mouseVisible = True

# Cleanup and exit the experiment
win.close()
core.quit()
