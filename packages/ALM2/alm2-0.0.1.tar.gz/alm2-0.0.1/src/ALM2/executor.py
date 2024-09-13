###########################################
#   Copyright (C) 2024 Sherenaz Al-Haj Baddar (The University of Jordan)
# 	This program is an entry point, it runs other the Python programs in this project and prompts the user for necessary input
###########################################
#   This software is licensed under the GNU General Public License version 3 (GPL-3), as published by the Free Software Foundation.
#   You can find a copy of the license at https://www.gnu.org/licenses/gpl-3.0.en.html
########################################################

import subprocess
import shutil
import os
import sys

def run_script():
  """Runs another Python script.

  Args:
    script_path: The path to the Python script to run.
  """

  # print current files
  files = [file for file in os.listdir(".") if file.endswith("csv") and "fix_counts" not in file]
  #files = os.listdir()
  for file in files:
      print(file)
  
  #read dataset file name from user
  source_file = input("Enter dataset file name from the previous list: ")
  dataset_file = "all_fix_counts.csv"
  sample_file =   "test_fix_counts.csv"
  scrambler_script_path = "scrambler.py"
  ULang_script_path = "LogL-global-v5.py"

  #call file loader to copy it to all_fix_counts.csv
  try:
    shutil.copy(source_file, dataset_file)
    print(f"File copied successfully")
  except FileNotFoundError:
    print(f"Error: File not found at {source_file}")
    print("script aborted")
    sys.exit()
    
  #call scrambler to read the perentage of input and generate test_fix_counts.csv
  ratio = input("enter a ratio, choose one from [0.05, 0.1, 0.15,0.2, 0.25]: ")
  try:
    subprocess.run(["python3", scrambler_script_path, ratio])
  except FileNotFoundError:
    print(f"Error: Script not found at {script_path}")
    print("script aborted")
    sys.exit()

  
  #call Uncle Lang script
  accuracy = input("mpmath accuracy: ")
  precision = input("mantissa precision: ")
  try:
    subprocess.run(["python3", ULang_script_path, accuracy, precision, source_file])
  except FileNotFoundError:
    print(f"Error: Script not found at {script_path}")
    print("script aborted")
    sys.exit()
  
  
# Example usage:
run_script()
