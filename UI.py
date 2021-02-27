import configparser
import os
import tkinter as tk
from random import randint
from tkinter import filedialog
import threading
import search_status
from tkinter import messagebox

PROGRAMM_NAME = 'Dateisucher'
MAX_DIRECTORIES = 40
LISTBOX_WIDTH = 130
UNIQUE_RESULTS = False
MAX_RESULTS = 500



class UserInterface:

    def __init__(self):
        self.main_window = tk.Tk(PROGRAMM_NAME)
        self.main_window.config(bg='light grey')
        self.main_window.title(PROGRAMM_NAME)
        self.main_window.config(padx=25, pady=25)
        self.main_window.protocol('', self.stop_program)
        #self.distance_label = tk.Label(self.main_window, bg='light grey')
        #self.distance_label.grid(row=49, column=0, pady=20)
        self.exit_button = tk.Button(self.main_window, width=20)
        self.exit_button.config(text='Beenden', command=self.stop_program)
        self.exit_button.grid(row=50, column=2, pady=5)
        ######
        self.read_config()
        ######

        ############### MenuBar ###############
        self.menu = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Neu laden', command=self.restart_program)
        self.filemenu.add_command(label='Beenden', command=self.stop_program)
        self.settings = tk.Menu(self.menu)
        self.menu.add_cascade(label='Einstellungen', menu=self.settings)
        self.settings.add_command(label='Ordner bearbeiten', command=self.directory_setting)
        self.settings.add_command(label='Dateiformate', command=self.fileformats)
        self.settings.add_command(label='Öffne Config', command=self.open_config)
        self.settings.add_command(label='Öffne Readme', command=self.open_readme)
        self.settings.add_command(label='Lösche Verlauf', command=self.delete_chronik)

        ############### MenuBar ###############

        ############### Ergebnisse ###############
        self.search_results = tk.Listbox(self.main_window, width=LISTBOX_WIDTH, height=20)
        self.search_results.grid(row=MAX_DIRECTORIES+1, column=0, rowspan=1, columnspan=3, pady=10)
        self.open_button = tk.Button(self.main_window, width=20)
        self.open_button.config(text='Öffnen', command=self.open_result)
        self.open_button.grid(row=MAX_DIRECTORIES+2, column=2, padx=5, pady=10)
        self.result_lst = []
        self.load_chronik()
        ############### Ergebnisse ###############

        ########## Suche ###############
        self.search_entry = tk.Entry(self.main_window, width=50)
        self.search_entry.grid(row=MAX_DIRECTORIES+2, column=0, padx=5, pady=10)
        self.search_button = tk.Button(width=20)
        self.search_button.config(text='Suchen', command=self.thread_search)
        self.search_button.grid(row=MAX_DIRECTORIES+2, column=1, padx=5, pady=10)

        self.search_status = tk.Text(self.main_window, width=30, height=5)
        self.search_status.grid(row=MAX_DIRECTORIES+3, column=1, padx=5, pady=5)
        self.status = search_status.SearchStatus()
        self.status_update()
        self.cancel_search = tk.Button(width=20)
        self.cancel_search.config(text='Suche abbrechen', command=self.status.search_off)
        self.cancel_search.grid(row=MAX_DIRECTORIES + 4, column=1, padx=5, pady=10)
        ########## Suche ###############

        ############### Pfade ###############
        self.check_variables = [tk.StringVar() for i in range(len(self.folder_lst))]
        self.checkbox_lst = []
        for i in self.folder_lst:
            self.create_checkbox(i, self.folder_lst.index(i))
        ############### Pfade ###############

        self.main_window.mainloop()

    def open_result(self):
        self.chronik_lst = configparser.ConfigParser()
        self.chronik_lst.read('chronik.ini')

        index_result = str(self.search_results.curselection()[0])
        item_to_open = self.search_results.get(index_result)
        item_to_open_file = item_to_open
        if self.unique_results:
            for key in self.chronik_lst['VERLAUF']:#find key
                if item_to_open.lower() == key.split(' ##+##% ')[0].lower():
                    item_to_open_file = self.chronik_lst['VERLAUF'][key]
                    #os.startfile(item_to_open_file)

        #print(item_to_open_file)
        #os.system(f"start '{item_to_open}'")
        os.startfile(item_to_open_file)

    def create_checkbox(self, folder, row_):
        tk.Checkbutton(text=folder, variable=self.check_variables[row_], onvalue=folder,
                       offvalue='').grid(row=row_, column=0, columnspan=3, padx=20, sticky='w')

    def update_listbox(self):
        self.search_results.insert(0, '')
        #for i in self.result_lst:
        #   self.search_results.insert(0,i.replace('/','\\'))
        results_found = False
        if not self.unique_results:
            for i in self.result_lst:
                # if not self.status.search_ongoing:
                #     return
                if i.split('.')[-1].lower() in self.format_lst or self.config_lst['ALL_FORMATS']['key'] == '1':
                    self.search_results.insert(0, i.replace('/', '\\'))

                    a = randint(1000000, 9999999)
                    new_key = str(hex(a))

                    self.chronik_lst['VERLAUF'][new_key] = i.replace('/', '\\')
                    results_found = True

            if self.config_lst['ALL_FORMATS']['key'] == '1' and results_found:
                self.search_results.insert(0, f'######### Treffer für "{self.search_entry.get()}": #########')
                a = randint(1000000, 9999999)
                new_key = str(hex(a))
                self.chronik_lst['VERLAUF'][new_key] = f'######### Treffer für "{self.search_entry.get()}": #########'
            elif self.config_lst['ALL_FORMATS']['key'] == '0' and results_found:
                #self.search_results.insert(0, self.format_lst)
                self.search_results.insert(0, f'######### Treffer für "{self.search_entry.get()}" in den Formaten {self.format_lst}#########')
                a = randint(1000000, 9999999)
                new_key = str(hex(a))
                self.chronik_lst['VERLAUF'][new_key] = f'######### Treffer für "{self.search_entry.get()}" in den Formaten {self.format_lst}#########'

        if self.unique_results:
            for i in self.result_lst:
                # if not self.status.search_ongoing:
                #     return
                #print(i)
                if i.split('.')[-1].lower() in self.format_lst or self.config_lst['ALL_FORMATS']['key'] == '1':
                    self.search_results.insert(0, i.split('/')[-1])

                    a = randint(1000000, 9999999)
                    new_key = str(hex(a))

                    new_key = i.split('/')[-1] + ' ##+##% ' + new_key

                    self.chronik_lst['VERLAUF'][new_key] = i.replace('/', '\\')
                    results_found = True

            if self.config_lst['ALL_FORMATS']['key'] == '1' and results_found:
                self.search_results.insert(0, f'######### Treffer für "{self.search_entry.get()}": #########')
                a = randint(1000000, 9999999)
                new_key = str(hex(a))
                self.chronik_lst['VERLAUF'][new_key] = f'######### Treffer für "{self.search_entry.get()}": #########'
            elif self.config_lst['ALL_FORMATS']['key'] == '0' and results_found:
                #self.search_results.insert(0, self.format_lst)
                self.search_results.insert(0, f'######### Treffer für "{self.search_entry.get()}" in den Formaten {self.format_lst}#########')
                a = randint(1000000, 9999999)
                new_key = str(hex(a))
                self.chronik_lst['VERLAUF'][new_key] = f'######### Treffer für "{self.search_entry.get()}" in den Formaten {self.format_lst}#########'

        with open('chronik.ini', 'w') as file:
            self.chronik_lst.write(file)

    def thread_search(self):
        self.status.toggle_search_status()
        self.search_thread = threading.Thread(target=self.search)
        self.search_thread.start()
        #self.search_thread.terminate()


    def search(self):
        self.search_button.config(state=tk.DISABLED)
        self.search_item = self.search_entry.get().lower()
        if self.search_item == '':
            self.search_item = 'kein Wert eingetragen'
        self.search_folder_lst = [i.get().replace('\\', '/') for i in self.check_variables]
        # for i in self.search_folder_lst:
        #     print(i)
        self.result_lst = []
        print(self.result_lst)
        self.searching_initial()

        self.update_listbox()

        self.search_button.config(state=tk.NORMAL)
        self.status.search_off()
        #print(self.result_lst)

    def searching_initial(self):

        for path in self.search_folder_lst:  # all source paths
            #self.file_list[path] = []
            if not self.status.search_ongoing:
                return
            try:
                item_lst = os.listdir(path)
                for i in range(len(item_lst)):  # list content
                    if not self.status.search_ongoing:
                        messagebox.showinfo('info', 'Suche abgebrochen')
                        return
                    item_lst[i] = path + '/' + item_lst[i]
                    if os.path.isfile(item_lst[i]) and self.search_item in item_lst[i].lower().split('/')[-1]:
                        self.result_lst.append(item_lst[i])
                        self.status.files_found_func()
                        self.status.files_checked_func()
                    elif os.path.isfile(item_lst[i]):
                        self.status.files_checked_func()
                    elif os.path.isdir(item_lst[i]):
                        self.find_all_recursiv(item_lst[i], path)
                        self.status.directory_checked()
            except:
                pass
            # Hier muss noch die Fehlermeldung rein

    def find_all_recursiv(self, cur_directory, path):
        if len(self.result_lst) > self.max_results:
            #messagebox.showinfo('info', 'Zu viele Treffer\nSuche abgebrochen')
            self.status.search_off()
            print(self.status.search_ongoing)

        if not self.status.search_ongoing:
            return
        try:
            dir_content = os.listdir(cur_directory)
            for i in range(len(dir_content)):
                dir_content[i] = cur_directory + '/' + dir_content[i]
                try:
                    if os.path.isfile(dir_content[i]) and self.search_item in dir_content[i].lower().split('/')[-1]:
                        self.result_lst.append(dir_content[i])
                        self.status.files_found_func()
                        self.status.files_checked_func()
                    elif os.path.isfile(dir_content[i]):
                        self.status.files_checked_func()
                    elif os.path.isdir(dir_content[i]):
                        self.find_all_recursiv(dir_content[i], path)
                        self.status.directory_checked()
                except:
                    pass
        except PermissionError:
            pass
        except:
            pass

    def restart_program(self):
        self.stop_program()
        ui = UserInterface()

    def read_config(self):
        self.config_lst = configparser.ConfigParser()
        self.config_lst.read('config.ini')

        self.format_lst = []  #Liste aller zu suchenden Formate

        for ending in self.config_lst['FORMATS']:
            if self.config_lst['FORMATS'][ending] == '1':
                self.format_lst.append(ending)

        for ending in [i.strip('.') for i in self.config_lst['ALSO_INCLUDE']['key_string'].split(' ')]:

            self.format_lst.append(ending)
        #print(self.format_lst)
        #print(self.config_lst['ALL_FORMATS']['key'])

        self.folder_lst = []
        for path in self.config_lst['PATHS']:
            self.folder_lst.append(self.config_lst['PATHS'][path])

        self.max_results = int(self.config_lst['SETTINGS']['max_results'])
        if self.config_lst['SETTINGS']['unique_results'] == 'True':
            self.unique_results = True
        else:
            self.unique_results = False

    def stop_program(self):
        self.main_window.destroy()
        try:
            self.directory_window.destroy()
        except:
            pass
        try:
            self.file_formats.destroy()
        except:
            pass

    def fileformats(self):

        try:
            self.file_formats.destroy()
            self.fileformats()
        except:
            self.file_formats = tk.Tk()
            self.file_formats.config(padx=25, pady=25)
            self.file_formats.title('Dateiformate')
            self.file_formats.attributes("-topmost", True)
            self.button_lst = []
            self.count_timer = 0
            self.formats = []

            for format_ending in self.config_lst['FORMATS']:
                self.formats.append(format_ending)
                self.create_change_button(self.count_timer, format_ending, self.config_lst['FORMATS'][format_ending])

            self.label_for_also_include = tk.Label(self.file_formats, text='Dateiendung mit Leerzeichen getrennt eingeben \n'
                                                                           'um diese in der Suche mit einzuschließen')
            self.label_for_also_include.grid(row=34, column=0, columnspan=3, padx=10, pady=10)
            self.also_include_entry = tk.Entry(self.file_formats, width=30)
            self.also_include_entry.grid(row=35, column=2, padx=10, pady=10)
            self.insert_also_include()
            self.add_format_button = tk.Button(self.file_formats, width=15)
            self.add_format_button.config(text='Formate einschließen', command=self.add_formats)
            self.add_format_button.grid(row=35, column=0, padx=10, pady=10)

            self.button_all_formats = tk.Button(self.file_formats, width=15)
            self.button_all_formats.config(text='Alle Formate', command=self.change_all_format_value)
            self.button_all_formats.grid(row=39, column=0, pady=10, padx=10)
            self.label_all_formats = tk.Label(self.file_formats, text='a', width=20)
            self.label_all_formats.grid(row=39, column=2, pady=10, padx=10)

            self.update_labels()

            self.save_config_button = tk.Button(self.file_formats,width=30)
            self.save_config_button.config(text='speichere config', command=self.save_config)
            self.save_config_button.grid(row=41, column=2, pady=10, padx=10)
            # self.open_config_button = tk.Button(self.file_formats,width=30)
            # self.open_config_button.config(text='Öffne config', command=self.open_config)
            # self.open_config_button.grid(row=41, column=0, pady=10, padx=10)

            self.file_formats.mainloop()

    def insert_also_include(self):
        self.also_include_entry.insert(0, self.config_lst['ALSO_INCLUDE']['key_string'])

    def add_formats(self):
        self.config_lst['ALSO_INCLUDE']['key_string'] = self.also_include_entry.get()
        self.save_config()

    def open_config(self):
        path = os.getcwd().replace('\\','/')
        #print(path)
        os.system(f'start config.ini')

    def open_readme(self):
        path = os.getcwd().replace('\\', '/')
        print(path)
        os.system(f'start readme.txt')

    def create_change_button(self, row, format, value):
        self.button_lst.append([tk.Label(self.file_formats,text='a', width=20)])
        self.button_lst[-1][0].grid(row=row, column=2, pady=10, padx=10)

        self.button_lst[-1][0]['text'] = '2'

        i=self.count_timer
        self.button_lst[-1].append(tk.Button(self.file_formats, width=15, command=lambda i=i:self.change_format_value(i)))
        self.button_lst[-1][1].grid(row=row, column=0, pady=10, padx=10)
        self.button_lst[-1][1].config(text=format)
        self.count_timer += 1

    def update_labels(self):
        for i in range(len(self.button_lst)):
            if self.config_lst['FORMATS'][self.formats[i]]=='1':
                self.button_lst[i][0]['text'] = 'wird angezeigt'
                self.button_lst[i][0].config(bg='green')

            if self.config_lst['FORMATS'][self.formats[i]]=='0':
                self.button_lst[i][0]['text'] = 'ausgeblendet'
                self.button_lst[i][0].config(bg='red')

        if self.config_lst['ALL_FORMATS']['key'] == '1':
            self.label_all_formats['text'] = 'Ja'
            self.label_all_formats.config(bg='green')
        else:
            self.label_all_formats['text'] = 'Nein'
            self.label_all_formats.config(bg='red')

    def change_format_value(self, index):
        if self.config_lst['FORMATS'][self.formats[index]]=='1':
            self.config_lst['FORMATS'][self.formats[index]]='0'

        elif self.config_lst['FORMATS'][self.formats[index]]=='0':
            self.config_lst['FORMATS'][self.formats[index]]='1'

        self.update_labels()

    def save_config(self):
        with open('config.ini', 'w') as file:
            self.config_lst.write(file)
        #messagebox.showinfo('Information', 'Aenderungen gespeichert. \nProgramm muss neugestartet werden')
        self.restart_program()

    def change_all_format_value(self):
        if self.config_lst['ALL_FORMATS']['key'] == '1':
            self.config_lst['ALL_FORMATS']['key'] = '0'
        else:
            self.config_lst['ALL_FORMATS']['key'] ='1'

        self.update_labels()

    def directory_setting(self):

        try:
            self.directory_window.destroy()
            self.directory_setting()
        except:
            self.directory_window = tk.Tk()
            self.directory_window.title('Ordner hizufügen')
            self.directory_window.config(padx=25, pady=25)
            self.directory_window.attributes("-topmost", True)

            self.add_directory_button = tk.Button(self.directory_window, width=30)
            self.add_directory_button.config(text='Hinzufügen', command=self.add_new_path)
            self.add_directory_button.grid(row=0, column=0)

            self.add_directory_entry = tk.Entry(self.directory_window, width=100)
            self.add_directory_entry.grid(row=0, column=1, padx=10, pady=5)

            self.browse_button = tk.Button(self.directory_window, command=self.browse, width=30, text='Ordner auswählen')
            self.browse_button.grid(row=2, column=0, padx=10, pady=5)


            self.directory_window.mainloop()

    def add_new_path(self):
        a = randint(100000, 999999)
        new_key = str(hex(a))
        new_path = f'{self.add_directory_entry.get()}'
        if new_path != '':
            self.config_lst['PATHS'][new_key] = new_path
            self.save_config()
            self.restart_program()

    def browse(self):
        file_path = filedialog.askdirectory()
        self.add_directory_entry.delete(0, 'end')
        self.add_directory_entry.insert(0, file_path)

    def load_chronik(self):
        try:
            self.chronik_lst = configparser.ConfigParser()
            self.chronik_lst.read('chronik.ini')


            if not self.unique_results:
                for key in self.chronik_lst['VERLAUF']:
                    self.search_results.insert(0, self.chronik_lst['VERLAUF'][key])

            if self.unique_results:
                for key in self.chronik_lst['VERLAUF']:
                    self.search_results.insert(0, self.chronik_lst['VERLAUF'][key].split('\\')[-1])
        except KeyError:
            self.delete_chronik()
            self.load_chronik()
        except:
            print('UnknownError')

    def delete_chronik(self):
        clear = '[VERLAUF]'
        with open('chronik.ini', 'w') as file:
            file.writelines(clear)
        self.restart_program()

    def status_update(self):
        self.search_status.delete(1.0,'end')
        self.search_status.insert(1.0,self.status.get_status())
        self.main_window.after(100, func=self.status_update)
