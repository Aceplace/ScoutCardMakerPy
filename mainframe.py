from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

from defensiveformation.defensecontroller import DefenseController
from defensiveformation.defensivelibraryeditor import DefensiveLibraryEditor
from misc.excelscriptparser import get_script_from_excel_file
from misc.powerpointexporter import export_to_powerpoint
from misc.preferences import Preferences
from offensiveformation.formationlibraryedtior import FormationLibraryEditor
from offensiveformation.formationlibraryeditorcontroller import FormationLibraryEditorController
from misc.scoutcardmakerexceptions import ScoutCardMakerException


class App(Tk):
    def __init__(self, preferences, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #menu setup
        menubar = Menu(self)

        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label='New Formation Library', command=self.new_formation_library)
        filemenu.add_command(label='New Defense Library', command=self.new_defense_library)
        filemenu.add_separator()
        filemenu.add_command(label='Open Formation Library', command=self.open_formation_library)
        filemenu.add_command(label='Open Defense Library', command=self.open_defense_library)
        filemenu.add_separator()
        filemenu.add_command(label='Save Formation Library', command=self.save_formation_library)
        filemenu.add_command(label='Save Defense Library', command=self.save_defense_library)
        filemenu.add_command(label='Save Formation Library As...', command=self.save_formation_library_as)
        filemenu.add_command(label='Save Defense Library As...', command=self.save_defense_library_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.on_close)
        menubar.add_cascade(label='File', menu=filemenu)

        viewmenu = Menu(menubar, tearoff = 0)
        self.viewmenu_option = IntVar()
        viewmenu.add_radiobutton(label='Formation Library', value=1, variable=self.viewmenu_option, command=self.change_view)
        viewmenu.add_radiobutton(label='Defense Library', value=2, variable=self.viewmenu_option, command=self.change_view)
        self.viewmenu_option.set(1)
        menubar.add_cascade(label='View', menu=viewmenu)

        createcardsmenu = Menu(menubar, tearoff=0)
        createcardsmenu.add_command(label='Create Scout Cards for Script', command=self.create_scout_cards)
        menubar.add_cascade(label='Create Scout Cards', menu=createcardsmenu)
        self.config(menu=menubar)

        #frame set ups
        mainframe = Frame(self)
        mainframe.pack(side=TOP, fill=BOTH, expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.formation_library_editor_controller = FormationLibraryEditorController()
        self.frames[FormationLibraryEditor] = FormationLibraryEditor(mainframe, self.formation_library_editor_controller)
        self.frames[FormationLibraryEditor].grid(row = 0, column = 0, stick=N+S+E+W)

        self.defense_editor_controller = DefenseController()
        self.frames[DefensiveLibraryEditor] = DefensiveLibraryEditor(mainframe, self.defense_editor_controller)
        self.frames[DefensiveLibraryEditor].grid(row=0, column=0, stick=N + S + E + W)

        self.current_frame = self.frames[FormationLibraryEditor]
        self.current_frame.tkraise()


        self.current_formation_library_filename = preferences.last_saved_formation_library
        if self.current_formation_library_filename:
            try:
                self.formation_library_editor_controller.load_library(self.current_formation_library_filename)
                self.defense_editor_controller.set_formation_library(self.formation_library_editor_controller.formation_library)
            except ScoutCardMakerException as e:
                messagebox.showerror('Open Library Error', e)
                self.current_formation_library_filename = None

        self.current_defense_library_filename = preferences.last_saved_defense_library
        if self.current_defense_library_filename:
            try:
                self.defense_editor_controller.load_defense_library(self.current_defense_library_filename)
            except ScoutCardMakerException as e:
                messagebox.showerror('Open Library Error', e)
                self.current_defense_library_filename = None

        self.last_import_script_location = preferences.last_import_script_location
        self.last_export_powerpoint_location = preferences.last_export_powerpoint_location


    def new_formation_library(self):
        self.current_formation_library_filename = None
        self.formation_library_editor_controller.new_library()

    def new_defense_library(self):
        self.current_defense_library_filename = None
        self.defense_editor_controller.new_defense_library()


    def open_formation_library(self):
        try:
            library_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select formation library", filetypes=(("Formation Library", "*.scmfl"),))
            if library_filename:
                self.formation_library_editor_controller.load_library(library_filename)
                self.current_formation_library_filename = library_filename
                self.defense_editor_controller.set_formation_library(self.formation_library_editor_controller.formation_library)
        except ScoutCardMakerException as e:
                messagebox.showerror('Open Library Error', e)

    def open_defense_library(self):
        try:
            library_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select defense library", filetypes=(("Defense Library", "*.scmdl"),))
            if library_filename:
                self.defense_editor_controller.load_defense_library(library_filename)
                self.current_defense_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Open Library Error', e)

    def save_formation_library(self):
        try:
            library_filename = None
            if self.current_formation_library_filename and os.path.isfile(self.current_formation_library_filename):
                library_filename = self.current_formation_library_filename
            else:
                self.current_formation_library_filename = None
                self.save_formation_library_as()
                return

            if library_filename:
                self.formation_library_editor_controller.save_library(library_filename)
                self.current_formation_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Save Library Error', e)

    def save_defense_library(self):
        try:
            library_filename = None
            if self.current_defense_library_filename and os.path.isfile(self.current_defense_library_filename):
                library_filename = self.current_defense_library_filename
            else:
                self.current_defense_library_filename = None
                self.save_defense_library_as()
                return

            if library_filename:
                self.defense_editor_controller.save_defense_library(library_filename)
                self.current_defense_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Save Library Error', e)

    def save_formation_library_as(self):
        try:
            library_filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                            title='Save formation library',
                                                            filetypes=(('Formation Library', '*.scmfl'),),
                                                            defaultextension='.scmfl')
            if library_filename:
                self.formation_library_editor_controller.save_library(library_filename)
                self.current_formation_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Save Library Error', e)

    def save_defense_library_as(self):
        try:
            library_filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                            title='Save defense library',
                                                            filetypes=(('Defense Library', '*.scmdl'),),
                                                            defaultextension='.scmdl')
            if library_filename:
                self.defense_editor_controller.save_defense_library(library_filename)
                self.current_defense_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Save Library Error', e)

    def create_scout_cards(self):
        try:
            if self.last_import_script_location and os.path.isdir(self.last_import_script_location):
                initial_dir = self.last_import_script_location
            else:
                initial_dir = os.getcwd()
            script_filename = filedialog.askopenfilename(initialdir=initial_dir, title="Select Script",
                                                          filetypes=(("Excel", "*.xlsx"),))
            if script_filename:
                self.last_import_script_location = os.path.dirname(script_filename)
                plays = get_script_from_excel_file(self, script_filename)

                if self.last_export_powerpoint_location and os.path.isdir(self.last_export_powerpoint_location):
                    initial_dir = self.last_export_powerpoint_location
                else:
                    initial_dir = os.getcwd()

                cards_filename = filedialog.asksaveasfilename(initialdir=initial_dir,
                                                                title='Create Scout Cards',
                                                                filetypes=(('Powerpoint', '*.pptx'),),
                                                                defaultextension='.pptx')

                if cards_filename:
                    self.last_export_powerpoint_location = os.path.dirname(cards_filename)
                    export_to_powerpoint(cards_filename, plays,
                                         self.formation_library_editor_controller.formation_library,
                                         self.defense_editor_controller.defense_library)
        except ScoutCardMakerException as e:
            messagebox.showerror('Create Scout Cards Error', e)



    def change_view(self):
        if self.viewmenu_option.get() == 1:
            self.current_frame = self.frames[FormationLibraryEditor]
        elif self.viewmenu_option.get() == 2:
            self.current_frame = self.frames[DefensiveLibraryEditor]
            self.defense_editor_controller.set_formation_library(self.formation_library_editor_controller.formation_library)
        self.current_frame.tkraise()

    def on_close(self):
        preferences = Preferences()
        preferences.last_saved_formation_library = self.current_formation_library_filename
        preferences.last_saved_defense_library = self.current_defense_library_filename
        preferences.last_import_script_location = self.last_import_script_location
        preferences.last_export_powerpoint_location = self.last_export_powerpoint_location
        preferences.save_preferences()
        self.destroy()


preferences = Preferences()
preferences.load_preferences()
root = App(preferences)
root.state('zoomed')
root.protocol('WM_DELETE_WINDOW', root.on_close)
root.mainloop()