# -*- coding: utf-8 -*-

import os
import getpass

is_debug = True
mount_folder = '/home/SMB/NAS'
mount_users = 'pi'
mount_group = 'users'
bitlocker_folder = '/media/bitlocker'
#Set CommandHold to FALSE to make sure command can be send
commandhold = True

def debugger(text):
    if is_debug is True:
        print('[Debug]' + str(text))
    
def mounter(source,point):
    debugger('Mount ' + str(source) + ' ' + 'to ' + str(point))
    mount_option = '-o ' + 'gid=' + str(mount_group) + ',' + 'uid=' + str(mount_users)
    send_command = 'mount ' + str(mount_option) + ' ' + str(source) + ' ' + str(point)
    debugger('Sending System Command: ' + str(send_command))
    if commandhold is False:
        os.system(str(send_command))
    else:
        print('[Info] CommandHold switch is on,not send any command to system.')

def bitlocker_unlocker(source,point,password):
    debugger('Unlocking ' + str(source))
    send_command = 'dislocker -r -V ' + str(source) + ' -u' + '*****' + ' -- ' + str(bitlocker_folder)
    debugger('Sending System Command: ' + str(send_command))
    if commandhold is False:
        os.system('dislocker -r -V ' + str(source) + ' -u' + str(password) + ' -- ' + str(bitlocker_folder))
    source = str(bitlocker_folder) + '/disklocker-file'
    debugger('Mount ' + str(source) + ' ' + 'to ' + str(point))
    send_command = 'mount -r -o loop ' + str(source) + ' ' + str(point)
    debugger('Sending System Command: ' + str(send_command))
    if commandhold is False:
        os.system(str(send_command))
    else:
        print('[Info] CommandHold switch is on,not send any command to system.')
    
#Main
print('''

###Disk mount tools###
=== Version 1.3.5 ===
Bash By | Tiya Anlite
This bash only run in Linux
Bitlocker unlock support by Dislocker,make sure you have installed.
=====================

[Info] Using ''fdisk -l '' to check all disk
''')
if commandhold is True:
    print('[Info] CommandHold switch is on,you should to set FALSE that is bash to work')
init_source = input('Enther mount source(like ''sda1'')  ')
mount_source = '/dev/' + str(init_source)
debugger('String: mount_source = ' + str(mount_source))
init_point = input('Enther mount point(like ''1'')  ')
mount_point = str(mount_folder) + str(init_point)
debugger('String: mount_point = ' + str(mount_point))
is_bitlocker = input('Is bitlocker source? (Y/N) ')
if is_bitlocker == 'y':
    is_bitlocker = True
if is_bitlocker == 'Y':
    is_bitlocker = True
    
if is_bitlocker is True:
    debugger('Mount Mode have been set to Bitlocker Mode')
    init_password = getpass.getpass('Enther your bitlocker password ')
    init_sure = input('Are you sure want to unlock and mount ' + str(mount_source) + ' to ' + str(mount_point) + ' ? (Y/N) ')
    if init_sure == 'y':
        bitlocker_unlocker(mount_source,mount_point,init_password)
        print('[Info] Mount Success')
        print('[Info] Bash End')
        exit()
    if init_sure == 'Y':
        bitlocker_unlocker(mount_source,mount_point,init_password)
        print('[Info] Mount Success')
        print('[Info] Bash End')
        exit()
    print('[Info] You cancel your operation')
    print('[Info] Bash End')
    exit()
else:
    debugger('Mount Mode have been set to Normal Mode')
    init_sure = input('Are you sure want to mount ' + str(mount_source) + ' to ' + str(mount_point) + ' ? (Y/N) ')
    if init_sure == 'y':
        mounter(mount_source,mount_point)
        print('[Info] Mount Success')
        print('[Info] Bash End')
        exit()
    if init_sure == 'Y':
        mounter(mount_source,mount_point)
        print('[Info] Mount Success')
        print('[Info] Bash End')
        exit()
    else:
        print('[Info] You cancel your operation')
        print('[Info] Bash End')
           
exit()
      
    
