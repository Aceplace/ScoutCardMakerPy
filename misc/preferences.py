class Preferences:
    def __init__(self):
        self.last_saved_formation_library = None
        self.last_saved_defense_library = None

    def save_preferences(self):
        with open('preferences.dat', 'w') as config_file:
            if self.last_saved_formation_library:
                config_file.write(f'{self.last_saved_formation_library}\n')
            else:
                config_file.write('\n')
            if self.last_saved_defense_library:
                config_file.write(f'{self.last_saved_defense_library}\n')
            else:
                config_file.write('\n')

    def load_preferences(self):
        try:
            config_file = open('preferences.dat', 'r')
            config_file_lines = config_file.read().split('\n')
            if config_file_lines[0]:
                self.last_saved_formation_library = config_file_lines[0]
            else:
                self.last_saved_formation_library = None
            if config_file_lines[1]:
                self.last_saved_defense_library = config_file_lines[1]
            else:
                self.last_saved_defense_library = None
        except Exception as e:
            self.last_saved_formation_library = None
            self.last_saved_defense_library = None