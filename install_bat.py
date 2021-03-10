import os


working_directory = os.getcwd()
print(working_directory)
program = 'main.pyw'


with open('start_file_finder.bat', 'w') as auto:
    auto.write(rf"start {working_directory}\{program}")



