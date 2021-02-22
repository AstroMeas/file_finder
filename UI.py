import tkinter as tk
import configparser
import os

PROGRAMM_NAME = 'window'
MAX_DIRECTORIES = 15

class UserInterface:

    def __init__(self):
        self.main_window = tk.Tk(PROGRAMM_NAME)
        self.main_window.config(bg='light grey')
        self.main_window.title(PROGRAMM_NAME)
        self.main_window.config(padx=25, pady=25)

        ############### MenuBar ###############
        self.menu = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menu)
        self.menu.add_cascade(label='File', )

        ############### MenuBar ###############

        ############### Ergebnisse ###############
        self.search_results = tk.Listbox(self.main_window, width=100, height=20)
        self.search_results.grid(row=0, column=2, rowspan=MAX_DIRECTORIES)
        self.open_button = tk.Button(self.main_window)
        self.open_button.config(text='Öffnen', command=self.open_result)
        self.open_button.grid(row=MAX_DIRECTORIES+1, column=2, padx=5, pady=10)
        self.result_lst = []
        ############### Ergebnisse ###############

        ########## Suche ###############
        self.search_entry = tk.Entry(self.main_window)
        self.search_entry.grid(row=MAX_DIRECTORIES+1, column=0, padx=5, pady=10)
        self.search_button = tk.Button()
        self.search_button.config(text='Suchen', command=self.search)
        self.search_button.grid(row=MAX_DIRECTORIES+1, column=1, padx=5, pady=10)
        ########## Suche ###############

        ############### Pfade ###############
        self.folder_lst = [r'C:\Users\rdeic\OneDrive\Dokumente\Programierung\hundredDayOfCode\code\my_bu_manager',
                           r'C:\Users\rdeic\OneDrive\Dokumente\Programierung\hundredDayOfCode\code\Day23-Turtle-crossing',
                           r'C:\Users\rdeic\OneDrive\Dokumente\Unterlagen']
        self.check_variables = [tk.StringVar() for i in range(len(self.folder_lst))]
        self.checkbox_lst = []
        for i in self.folder_lst:
            self.create_checkbox(i, self.folder_lst.index(i))
        ############### Pfade ###############


        self.main_window.mainloop()







    def open_result(self):
        index_result = str(self.search_results.curselection()[0])
        item_to_open = self.search_results.get(index_result)
        print(item_to_open)
        os.system(f'start {item_to_open}')


    def create_checkbox(self,folder, row_):
        tk.Checkbutton(text=folder, variable=self.check_variables[row_], onvalue=folder,
                       offvalue='').grid(row=row_, column=0, columnspan=2, padx=20, sticky='w')

    def update_listbox(self):
        self.search_results.insert(0, '')
        for i in self.result_lst:
            self.search_results.insert(0,i.replace('/','\\'))









    def search(self):
        self.search_button.config(state=tk.DISABLED)
        self.search_item = self.search_entry.get()
        if self.search_item == '':
            self.search_item = 'kein Wert eingetragen'
        self.search_folder_lst = [i.get().replace('\\','/') for i in self.check_variables]
        for i in self.search_folder_lst:
            print(i)
        self.result_lst = []

        self.searching_initial()

        self.update_listbox()

        self.search_button.config(state=tk.NORMAL)
        print(self.result_lst)

    def searching_initial(self):

        for path in self.search_folder_lst:  # all source paths
            #self.file_list[path] = []
            try:
                item_lst = os.listdir(path)
                for i in range(len(item_lst)):  # list content
                    item_lst[i] = path + '/' + item_lst[i]
                    if os.path.isfile(item_lst[i]) and self.search_item in item_lst[i]:
                        self.result_lst.append(item_lst[i])
                    elif os.path.isdir(item_lst[i]):
                        self.find_all_recursiv(item_lst[i], path)
            except:
                pass
            # Hier muss noch die Fehlermeldung rein

    def find_all_recursiv(self, cur_directory, path):
        try:
            dir_content = os.listdir(cur_directory)
            for i in range(len(dir_content)):
                dir_content[i] = cur_directory + '/' + dir_content[i]
                try:
                    if os.path.isfile(dir_content[i]) and self.search_item in dir_content[i]:
                        self.result_lst.append(dir_content[i])
                    elif os.path.isdir(dir_content[i]):
                        self.find_all_recursiv(dir_content[i], path)
                except:
                    pass
        except PermissionError:
            pass
        except:
            pass