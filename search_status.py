class SearchStatus:
    def __init__(self):
        self.directories_searched = 0
        self.files_checked = 0
        self.files_found = 0
        self.search_ongoing = False

    def directory_checked(self):
        self.directories_searched += 1

    def files_checked_func(self):
        self.files_checked += 1

    def files_found_func(self):
        self.files_found += 1

    def toggle_search_status(self):
        if self.search_ongoing:
            self.search_ongoing = False
        else:
            self.search_ongoing = True

    def search_off(self):
        self.search_ongoing = False

    def status_reset(self):
        self.directories_searched = 0
        self.files_checked = 0
        self.files_found = 0
        self.search_ongoing = False

    def get_status(self):
        status=''
        status += f'Ordner durchsucht:\t{self.directories_searched}\n'
        status += f'Dateien geprüft:\t  {self.files_checked}\n'
        status += f'Dateien gefunden:\t {self.files_found}\n'
        status += f'Suche läuft noch:\t {self.search_ongoing}'
        return status