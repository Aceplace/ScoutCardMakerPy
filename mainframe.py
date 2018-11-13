from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

from defensiveformation.defensecontroller import DefenseController
from defensiveformation.defensivelibraryeditor import DefensiveLibraryEditor
from offensiveformation.formationlibraryedtior import FormationLibraryEditor
from offensiveformation.formationlibraryeditorcontroller import FormationLibraryEditorController
from misc.scoutcardmakerexceptions import ScoutCardMakerException


class App(Tk):
    def __init__(self, *args, **kwargs):
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
        filemenu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label='File', menu=filemenu)

        viewmenu = Menu(menubar, tearoff = 0)
        self.viewmenu_option = IntVar()
        viewmenu.add_radiobutton(label='Formation Library', value=1, variable=self.viewmenu_option, command=self.change_view)
        viewmenu.add_radiobutton(label='Defense Library', value=2, variable=self.viewmenu_option, command=self.change_view)
        self.viewmenu_option.set(1)
        menubar.add_cascade(label='View', menu=viewmenu)
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

        self.current_formation_library_filename = None
        self.current_defense_library_filename = None

    def new_formation_library(self):
        self.current_libary_filename = None
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
            if self.current_formation_library_filename:
                library_filename = self.current_formation_library_filename
            else:
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
            if self.current_defense_library_filename:
                library_filename = self.current_defense_library_filename
            else:
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

    def change_view(self):
        if self.viewmenu_option.get() == 1:
            self.current_frame = self.frames[FormationLibraryEditor]
        elif self.viewmenu_option.get() == 2:
            self.current_frame = self.frames[DefensiveLibraryEditor]
            self.defense_editor_controller.set_formation_library(self.formation_library_editor_controller.formation_library)
        self.current_frame.tkraise()



root = App()
root.state('zoomed')
root.mainloop()