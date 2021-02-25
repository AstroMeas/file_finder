import os


working_directory = os.getcwd()
print(working_directory)
program = 'main.py'


with open('start_file_finder.bat', 'w') as auto:
    auto.write(rf"python {working_directory}\{program}")



