#################################################################
# FILE : ex5.py
# WRITER : Dolev Mizrahi , dolevm
# EXERCISE : intro2cs2 ex5 2020
# DESCRIPTION: wave_editor program
#################################################################
import numpy
import math
import wave_helper as wh
import sys
import copy
import os.path

SAMPLE_RATE = 2000
MAX_VOLUME = 32767
MIN_VOLUME = -32768
MAIN_MENU_MSG = "<~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>" + "\n" \
                "what would you like to do?" + "\n" \
                + "1. Edit a wav file" + "\n" \
                + "2. Compose a beautiful masterpiece" + "\n" \
                + "3. Exit" + "\n" \
                + "<~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>" + "\n"
ERROR_MSG = "You've chosen an illegal option."
ILLEGAL_FILE = "There was a problem with your file."
EDIT_MSG = "Which file would you want to edit?" + "\n"
EDIT_OPTIONS = "What would you want to do?" + "\n" "1. Reverse it" \
               + "\n" + "2. Negate the audio" + "\n" + "3. speed it up" \
               + "\n" + "4. slow it down" + "\n" + "5. Turn volume up" \
               + "\n" + "6. Turn volume down" + "\n" \
               + "7. Apply low pass filter" + "\n" \
               + "8. I finished" + "\n"
DICT = {"A": 440, "B": 494, "C": 523, "D": 587,
        "E": 659, "F": 698, "G": 784, "Q": 0}
COMPOSITION_MSG = "Please, provide us a composition file:" + "\n"
SAVE_FILE = "Please enter file name: "
VOLUME_PRODUCT = 1.2
EDIT_WAVE = 1
COMPOSE = 2
EXIT = 3
REVERSE = 1
NEGATE = 2
SPEED = 3
SLOW = 4
VOL_UP = 5
VOL_DOWN = 6
FILTER = 7
FINAL = 8


def average(a, b):
    """calculate average for 2 elements
    :returns list"""
    return [int((x + y) / 2) for x, y in zip(a, b)]


def triple_average(a, b, c):
    """calculate average for 3 elements
    :returns list"""
    return [int((x + y + z) / 3) for x, y, z in zip(a, b, c)]


def reverse_wave(audio_data):
    """This function reverses the audio
    :returns list of lists"""
    return [sample for sample in audio_data[::-1]]


def negate_wave(audio_data):
    """This function negate the audio
    :returns list of lists"""
    return [[32767 if i == -32768 else (-1) * i
             for i in sample] for sample in audio_data]


def speed_up_wave(audio_data):
    """This function speeds up the audio
    :returns list of lists"""
    # creating list of samples at odd positions
    return [sample for index, sample in
            enumerate(audio_data) if index % 2 == 0]


def slow_down_wave(audio_data):
    """This function slows down the audio
    :returns list of lists"""
    # creates a list of averages
    average_list = [average(audio_data[i], audio_data[i + 1])
                    for i in range(len(audio_data) - 1)]
    slow_list = [None] * (len(audio_data) + len(average_list))
    # adding averages at odd positions
    slow_list[::2] = audio_data
    slow_list[1::2] = average_list
    return slow_list


def volume_up_wave(audio_data):
    """This function turn up the volume
    :returns list of lists"""
    return [[-32768 if int(1.2 * i) < -32768
             else 32767 if int(1.2 * i) > 32767 else int(1.2 * i)
             for i in sample] for sample in audio_data]


def volume_down_wave(audio_data):
    """This function turn down the volume
    :returns list of lists"""
    # divides each sample by 1.2 and add it to list
    return [[int(i / 1.2) for i in sample]
            for sample in audio_data]


def low_pass_filter(audio_data):
    """This function applies a low pass filter
    :returns list of lists"""
    return [triple_average(audio_data[i - 1],
                           audio_data[i],
                           audio_data[i + 1])
            # calculate averages for inner samples
            # then adding them to a list
            if 1 <= i <= (len(audio_data) - 2)
            # calculate average for edges and add it to the list
            else average(audio_data[i], audio_data[i + 1])
            if i == 0 else average(audio_data[i - 1], audio_data[i])
            # iterating over each sample
            for i in range(len(audio_data))]


def check_file_name():
    """This function checks if the wave file is legal
    :returns [int, list of lists]"""
    file = input(EDIT_MSG)
    # calling load_wave in order to import wave data
    while wh.load_wave(file) == -1:
        print(ILLEGAL_FILE)
        file = input(EDIT_MSG)
    return wh.load_wave(file)


def edit_wave_menu(wave):
    """This is the edit menu where all
    the wave modifications are done"""
    modified_wave = copy.deepcopy(wave)
    while True:
        # edit menu options, check if user choice is legal
        edit_option = check_input(8, EDIT_OPTIONS)
        if edit_option == REVERSE:
            modified_wave[1] = reverse_wave(modified_wave[1])
        elif edit_option == NEGATE:
            modified_wave[1] = negate_wave(modified_wave[1])
        elif edit_option == SPEED:
            modified_wave[1] = speed_up_wave(modified_wave[1])
        elif edit_option == SLOW:
            modified_wave[1] = slow_down_wave(modified_wave[1])
        elif edit_option == VOL_UP:
            modified_wave[1] = volume_up_wave(modified_wave[1])
        elif edit_option == VOL_DOWN:
            modified_wave[1] = volume_down_wave(modified_wave[1])
        elif edit_option == FILTER:
            modified_wave[1] = low_pass_filter(modified_wave[1])
        elif edit_option == FINAL:
            final_menu(modified_wave)
            break


def check_composing_file():
    """This function checks if composing file is legit
    :returns list"""
    composing_file = input(COMPOSITION_MSG)
    while not (os.path.exists(composing_file)
               and os.path.isfile(composing_file)):
        print(ILLEGAL_FILE)
        composing_file = input(COMPOSITION_MSG)
    return composing_file


def convert_composition_to_list():
    """This function converts the composing
     instructions to a readable list
     :returns list"""
    composition_file = check_composing_file()
    with open(composition_file, 'r') as file:
        composing_as_list = file.read().split()
    return composing_as_list


def calc_equation(samples_per_cycle, i):
    """This function calculates the i-th sample for a given note
    :returns list"""
    return [int(MAX_VOLUME * math.sin((math.pi * 2 * i) * samples_per_cycle)),
            int(MAX_VOLUME * math.sin((math.pi * 2 * i) * samples_per_cycle))]


def composition_menu():
    """This is the composition menu"""
    # checking the composing instructions file
    # converting it to a list
    comp_lst = convert_composition_to_list()
    comp_result = [SAMPLE_RATE, []]
    for note in range(len(comp_lst[::2])):
        # calculate the inverse of
        # samples_per_cycle per each note
        samples_per_cycle = DICT[comp_lst[::2][note]] / SAMPLE_RATE
        for i in range((SAMPLE_RATE * int(comp_lst[1::2][note])) // 16):
            # adding the i-th sample for a given note
            comp_result[1].append(calc_equation(samples_per_cycle, i))
    return edit_wave_menu(comp_result)


def check_modified_file(file):
    """This function checks and saves the file"""
    file_name = input(SAVE_FILE)
    # check if the parameters are legal
    while True:
        if file_name != "":
            # after passing the test, saves file
            wh.save_wave(file[0], file[1], file_name)
            break
        else:
            print(ILLEGAL_FILE)
            file_name = input(SAVE_FILE)


def final_menu(file):
    """This is the final menu"""
    check_modified_file(file)
    menu()


def check_input(num_of_options, message_to_display):
    """This function checks if the user
    chose an option from the relevant menu
    :returns integer (user's choice)"""
    while True:
        user_input = input(message_to_display)
        # checks if it's a single digit between 1-num_of_options
        if len(user_input) != 1 or not user_input.isdigit() \
                or not 49 <= ord(user_input) <= ord(str(num_of_options)):
            print(ERROR_MSG)
        else:
            break
    return int(user_input)


def menu():
    """This is the Main Menu"""
    # asks for an input and check it
    choice = check_input(3, MAIN_MENU_MSG)
    if choice == EDIT_WAVE:
        wave_file = list(check_file_name())
        edit_wave_menu(wave_file)
    elif choice == COMPOSE:
        composition_menu()
    elif choice == EXIT:
        sys.exit()
    else:
        print(ERROR_MSG)


if __name__ == '__main__':
    menu()
