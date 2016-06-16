# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:09:05 2015

@author: qwe14789cn
"""
import os
import sys
import platform
depart_path = os.sep

pth1 = sys.argv
pth2 = sys.path[0]

pth1_str = str(pth1)
pth2_str = str(pth2)
pth_str = pth2_str + pth1_str

def get_dir(path):
    char_L = 0
    char_R = -1
    while(1):
        if path[char_L] == depart_path:
            break
        if char_L >= len(path):
            break
        char_L = char_L + 1

    while(1):
        if path[char_R] == depart_path or path[char_R] == '[':
            break
        char_R = char_R - 1
    return path[char_L:char_R]

if platform.system()=='Windows':
    main_dir = pth2
else:
    main_dir = get_dir(pth_str)

input_data = depart_path + 'input'
output_data = depart_path + 'output'
program_dir = depart_path + 'program'
sys.path.append(main_dir + program_dir)

os.chdir(main_dir)

while(1):
    i = os.system('clear')
    print
    print(' ')
    print('-' * 60)
    print(' ' * 15 + 'please select your choice below:')
    print('-' * 60)
    print('                               ')
    print('\t\t1.read and save wrf data')
    print('\t\t2.calculate and save polar data')
    print('\t\t0.exit program')
    print('-' * 60)

    select = raw_input('select:?')
    print(' ')

    if select == '1':
        os.chdir(main_dir + program_dir)
        import pr1
        pr1.fun(main_dir, input_data, output_data)
        os.chdir(main_dir)

    elif select == '2':
        os.chdir(main_dir + program_dir)
        import pr2
        pr2.fun(main_dir, input_data, output_data)
        os.chdir(main_dir)

    elif select == '0':
        print 'thank you!'
        break
    else:
        print 'error input,please select from 1~5'

    raw_input('press any key to continue...')
