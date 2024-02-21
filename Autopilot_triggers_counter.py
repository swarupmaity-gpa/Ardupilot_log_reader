# -*- coding: utf-8 -*-
"""
@author: Swarup Maity
"""

import os
import csv
import datetime
from tkinter import Tk, filedialog
from fileinput import close
from pickle import TRUE
from pymavlink import mavutil
from df_to_csv import DFReader_binary
from modified_code_29082022 import extra_events_remove

# Global Constants
AUTOPREFIX = "AP"
MINIMUM_TIME_DIFFERENCE_MS = 800

def extracting_autopilot_CAM_info(filename):
    """Extract autopilot CAM info from a given log file."""
    print("Autopilot log:", filename)
    log = DFReader_binary(filename)

    extra_trg_msg = 0
    in_diff = 0
    count = 0
    j = 0

    while TRUE:
        m = log.recv_msg()
        try:
            data_packet = m.to_dict()
            gps_time = data_packet['GPSTime']
            count += 1
            delta = gps_time - in_diff
            print("Time_diff:", delta)
            if delta < MINIMUM_TIME_DIFFERENCE_MS:
                extra_trg_msg += 1
                print(f"{AUTOPREFIX}_false_trigger_number:", j + 1)
            in_diff = gps_time
            j += 1

        except Exception as e:
            print(f"Error processing message: {e}")

        if m is None:
            print("ENDOFFILE")
            break

    print("Number-of-Extra-trigger-message:", extra_trg_msg)
    print('Total number of CAM_MSG', count)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    autopilot_log = filedialog.askopenfilename(title='Select Autopilot log: ')  # "2022-11-30 12-07-23.bin"

    extracting_autopilot_CAM_info(autopilot_log)
